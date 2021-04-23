# Elements
# Base building blocks to create SVG components
import base64
import pathlib
from collections import namedtuple
from .templates import (
    svg_group,
    svg_image,
    svg_label,
    svg_path,
    svg_rect,
    svg_text,
)


BoundingBox = namedtuple("BoundingBox", ("x y w h"))
BoundingCoords = namedtuple("BoundingCoords", ("x_min y_min x_max y_max"))
Coords = namedtuple("Coords", ("x y"))


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
        media_type = pathlib.Path(self.href).suffix[1:]
        path = pathlib.Path(self.href)
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


class Path(Element):
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