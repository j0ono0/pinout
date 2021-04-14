import base64
from collections import namedtuple
from pathlib import Path
import pkg_resources
import yaml

from .templates import (
    svg_group,
    svg_image,
    svg_label,
    svg_line,
    svg_rect,
    svg_style,
    svg_textblock,
)

BoundingBox = namedtuple("BoundingBox", ("x y w h"))
BoundingCoords = namedtuple("BoundingCoords", ("x_min y_min x_max y_max"))
Coords = namedtuple("Coords", ("x y"))


# Load default settings
path = "resources/default_config.yaml"
cfg = yaml.safe_load(pkg_resources.resource_string(__name__, path).decode("utf-8"))


#####################################################################
# Base Element and Component classes


class ClassMethodMissing(Exception):
    """ An element is missing an expected method """

    pass


class SVG:
    def __init__(self, x=0, y=0, scale=(1, 1), rotation=0, tags=""):
        self.x = x
        self.y = y
        self._scale = scale if isinstance(scale, Coords) else Coords(*scale)
        self.rotation = rotation
        self.tags = tags

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value

    def extract_scale(self, coords):
        """Separate scale information from a tuple that represents (x, y) or (width, height) values. Components and elements control orientation via the scale property rather than negative dimension/direction values. **NOTE**: Existing scale property is only overridded if the provided coords include a negative value.

        :param coords: tuple representing  (x, y) or (width, height). values may be positive or negative.
        :type coords: Union(tuple, Coords)
        :raises ClassMethodMissing: [description]
        :return: nametuple with absolute values
        :rtype: Coords
        """

        if not all(val >= 0 for val in coords):
            self.scale = Coords(*[i / abs(i) if i != 0 else 1 for i in coords])
        return Coords(*[abs(i) for i in coords])


class Element(SVG):
    def __init__(self, width=0, height=0, *args, **kwargs):
        self._width = width
        self._height = height
        super().__init__(*args, **kwargs)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def bounding_coords(self):
        x_min, x_max = sorted(
            [self.x * self.scale.x, (self.x + self.width) * self.scale.x]
        )
        y_min, y_max = sorted(
            [self.y * self.scale.y, (self.y + self.height) * self.scale.y]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

    @property
    def bounding_rect(self):
        x_min, y_min, x_max, y_max = self.bounding_coords
        return BoundingBox(x_min, y_min, x_max - x_min, y_max - y_min)

    def render(self):
        raise ClassMethodMissing(f"{self} requires a 'render' method.")


class Component(SVG):
    """Container object that manages groups of child objects.
    All children must include a render and bounding_coords functions."""

    def __init__(self, children=None, *args, **kwargs):
        """Container object that manages child Component and/or Elements as a group, it renders as a <group> tag.
        Child coordinates are all relative to their parent Component.
        When scale is applied to a Component no direct affect to the <group> tag is applied but the scale setting is passed down to direct child **Elements**.

        :param children: Component and/or Element objects, defaults to None
        :type children: Union[Component, Element], optional
        """
        self.children = []
        super().__init__(*args, **kwargs)
        if children:
            self.add(children)

    @property
    def bounding_coords(self):
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
        try:
            x_min, y_min, x_max, y_max = self.bounding_coords
            return x_max - x_min
        except ValueError:
            # Component has no children with bounding_coords
            return 0

    @property
    def height(self):
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
        x_min, y_min, x_max, y_max = self.bounding_coords
        return BoundingBox(x_min, y_min, x_max - x_min, y_max - y_min)

    def add(self, children):
        try:
            for child in children:
                self.children.append(child)
                if issubclass(type(child), Element):
                    child.scale = self.scale

        except TypeError:
            self.add([children])

    def render(self):
        """Render Component, and children, as SVG markup.
        NOTE: *scale* only affects Elements! It does not affect the grapical appearance of Components.

        :return: SVG markup of component including all children.
        :rtype: str
        """
        output = ""
        for child in self.children:
            output += child.render()
        return svg_group.render(
            x=self.x,
            y=self.y,
            tags=self.tags,
            content=output,
            # NOTE: Graphically, components are *not* affected by scale
            scale=Coords(1, 1),
        )


class StyleSheet:
    def __init__(self, path, embed=False):
        """Include a stylesheet in the diagram

        :param path: Filename, including path, of the external stylesheet. *NOTE*: If *embedding*, a relative path is relative to the current working directory. If *linking*, a relative path is relative to the location of the final SVG diagram.
        :type path: str
        :param embed: Elect to link or embed the stylesheet, defaults to False
        :type embed: bool, optional
        """
        self.path = path
        self.embed = embed

    def render(self):
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
        super().__init__(*args, **kwargs)

        self.href = href
        self.embed = embed

    @property
    def bounding_coords(self):
        x_min, x_max = sorted(
            [self.x * self.scale.x, (self.x + self.width) * self.scale.x]
        )
        y_min, y_max = sorted(
            [self.y * self.scale.y, (self.y + self.height) * self.scale.y]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

    def render(self):
        """Generates SVG <image> tag using the image 'filename', Note that JPG and PNG are the only binary images files officially supported by the SVG format. If 'embed' is True the image is assigned to the path as a data URI. JPG and PNG image are base64 encoded, SVG files included verbatim. Otherwise the path 'src' is assigned 'filename'. Note: 'filename' includes the path to the file. Where a relative path is used it must be relative to the **exported file**.

        :return: SVG <image> component
        :rtype: str
        """
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
    def __init__(self, rx=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rx = rx

    def render(self):
        return svg_rect.render(
            rx=self.rx,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            scale=self.scale,
            tags=self.tags,
        )


class Line(Element):
    def render(self):
        return svg_line.render(
            d=f"M 0 0 V {self.height} H {self.width}",
            scale=self.scale,
            tags=self.tags,
        )


class TextBlock(Element):

    default_width = 7
    default_line_height = 20

    def __init__(self, text, line_height=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._line_height = line_height
        try:
            _ = iter(text)
        except TypeError:
            text = [text]
        self.text = text

    @property
    def height(self):
        return len(self.text) * self.line_height

    @property
    def line_height(self):
        return (
            self._line_height
            if self._line_height is not None
            else self.default_line_height
        )

    @line_height.setter
    def line_height(self, value):
        self._line_height = value

    def render(self):
        return svg_textblock.render(
            text=self.text,
            line_height=self.line_height,
            tags=("textblock " + self.tags).strip(),
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            scale=self.scale,
        )


#####################################################################
# Composite classes


class Label(Element):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text

    def render(self):
        return svg_label.render(
            text=self.text,
            tags=self.tags,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            scale=self.scale,
        )


class LeaderLine(Component):
    def __init__(self, offset=(0, 0), *args, **kwargs):
        """Draws a line from *offset* to the component's (x, y) location.

        :param offset: The (x, y) coordinates the leaderline is drawn from
        :type offset: tuple
        """

        super().__init__(*args, **kwargs)

        offset = self.extract_scale(offset)

        # Add Path to children
        self.add(
            Line(
                width=abs(offset[0]),
                height=abs(offset[1]),
            ),
        )


class PinLabel(Component):
    def __init__(
        self,
        text,
        offset=cfg["pinlabel"]["offset"],
        box_width=cfg["pinlabel"]["box_width"],
        box_height=cfg["pinlabel"]["box_height"],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.tags = ("pinlabel " + self.tags).strip()

        offset = self.extract_scale(offset)

        line_scale = (-self.scale.x, -self.scale.y)

        self.add(
            [
                Line(width=offset.x, height=offset.y),
                Label(
                    text=text,
                    x=offset.x,
                    y=offset.y,
                    width=box_width,
                    height=box_height,
                    scale=self.scale,
                ),
            ]
        )


class PinLabelRow(Component):
    def __init__(self, offset=(85, 0), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = self.extract_scale(offset)
        self.tags = ("pinlabelrow " + self.tags).strip()
        self.labels = Component(x=offset[0], y=offset[1], scale=self.scale)

        self.children = [
            LeaderLine(offset=offset, scale=self.scale),
            self.labels,
        ]

    def add(self, label_list):
        for i, label in enumerate(label_list):
            context = dict(zip(("text", "tags", "offset", "box_width"), label))
            # Remove 'na' entries - they fall-back to default settings
            context = {
                key: val
                for key, val in context.items()
                if val not in [None, "auto", "defalut", "", "-", "na"]
            }

            # Conditionally set offset if none supplied (first label has no leaderline)
            if i == 0:
                context["offset"] = context.get("offset", (0, 0))

            # Add PinLabel to label_row
            label_x = self.labels.width * self.scale.x
            self.labels.add(PinLabel(**context, x=label_x, scale=self.scale))


class PinLabelSet(Component):
    def __init__(self, pitch, offset, labels, *args, **kwargs):
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

            label_row = PinLabelRow(x=pin_x, y=pin_y, offset=row_offset, tags="plr")
            label_row.add(label_list)

            self.add(label_row)
