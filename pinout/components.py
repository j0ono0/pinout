import base64
from collections import namedtuple
from pathlib import Path

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
        x_min = self.x + min(
            [
                child.bounding_coords.x_min
                for child in self.children
                if hasattr(child, "bounding_coords")
            ]
        )
        y_min = self.y + min(
            [
                child.bounding_coords.y_min
                for child in self.children
                if hasattr(child, "bounding_coords")
            ]
        )
        x_max = self.x + max(
            [
                child.bounding_coords.x_max
                for child in self.children
                if hasattr(child, "bounding_coords")
            ]
        )
        y_max = self.y + max(
            [
                child.bounding_coords.y_max
                for child in self.children
                if hasattr(child, "bounding_coords")
            ]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

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

    default_width = 70
    default_height = 30

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
    def __init__(self, origin, *args, **kwargs):
        """Draws a line from *origin* to the component's (x, y) location.

        :param origin: The (x, y) coordinates the leaderline is drawn from
        :type origin: tuple
        """

        super().__init__(*args, **kwargs)

        # If a negative value is in 'origin' override scale with deduced values from offset.
        # then set offset to positive values.
        if not all(val >= 0 for val in origin):
            self.scale = Coords(*[i / abs(i) if i != 0 else 1 for i in origin])

        line_x = abs(origin[0])
        line_y = abs(origin[1])

        # Add Path to children
        self.add(Line(width=line_x, height=line_y, scale=self.scale))


class PinLabel(Component):
    def __init__(self, text, offset=(15, 0), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = ("pinlabel " + self.tags).strip()

        # If a negative value is in 'offset' override scale with deduced values from offset.
        # then set offset to positive values.
        if not all(val >= 0 for val in offset):
            self.scale = Coords(*[i / abs(i) if i != 0 else 1 for i in offset])
        offset = Coords(*[abs(i) for i in offset])

        # Deduce route from scale
        if offset.x == 0:
            route = "v"
        elif offset.y == 0:
            route = "h"
        else:
            route = "vh"

        self.children = [
            Line(width=offset.x, height=offset.y, scale=self.scale),
            Label(
                text=text, x=offset.x, y=offset.y, width=70, height=28, scale=self.scale
            ),
        ]
