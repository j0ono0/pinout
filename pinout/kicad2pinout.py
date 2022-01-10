import copy
import math
import tokenize
from tokenize import ENDMARKER, LPAR, RPAR, NAME, NUMBER, OP


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
        if token.type == OP:
            if token.exact_type == LPAR:
                self.depth += 1
            elif token.exact_type == RPAR:
                self.depth -= 1


class KiCadParser:
    def __init__(self, pcb_file, dpi=72):
        self.dpi = dpi
        self.filepath = pcb_file

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

    def at(self, tokens):
        # 'at' can be 2 to 3 numbers. x, y, (and optional) rotation
        at = []
        prefix = ""
        exit_depth = tokens.depth
        while tokens.depth >= exit_depth:
            if tokens.next().type == NUMBER:
                at.append(prefix + tokens.current.string.strip('"'))
                prefix = ""
            else:
                prefix = tokens.current.string.strip('"')

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
        while tokens.current.type != ENDMARKER:
            if tokens.current.type == NAME and tokens.current.string == "footprint":
                fp = {
                    "id": counter(),
                    "at": None,
                    "fp_text": [],
                    "layer": None,
                    "name": tokens.next().string.strip('"'),
                }
                exit_depth = tokens.depth
                while tokens.depth >= exit_depth:
                    if tokens.next().type == NAME:
                        if tokens.current.string == "layer":
                            fp["layer"] = tokens.next().string.strip('"')
                        if tokens.current.string == "at":
                            fp["at"] = self.at(tokens)
                        if tokens.current.string == "fp_text":
                            fp["fp_text"].append(self.fp_text(tokens))
                footprints.append(fp)
            tokens.next()
        return footprints


class PinoutParser(KiCadParser):
    """Filter and format data exclusively for pinout requirements"""

    def __init__(self, filepath, dpi=72):
        super().__init__(filepath, dpi)

    def layers(self):
        layers = super().layers()
        pinout_layers = [
            layer["canonical_name"]
            for layer in layers.values()
            if layer["user_name"] and layer["user_name"].lower().startswith("pinout")
        ]
        return pinout_layers

    def footprints(self):
        pinout_fps = []
        pinout_layers = self.layers()
        pinout_origin = [0, 0]
        fps = super().footprints()

        # Collect all pinout footprints
        for fp in fps:
            for fp_text in fp["fp_text"]:
                if fp_text["layer"] in pinout_layers or fp_text[
                    "text"
                ].lower().startswith("pinout"):
                    if fp not in pinout_fps:
                        pinout_fps.append(fp)

        # Find pinout origin
        # Needs to be a copy as original pinout_origin
        # is later changed to (0,0)
        for fp in pinout_fps:
            if fp["name"] == "pinout:pinout_origin":
                pinout_origin = copy.copy(fp["at"])

        # Offset coordinates by pinout_origin
        for fp in pinout_fps:
            oldat = fp["at"][:2]
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
