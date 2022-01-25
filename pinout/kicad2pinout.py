from collections import namedtuple
import copy
import math
import tokenize
from tokenize import ENDMARKER, LPAR, RPAR, NAME, NUMBER, OP
import re
import warnings

from pinout.components.pinlabel import PinLabelGroup
from pinout.components.annotation import AnnotationLabel

Pinout_item = namedtuple("Pinout_item", ["content", "attrs", "x", "y", "scale"])


def format_tag_warning(message, category, filename, lineno, file=None, line=None):
    return f"{category.__name__}: {message}"


def rotate_point_coord(coord, rotate):
    """Rotate a coordinate around (0,0) by angle in degrees."""
    # Rotate in opposite direction to kicad for SVG coordinate space
    rotate = -rotate
    x, y = coord
    x1 = x * math.cos(math.radians(rotate)) - y * math.sin(math.radians(rotate))
    y1 = x * math.sin(math.radians(rotate)) + y * math.cos(math.radians(rotate))
    return (x1, y1)


class Counter:
    def __init__(self, start_num):
        self.count = start_num

    def __call__(self):
        self.count += 1
        return self.count


class Tokens:
    def __init__(self, filepath):
        self.tokens = self.load_tokens(filepath)
        self.depth = 0
        self.current = None
        # Get initial value
        self.next()

    def next(self):
        self.current = next(self.tokens)
        self.update_depth(self.current)
        return self.current

    def goto(self, name):
        while self.current.string != name:
            self.next()
        return True

    def load_tokens(self, filepath):
        with tokenize.open(filepath) as f:
            tokens = tokenize.generate_tokens(f.readline)
            for tok in tokens:
                yield tok

    def update_depth(self, token):
        if token.exact_type == LPAR:
            self.depth += 1
        elif token.exact_type == RPAR:
            self.depth -= 1


class KiCadParser:
    def __init__(self, pcb_file, dpi=72, version=6):
        self.dpi = dpi
        self.filepath = pcb_file
        self.version = version

    def fp_text(self, tokens):
        exit_depth = tokens.depth
        fp_text = {
            "type": tokens.next().string.strip('"'),
            "text": tokens.next().string.strip('"'),
        }
        while tokens.depth >= exit_depth:
            if tokens.current.type == NAME:
                if tokens.current.string == "at":
                    fp_text["at"] = self.at(tokens)
                if tokens.current.string == "layer":
                    fp_text["layer"] = tokens.next().string.strip('"')
            tokens.next()
        return fp_text

    def fp_text_kicad_5(self, tokens):
        exit_depth = tokens.depth
        fp_text = {
            "type": tokens.next().string,
            "text": "",
            "layer": "",
        }
        # collate text until attribute starts
        while tokens.next().exact_type != LPAR:
            fp_text["text"] += tokens.current.string.strip('"')

        # Find and collate attributes
        tokens.next()
        while tokens.depth >= exit_depth:
            if tokens.current.type == NAME:
                if tokens.current.string == "at":
                    fp_text["at"] = self.at(tokens)
                if tokens.current.string == "layer":
                    while tokens.current.exact_type != RPAR:
                        fp_text["layer"] += tokens.next().string
            tokens.next()
        return fp_text

    def at(self, tokens):

        # 'at' can be 2 to 3 numbers. x, y, (and optional) rotation
        at = []
        prefix = ""
        exit_depth = tokens.depth
        while tokens.depth >= exit_depth:
            if tokens.current.type == NUMBER:
                at.append(prefix + tokens.current.string.strip('"'))
                prefix = ""
            elif tokens.current.type == OP:
                prefix = tokens.current.string
            tokens.next()

        # Convert strings into numbers
        at = [float(num) for num in at]

        # Convert x and y (mm) values to px.
        # !!! Do NOT convert rotation value
        at[:2] = [self.mm_to_dpi(val) for val in at[:2]]

        return at

    def mm_to_dpi(self, mm):
        return mm / 25.5 * self.dpi

    def get_single_attr(self, key):
        tokens = Tokens(self.filepath)
        tokens.goto(key)
        return tokens.next().string.strip('"')

    def version(self):
        return self.get_single_attr("version")

    def generator(self):
        return self.get_single_attr("generator")

    def paper(self):
        return self.get_single_attr("paper")

    def general(self):
        general = {}
        tokens = Tokens(self.filepath)
        tokens.goto("general")
        exit_depth = tokens.depth
        while tokens.depth >= exit_depth:
            # Assumes all entries are (key value) pairs
            if tokens.current.type == NAME and tokens.depth == exit_depth + 1:
                key = tokens.current.string.strip('"')
                val = tokens.next()
                if val.type == NUMBER:
                    general[key] = float(val.string)
                else:
                    general[key] = val.string.strip('"')
            tokens.next()
        return general

    def layers(self):
        layers = {}
        tokens = Tokens(self.filepath)
        tokens.goto("layers")
        exit_depth = tokens.depth
        while tokens.depth >= exit_depth:
            if tokens.current.type == NUMBER:
                key = int(tokens.current.string)
                layers[key] = {
                    "canonical_name": tokens.next().string.strip('"'),
                    "type": tokens.next().string.strip('"'),
                    "user_name": None,
                }
                if tokens.next().type != OP:
                    layers[key]["user_name"] = tokens.current.string.strip('"')
            tokens.next()
        return layers

    def footprints(self):
        # counter used give unique id to each footprint
        counter = Counter(0)
        footprints = []
        tokens = Tokens(self.filepath)

        # Set footprint name depending on KiCad version
        if self.version < 6:
            fooprint_name = "module"
        else:
            fooprint_name = "footprint"

        while tokens.current.type != ENDMARKER:
            if tokens.current.type == NAME and tokens.current.string == fooprint_name:
                fp = {
                    "id": counter(),
                    "at": None,
                    "fp_text": [],
                    "layer": "",
                    "name": tokens.next().string.strip('"'),
                }
                exit_depth = tokens.depth

                if self.version >= 6:

                    while tokens.depth >= exit_depth:
                        tokens.next()
                        if tokens.current.type == NAME:
                            if tokens.current.string == "layer":
                                fp["layer"] = tokens.next().string.strip('"')
                            if tokens.current.string == "at":
                                fp["at"] = self.at(tokens)
                            if tokens.current.string == "fp_text":
                                fp["fp_text"].append(self.fp_text(tokens))
                    footprints.append(fp)

                else:
                    #####################################################
                    # KiCad 5 does NOT wrap attribute strings in quotes #
                    # tokens need to be collated until end of attribute.#
                    #####################################################
                    while tokens.next().exact_type != LPAR:
                        fp["name"] += tokens.current.string

                    while tokens.depth >= exit_depth:
                        if (
                            tokens.next().type == NAME
                            and tokens.depth == exit_depth + 1
                        ):
                            if tokens.current.string == "layer":
                                while tokens.next().exact_type != RPAR:
                                    fp["layer"] += tokens.current.string
                            elif tokens.current.string == "at":
                                fp["at"] = self.at(tokens)
                            elif tokens.current.string == "fp_text":
                                fp["fp_text"].append(self.fp_text_kicad_5(tokens))

                            tokens.next()
                    footprints.append(fp)

            tokens.next()
        return footprints

    def gr_text(self):
        text = {}
        tokens = Tokens(self.filepath)
        while tokens.current.type != ENDMARKER:
            if tokens.current.type == NAME and tokens.current.string == "gr_text":
                content = tokens.next().string.strip('"')
                match = re.search("{{[\.\-_ a-zA-Z0-9]+}}", content)
                if match:
                    key = match.group(0)[2:-2]
                    content = (
                        re.sub("{{[\.\- _a-zA-Z0-9]+}}", "", content).strip('"').strip()
                    )
                    # sub double quotes back in
                    content = re.sub("{dblquote}", '"', content)
                    # unescape chars
                    content = bytes(content, "utf-8").decode("unicode_escape")
                    text[key] = content

            tokens.next()
        return text


class PinoutParser(KiCadParser):
    """Filter and format data exclusively for pinout requirements"""

    def __init__(self, filepath, dpi=72, version=6):
        super().__init__(filepath, dpi, version)
        self.pinout_img = None

    def layers(self):
        layers = super().layers()
        pinout_layers = [
            layer["canonical_name"]
            for layer in layers.values()
            if layer["user_name"] and layer["user_name"].lower().startswith("pinout")
        ]
        return pinout_layers

    def link_image(self, image_instance):
        self.pinout_img = image_instance

    def footprints(self):
        pinout_fps = []
        pinout_origin = [0, 0]
        fps = super().footprints()
        # Collect all pinout footprints
        for fp in fps:
            if fp["name"].startswith("pinout"):
                pinout_fps.append(fp)

        # Find pinout origin
        # Needs to be a copy as original pinout_origin
        # is later changed to (0,0)
        for fp in pinout_fps:
            if fp["name"] == "pinout:Origin":
                pinout_origin = copy.copy(fp["at"])

        # Offset coordinates by pinout_origin
        for fp in pinout_fps:
            fp["at"][:2] = [a - b for a, b in zip(fp["at"][:2], pinout_origin)]

        # Rotate fp_text coords

        for fp in pinout_fps:
            try:
                rotate = fp["at"][2]
            except IndexError:
                rotate = 0

            for fp_text in fp["fp_text"]:
                x, y = fp_text["at"][:2]
                rx, ry = rotate_point_coord((x, y), rotate)
                fp_text["at"][:2] = [rx, ry]

        return pinout_fps

    def transfer_footprint_coords(self, footprint):

        """Transfer footprint and child fp_text coords to pinout Image instance"""

        self.pinout_img.add_coord(f"footprint_{footprint['id']}", *footprint["at"][:2])

        for fp_text in footprint["fp_text"]:
            if fp_text["type"] == "value":
                self.pinout_img.add_coord(
                    f"{fp_text['text']}_{footprint['id']}", *fp_text["at"][:2]
                )

    def get_text(self):
        text = {}
        for fp in self.footprints():
            if fp["name"] == "pinout:Text":
                for fp_text in fp["fp_text"]:
                    if fp_text["type"] == "reference":
                        key = fp_text["text"].split(" ", 1)[1]
                    elif fp_text["type"] == "user":
                        tag = fp_text["text"]
                    elif fp_text["type"] == "value":
                        content = fp_text["text"]
                text[key] = {"content": content, "tag": tag}
        return text

    def get_scale(self, x, y):
        # Deduce scale from label location (it is relative to pin)
        try:
            sx = x / abs(x)
        except ZeroDivisionError:
            sx = 1
        try:
            sy = y / abs(y)
        except ZeroDivisionError:
            sy = 1
        return (sx, sy)

    def get_footprint_specs(self, footprint):
        for fp_text in footprint["fp_text"]:
            attrs = ["hh"]
            if fp_text["type"] == "user":
                # Excepted format: <leaderline direction>
                attrs = fp_text["text"].split(" ")
            elif fp_text["type"] == "value":
                x, y = self.pinout_img.coord(
                    f"{fp_text['text']}_{footprint['id']}", raw=True
                )
                scale = self.get_scale(x, y)
                content = fp_text["text"]
        return Pinout_item(content, attrs, x, y, scale)

    def add_pinlabels(self, container):
        for fp in self.footprints():

            self.transfer_footprint_coords(fp)

            # Get transformed footprint coords
            pin_x, pin_y = self.pinout_img.coord(f"footprint_{fp['id']}")

            # Add pinlabels
            if fp["name"] == "pinout:PinLabel":
                self.transfer_footprint_coords(fp)

                # Get transformed footprint coords
                pin_x, pin_y = self.pinout_img.coord(f"footprint_{fp['id']}")

                fp_specs = self.get_footprint_specs(fp)

                # Parse label content
                tags = [
                    t[2:-2]
                    for t in re.findall(
                        "{{-?[_a-zA-Z]+[_a-zA-Z0-9-]*}}", fp_specs.content
                    )
                ]
                txts = [
                    t.strip()
                    for t in re.split(
                        "{{-?[_a-zA-Z]+[_a-zA-Z0-9-]*}}", fp_specs.content
                    )
                    if t
                ]
                if len(txts) > len(tags):
                    # User has fogotten to include tags on pinlabels
                    # Warn them and add place-holder tags
                    len_diff = len(txts) - len(tags)
                    txts += ["no_tag_assigned"] * len_diff

                    warnings.formatwarning = format_tag_warning
                    warnings.warn(
                        "pin-label(s) have not been assigned a tag in KiCad.",
                        SyntaxWarning,
                    )

                labels = list(zip(txts, tags))
                # Create pinlabel group
                container.add(
                    PinLabelGroup(
                        x=pin_x,
                        y=pin_y,
                        pin_pitch=(0, 0),
                        label_start=(abs(fp_specs.x), abs(fp_specs.y)),
                        label_pitch=(0, 0),
                        labels=[labels],
                        scale=fp_specs.scale,
                        leaderline={"direction": fp_specs.attrs[0]},
                    )
                )

    def add_annotations(self, container):
        for fp in self.footprints():

            if fp["name"] == "pinout:Annotation":
                scale = (1, 1)
                self.transfer_footprint_coords(fp)

                # Get transformed footprint coords
                pin_x, pin_y = self.pinout_img.coord(f"footprint_{fp['id']}")

                for fp_text in fp["fp_text"]:
                    # Get annotation attrs
                    if fp_text["type"] == "user":
                        # Excepted format: <leaderline direction>
                        direction, *_ = fp_text["text"].split(" ")

                    elif fp_text["type"] == "value":
                        x, y = self.pinout_img.coord(
                            f"{fp_text['text']}_{fp['id']}", raw=True
                        )
                        content = fp_text["text"]

                        scale = self.get_scale(x, y)

                container.add(
                    AnnotationLabel(
                        content=content,
                        x=pin_x,
                        y=pin_y,
                        body={"x": abs(x), "y": abs(y)},
                        scale=scale,
                    )
                )
