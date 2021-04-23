Elements
========


class Element(SVG):
"""Container that exclusively handles graphical SVG code. Elements can be considered the smallest building blocks of *pinout*.

:param width: Width of the renderable SVG code, defaults to 0
:type width: int, optional
:param height: Height of the renderable SVG code, defaults to 0
:type height: int, optional
"""

bounding_coords
---------------
Coordinates, relative to its parent, representing sides of a rectangle that encompass the rendered element.

:return: (x_min, y_min, x_max, y_max)
:rtype: tuple


bounding_rect
-------------

Coordinates representing the location of an elements origin (usually top-left corner) within its parent along with the elements width and height.

:return: (x, y, width, height)
:rtype: tuple


class Image(Element):
    def __init__(self, href, embed=False, *args, **kwargs):
Associate a PNG, JPG or SVG formatted image to the diagram. *IMPORTANT*: Image width and height parameters must be supplied for the image to display! *pinout* does not auto-detect these attributes.

        :param href: Location of the image. *Note*: Where :code:`embed=False` the path is relative to the exported file. Where :code:`embed=True` the path is relative to the current working directory.
        :type path: string
        :param embed: Embed or link the image in the exported file, defaults to False
        :type embed: bool, optional

        
    def bounding_coords(self):
    Coordinates, relative to its parent, representing sides of a rectangle that encompass the image.

        :return: (x_min, y_min, x_max, y_max)
        :rtype: tuple


    def render(self):
Generates SVG <image> tag using the image 'filename', Note that JPG and PNG are the only binary images files officially supported by the SVG format. If 'embed' is True the image is assigned to the path as a data URI. JPG and PNG image are base64 encoded, SVG files included verbatim. Otherwise the path 'src' is assigned 'filename'. Note: 'filename' includes the path to the file. Where a relative path is used it must be relative to the **exported file**.

        :return: SVG <image> component
        :rtype: str


class Rect(Element):
    """SVG <rect> (rectangle) element."""


    def render(self):
create an SVG <rect> tag.

        :return: SVG <rect> code
        :rtype: string


class Line(Element):
    """Create an SVG <path> tag with (at most) a single 90deg bend in it. The design of this Element is soley for use as a leader line with pin labels.

    :return: SVG <path> code
    :rtype: string
    """

    def render(self):
create an SVG <path> tag.

        :return: SVG <path> code
        :rtype: string



class SVGPath(Element):
    """Create as SVG path tag.
    *NOTE*: If the path forms part of the diagram bounding box a width and height must be **explicitly** passed to it for final dimensions to be calculated correctly.
    """


class Text(Element):
    """Create an SVG <text> tag with a single line of text.

    :return: SVG <text> code
    :rtype: string
    """

    def render(self):
create an SVG <text> tag.

        :return: SVG <text> code
        :rtype: string



class Label(Element):
"""A single line of text infront of a rectangle. *Note*: Text length is not auto-detected and the element's width should be set to ensure text will not overflow the rectangle in the final diagram export.

:param text: Text to appear on the label
:type text: string
"""

def render(self):
create an SVG <group> tag that includes text and an rectangle.

    :return: SVG <group> code
    :rtype: string