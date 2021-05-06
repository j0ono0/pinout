""" Elements: Basic building blocks for pinout diagrams
"""

# Elements
# Base building blocks to create SVG components
import base64
import pathlib
import uuid
from collections import namedtuple
from .templates import (
    svg_group,
    svg_image,
    svg_label,
    svg_path,
    svg_rect,
    svg_text,
    svg_textblock,
)


BoundingBox = namedtuple("BoundingBox", ("x y w h"))
BoundingCoords = namedtuple("BoundingCoords", ("x_min y_min x_max y_max"))
Coords = namedtuple("Coords", ("x y"))


class ClassMethodMissing(Exception):
    """ An element is missing an expected method """

    pass


class SVG:
    """Common base for all SVG entities that ultimately have a graphical representation.

    :param x: Coordinate position in the 'x' direction, defaults to 0
    :type x: int, optional
    :param y: Coordinate position in the 'y' direction, defaults to 0
    :type y: int, optional
    :param scale: Primarily used to define direction of width, height, and coordinates, from an origin. Defaults to (1, 1)
    :type scale: tuple, optional
    :param rotation:  (***Currently NOT implemented***) Rotation around an origin, defaults to 0
    :type rotation: int, optional
    :param tag: Associate an entity for application of predefined attributes/styles, defaults to ""
    :type tag: str, optional
    :param config: Directly supply attributes to an entity. Alternative to assigning via 'tag' or in the default config. Defaults to None
    :type config: dict, optional
    """

    def __init__(self, x=0, y=0, scale=(1, 1), rotation=0, tag="", config=None):
        """Create a new SVG object."""
        self.config = config
        self.rotation = rotation
        self._scale = Coords(*scale)
        self.tag = tag
        self.x = x
        self.y = y

    @property
    def scale(self):
        """Tuple representing orientation of entity."""
        # NOTE: set here as a property for override by Component
        return self._scale

    @scale.setter
    def scale(self, value):
        """Scale setter property - overridden by Component

        :param value: (x, y) where x and y are either 1 or -1
        :type value: tuple
        """
        # NOTE: set here for override by Component
        self._scale = value

    @staticmethod
    def extract_scale(coords):
        """Separate and scale information from *coords*.

        :param coords: (x, y) coordinates or (width, height) dimensions.
        :type coords: tuple
        :return: 'coords' parameter with absolute values and scale Coords.
        :rtype: (Coords, Coords), namedtuples
        """

        scale = Coords(*[i / abs(i) if i != 0 else 1 for i in coords])
        abs_coords = Coords(*[abs(i) for i in coords])
        return (abs_coords, scale)


class Element(SVG):
    """Fundamental building blocks that render SVG markup.

    :param width: Width of the rendered element, defaults to 0
    :type width: int, optional
    :param height: Height of the rendered element, defaults to 0
    :type height: int, optional

    """

    def __init__(self, width=0, height=0, *args, **kwargs):
        """Create a new Element"""
        self.width = width
        self.height = height
        super().__init__(*args, **kwargs)

    @property
    def bounding_coords(self):
        """Coordinates of the element's bounding rectangle.

        :return: (x_min, y_min, x_max, y_max)
        :rtype: BoundingCoords (namedtuple)
        """
        x_min, x_max = sorted(
            [self.x * self.scale.x, (self.x + self.width) * self.scale.x]
        )
        y_min, y_max = sorted(
            [self.y * self.scale.y, (self.y + self.height) * self.scale.y]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

    @property
    def bounding_rect(self):
        """Element's coordinates and size.

        :return: (x, y, width, height)
        :rtype: BoundingBox (namedtuple)
        """
        x_min, y_min, x_max, y_max = self.bounding_coords
        return BoundingBox(x_min, y_min, x_max - x_min, y_max - y_min)

    def render(self):
        """Create SVG markup of the element"""
        raise ClassMethodMissing(f"{self} requires a 'render' method.")


class Image(Element):
    """Associate a PNG, JPG or SVG formatted image to the diagram.

    :param href: path to image
    :type href: string
    :param embed: Embed image in rendered SVG file, defaults to False
    :type embed: bool, optional
    """

    def __init__(self, href, embed=False, *args, **kwargs):
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
        """Render SVG markup either linking or embedding an image.

        :return: SVG markup
        :rtype: string
        """
        media_type = pathlib.Path(self.href).suffix[1:]
        path = pathlib.Path(self.href)
        if self.embed:
            if media_type == "svg":
                with path.open() as f:
                    svg_data = f.read()
                # Extract JUST the <svg> markup with no <XML> tag
                import xml.etree.ElementTree as ET

                tree = ET.fromstring(svg_data)
                just_svg_tag = ET.tostring(tree)
                return svg_group.render(
                    x=self.x, y=self.y, scale=self.scale, content=just_svg_tag
                )
            else:
                encoded_img = base64.b64encode(open(self.href, "rb").read())
                path = f"data:image/{media_type};base64,{encoded_img.decode('utf-8')}"

        return svg_image.render(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            href=path,
        )


class Rect(Element):
    """SVG <rect> (rectangle) element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self):
        """Return SVG markup

        :return: SVG markup
        :rtype: string
        """
        return svg_rect.render(
            x=self.x,
            y=self.y,
            scale=self.scale,
            uid=uuid.uuid1(),
            **self.config,
        )


class Path(Element):
    """SVG <path> element"""

    def __init__(self, definition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.definition = definition

    def render(self):
        return svg_path.render(d=self.definition, scale=self.scale, **self.config)


class Text(Element):
    """SVG <text> element."""

    def __init__(self, text_content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_content = text_content

    def render(self):
        """create an SVG <text> tag."""
        return svg_text.render(
            text_content=self.text_content,
            x=self.x,
            y=self.y,
            scale=self.scale,
            **self.config,
        )


class TextBlock(Element):
    """SVG <text> element."""

    def __init__(self, text_content, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if type(text_content) == str:
            # attempt to split on '\n' to make a list
            text_content = text_content.split("\n")

        self.text_content = text_content

    def render(self):
        """create an SVG <text> tag."""
        return svg_textblock.render(
            text_content=self.text_content,
            x=self.x,
            y=self.y,
            scale=self.scale,
            **self.config,
        )


class Label(Element):
    """SVG <text> and <rect> markup in a single element."""

    def __init__(self, text_content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_content = text_content
        self.width = self.config["rect"]["width"]
        self.height = self.config["rect"]["height"]

    def render(self):
        """Render SVG component."""
        return svg_label.render(
            text_content=self.text_content,
            x=self.x,
            y=self.y,
            scale=self.scale,
            **self.config,
        )
