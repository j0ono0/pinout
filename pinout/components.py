import base64
import copy
from collections import namedtuple
from pathlib import Path
from . import file_manager

from .templates import (
    svg_group,
    svg_image,
    svg_label,
    svg_path,
    svg_rect,
    svg_style,
    svg_text,
)

BoundingBox = namedtuple("BoundingBox", ("x y w h"))
BoundingCoords = namedtuple("BoundingCoords", ("x_min y_min x_max y_max"))
Coords = namedtuple("Coords", ("x y"))


#####################################################################
# Base Element and Component classes


class ClassMethodMissing(Exception):
    """ An element is missing an expected method """

    pass


class SVG:
    """Common base for all SVG entities that ultimately have a graphical representation."""

    def __init__(self, x=0, y=0, scale=(1, 1), rotation=0, tag="", config=None):
        self.cfg = config
        self.rotation = rotation
        self._scale = Coords(*scale)
        self.tag = tag
        self.x = x
        self.y = y

    @property
    def scale(self):
        """Tuple used to represent orientation of entity"""
        # NOTE: set here for override by Component
        return self._scale

    @scale.setter
    def scale(self, value):
        """Scale setter property - overridden by Component

        :param value: (x, y) where x and y are either 1 or -1
        :type value: tuple
        """
        # NOTE: set here for override by Component
        self._scale = value

    def extract_scale(self, coords):
        """Separate scale information from a tuple that represents (x, y) or (width, height) values."""

        if not all(val >= 0 for val in coords):
            self.scale = Coords(*[i / abs(i) if i != 0 else 1 for i in coords])
        return Coords(*[abs(i) for i in coords])


class Element(SVG):
    """Container that exclusively handles graphical SVG code. """

    def __init__(self, width=0, height=0, *args, **kwargs):
        self.width = width
        self.height = height
        super().__init__(*args, **kwargs)

    @property
    def bounding_coords(self):
        """Coordinates, relative to its parent, representing sides of a rectangle that encompass the rendered element."""
        x_min, x_max = sorted(
            [self.x * self.scale.x, (self.x + self.width) * self.scale.x]
        )
        y_min, y_max = sorted(
            [self.y * self.scale.y, (self.y + self.height) * self.scale.y]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

    @property
    def bounding_rect(self):
        """Coordinates and size representing the location of an elements origin (usually top-left corner)"""
        x_min, y_min, x_max, y_max = self.bounding_coords
        return BoundingBox(x_min, y_min, x_max - x_min, y_max - y_min)

    def render(self):
        raise ClassMethodMissing(f"{self} requires a 'render' method.")


class Component(SVG):
    """Container object that manages child Components and/or Elements as a group."""

    conf = {}

    def __init__(self, children=None, *args, **kwargs):
        self.children = []
        super().__init__(*args, **kwargs)

    @property
    def bounding_coords(self):
        """Coordinates, relative to its parent, representing sides of a rectangle that encompass all child elements of the rendered Component."""
        # Untransformed bounding coords
        x_min = y_min = x_max = y_max = 0
        for child in self.children:
            try:
                child_coords = child.bounding_coords
                x_min = min(x_min, child_coords.x_min)
                y_min = min(y_min, child_coords.y_min)
                x_max = max(x_max, child_coords.x_max)
                y_max = max(y_max, child_coords.y_max)
            except AttributeError:
                # The child has no bounding_coords.
                pass
        return BoundingCoords(
            self.x + x_min, self.y + y_min, self.x + x_max, self.y + y_max
        )

    @property
    def width(self):
        """Calculated width that encompasses all child elements"""
        try:
            x_min, y_min, x_max, y_max = self.bounding_coords
            return x_max - x_min
        except ValueError:
            # Component has no children with bounding_coords
            return 0

    @property
    def height(self):
        """Calculated height that encompasses all child elements"""
        try:
            x_min, y_min, x_max, y_max = self.bounding_coords
            return y_max - y_min
        except ValueError:
            # Component has no children with bounding_coords
            return 0

    @property
    def scale(self):

        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        for child in self.children:
            if issubclass(type(child), Element):
                child.scale = self.scale

    @property
    def bounding_rect(self):
        """Coordinates representing location and size"""
        x_min, y_min, x_max, y_max = self.bounding_coords
        return BoundingBox(x_min, y_min, x_max - x_min, y_max - y_min)

    def add_and_instantiate(self, cls, *args, **kwargs):
        """Instantiate a class and add it to the components children."""

        if issubclass(cls, Element):
            kwargs["scale"] = self.scale

        instance = cls(*args, **kwargs)
        self.children.append(instance)
        return instance

    def patch_config(self, source, patch):
        """Recursively update source with patch dict items."""
        try:
            for key, val in patch.items():
                if type(val) == dict:
                    self.patch_config(source[key], patch[key])
                else:
                    source[key] = val
        except KeyError:
            # patch has no items
            pass
        return source

    def render(self):
        """Render Component, and children, as SVG markup."""
        output = ""
        for child in self.children:
            output += child.render()
        return svg_group.render(
            x=self.x,
            y=self.y,
            tag=self.tag,
            content=output,
            # NOTE: Graphically, components are *not* affected by scale
            scale=Coords(1, 1),
        )


class StyleSheet:
    def __init__(self, path, embed=False, config=None):
        """stylesheet handler"""
        self.path = path
        self.embed = embed
        self.cfg = config

    def render(self):
        """Create SVG tag with content to either embed or link styles.

        :return: SVG <link> or <style> code
        :rtype: string
        """
        context = {}
        if self.embed:
            p = Path(self.path)
            context["css_data"] = p.read_text()
        else:
            context["path"] = self.path

        return svg_style.render(**context)


#####################################################################
# SVG tag classes


class Image(Element):
    def __init__(self, href, embed=False, *args, **kwargs):
        """Associate a PNG, JPG or SVG formatted image to the diagram."""
        super().__init__(*args, **kwargs)

        self.href = href
        self.embed = embed

    @property
    def bounding_coords(self):
        """Coordinates of element boundaries"""
        x_min, x_max = sorted(
            [self.x * self.scale.x, (self.x + self.width) * self.scale.x]
        )
        y_min, y_max = sorted(
            [self.y * self.scale.y, (self.y + self.height) * self.scale.y]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

    def render(self):
        """Render SVG markup either linking or embedding an image."""
        media_type = Path(self.href).suffix[1:]
        path = Path(self.href)
        if self.embed:
            if media_type == "svg":
                with path.open() as f:
                    svg_data = f.read()
                return svg_group.render(x=self.x, y=self.y, content=svg_data)
            else:
                encoded_img = base64.b64encode(open(self.href, "rb").read())
                path = f"data:image/{media_type};base64,{encoded_img.decode('utf-8')}"

        return svg_image.render(
            x=self.x, y=self.y, width=self.width, height=self.height, href=path
        )


class Rect(Element):
    """SVG <rect> (rectangle) element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self):
        return svg_rect.render(
            x=self.x,
            y=self.y,
            scale=self.scale,
            **self.cfg,
        )


class SVGPath(Element):
    """SVG <path> element"""

    def __init__(self, definition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.definition = definition

    def render(self):
        return svg_path.render(d=self.definition, scale=self.scale, **self.cfg)


class Text(Element):
    """SVG <text> element."""

    def __init__(self, text_msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_msg = text_msg

    def render(self):
        """create an SVG <text> tag."""
        return svg_text.render(
            text_msg=self.text_msg, x=self.x, y=self.y, scale=self.scale, **self.cfg
        )


#####################################################################
# Composite classes


class Label(Element):
    """SVG <text> and <rect> markup in a single element."""

    def __init__(self, text_msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_msg = text_msg
        self.width = self.cfg["rect"]["width"]
        self.height = self.cfg["rect"]["height"]

    def render(self):
        """Render SVG component."""
        return svg_label.render(
            text_msg=self.text_msg,
            x=self.x,
            y=self.y,
            scale=self.scale,
            **self.cfg,
        )


class PinLabel(Component):
    """Create a single Pinlabel"""

    def __init__(
        self,
        text_msg,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # Assign config values if none supplied
        offset = self.cfg["offset"]

        # Separate offset and scale data
        offset = self.extract_scale(offset)

        vertical_move = f"V {offset.y}" if offset.y != 0 else ""
        horizontal_move = f"H {offset.x}" if offset.x != 0 else ""

        definition = f"M 0 0 {vertical_move} {horizontal_move}"

        self.add_and_instantiate(
            SVGPath,
            definition=definition,
            config=self.cfg["leaderline"],
        )

        self.add_and_instantiate(
            Label,
            text_msg,
            x=offset.x - 1,
            y=offset.y - self.cfg["label"]["rect"]["height"] / 2,
            scale=self.scale,
            tag=self.tag,
            config=self.cfg["label"],
        )


class PinLabelRow(Component):
    """Create a row of PinLabels and leaderline connecting the row to an origin coordinate."""

    def __init__(self, offset, labels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = self.extract_scale(offset)
        self.labels = self.add_and_instantiate(
            Component, x=offset[0], y=offset[1], scale=self.scale
        )

        cfg_tag = self.cfg.get("pinlabelrow", {}).get("tag", "")
        self.tag = (cfg_tag + self.tag).strip()

        self.add_labels(labels)

    def add_labels(self, label_list):
        for i, label in enumerate(label_list):
            ctx = dict(zip(("text_msg", "tag", "config"), label))

            # Create a duplicate config for each pinlabel
            config = self.patch_config(copy.deepcopy(self.cfg), ctx.get("config", {}))

            # update tag in pinlabel and leaderline
            config["tag"] = " ".join([config["tag"], ctx.get("tag", "")])
            config["leaderline"]["tag"] = " ".join(
                [config["leaderline"]["tag"], ctx.get("tag", "")]
            )

            # update pinlabel config with tag styles
            tag_color = self.conf["tags"][ctx["tag"]]["color"]
            patch = {
                "label": {
                    "rect": {"fill": tag_color},
                },
                "leaderline": {"stroke": tag_color},
            }
            self.patch_config(config, patch)

            if i == 0:
                # Create a leaderline joining the labelrow to the offset origin
                v_move = f"V {self.offset.y}" if self.offset.y != 0 else ""
                h_move = f"H {self.offset.x}" if self.offset.x != 0 else ""
                definition = f"M 0 0 {v_move} {h_move}"

                self.add_and_instantiate(
                    SVGPath,
                    definition=definition,
                    scale=self.scale,
                    config=config["leaderline"],
                )

            # Add PinLabel to label_row
            label_x = self.labels.width * self.scale.x
            self.labels.add_and_instantiate(
                PinLabel,
                ctx["text_msg"],
                x=label_x,
                y=0,
                tag=config["tag"],
                scale=self.scale,
                config=config,
            )


class PinLabelSet(Component):
    """Add rows of PinLabels to a 'header' of pins"""

    def __init__(self, offset, labels, pitch=(1, 1), *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a Component for each row in 'labels'
        for i, label_list in enumerate(labels):
            pin_x = pitch[0] * i
            pin_y = pitch[1] * i
            if pitch[1] == 0:
                # Horizontal pinset
                row_offset = (offset[0] - pin_x, offset[1] + abs(pin_x))
            else:
                row_offset = offset

            label_row = self.add_and_instantiate(
                PinLabelRow,
                offset=row_offset,
                labels=label_list,
                x=pin_x,
                y=pin_y,
                config=self.cfg,
            )


class Legend(Component):
    """Provide a colour coded legend to describe pin labels. """

    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pad = Coords(*self.cfg["padding"])
        row_height = self.cfg["row_height"]
        swatch_size = row_height * 2 / 3

        for i, (name, tag) in enumerate(categories):
            entry = self.add_and_instantiate(
                Component, x=pad.x, y=pad.y + row_height * i, tag=self.cfg["tag"]
            )
            entry.add_and_instantiate(
                Text,
                name,
                x=swatch_size * 2,
                y=0,
                width=self.cfg["rect"]["width"],
                height=row_height,
                config=self.cfg["text"],
            )

            pinlabel_config = copy.deepcopy(self.conf["pinlabel"])
            pinlabel_config["offset"] = (-swatch_size / 2, 0)
            pinlabel_config["label"]["rect"]["height"] = swatch_size
            pinlabel_config["label"]["rect"]["width"] = swatch_size
            pinlabel_config["label"]["rx"] = 2

            entry.add_and_instantiate(
                PinLabel,
                text_msg="",
                x=swatch_size * 1.5,
                tag="pl " + tag,
                config=pinlabel_config,
            )

        # Add an panel *behind* component
        self.cfg["rect"]["height"] = row_height * len(categories) + pad.y
        self.children.insert(
            0,
            Rect(
                x=0,
                y=0,
                width=self.cfg["rect"]["width"],
                height=self.cfg["rect"]["height"],
                scale=self.scale,
                config=self.cfg["rect"],
            ),
        )


class Annotation(Component):
    def __init__(self, text_msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        offset = Coords(*self.cfg["offset"])
        path_definition = f"M 0 0 l {offset.x} {offset.y}"
        # Shift label rect to move 'origin' to half height on left hand edge

        self.add_and_instantiate(
            Label,
            text_msg,
            x=offset.x,
            y=offset.y - self.cfg["label"]["rect"]["height"] / 2,
            config=self.cfg["label"],
        )
        self.add_and_instantiate(
            SVGPath, path_definition, config=self.cfg["leaderline"]
        )
