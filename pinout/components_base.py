
import math
from pathlib import Path
from collections import namedtuple
from .templates import svg, svg_group, svg_image, svg_legend, svg_style, svg_leaderline, svg_label, svg_textblock, svg_rect


BoundingBox = namedtuple('BoundingBox',('x y w h'))
BoundingCoords = namedtuple('BoundingCoords',('x1 y1 x2 y2'))
Coords = namedtuple('Coords',('x y'))


#####################################################################
# Base Element and Component classes

class ClassMethodMissing(Exception):
    """ An element is missing an expected method """
    pass


class Element:

    default_width = 10
    default_height = 10

    def __init__(self, x=0, y=0, width=None, height=None, scale=(1,1), rotation=0, tags=''):
        self.x = x
        self.y = y
        self._width = width
        self._height = height
        self._scale = scale if isinstance(scale, Coords) else Coords(*scale)
        self.rotation = rotation
        self.tags = tags

    @property
    def width(self):
        return self._width if self._width != None else self.default_width

    @width.setter
    def width(self, value):
        self._width = value
    
    @property
    def height(self):
        return self._height if self._height != None else self.default_height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, coords):
        coords = coords if isinstance(coords, Coords) else Coords(*coords)
        self._scale = coords
        try:
            for c in self.children:
                c.scale = Coords(c.scale.x * coords.x, c.scale.y * coords.y)
        except AttributeError:
            """ No children to update """   

    @property
    def bounding_coords(self):
        x_min, x_max = sorted([self.x * self.scale.x, (self.x + self.width) * self.scale.x])
        y_min, y_max = sorted([self.y * self.scale.y, (self.y + self.height) * self.scale.y])
        return BoundingCoords(x_min, y_min, x_max, y_max)

    @property
    def bounding_rect(self):
        x1, y1, x2, y2 = self.bounding_coords
        return BoundingBox(x1, y1, x2-x1, y2-y1)

    def render(self):
        raise ClassMethodMissing(f"{self} requires a 'render' method.")
        """ Return a string of valid SVG markup."""


class Component(Element):
    """Container object that manages groups of child objects. All children must include a render and bounding_coords functions.
    """
    def __init__(self, children=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = []
        if children:
            self.add(children)

    @property
    def bounding_coords(self):
        # Untransformed bounding coords
        x1 = self.x + min([c.bounding_coords.x1 for c in self.children])
        y1 = self.y + min([c.bounding_coords.y1 for c in self.children])
        x2 = self.x + max([c.bounding_coords.x2 for c in self.children])
        y2 = self.y + max([c.bounding_coords.y2 for c in self.children])
        return BoundingCoords(x1, y1, x2, y2)

    @property
    def width(self):
        x1, y1, x2, y2 = self.bounding_coords
        return x2 - x1

    @property
    def height(self):
        x1, y1, x2, y2 = self.bounding_coords
        return y2 - y1

    @property
    def bounding_rect(self):
        x1, y1, x2, y2 = self.bounding_coords
        return BoundingBox(x1, y1, x2-x1, y2-y1)

    def add(self, children):
        try:
            iterator = iter(children)
        except TypeError:
            children = [children]
        for c in children:
            self.children.append(c)
            c.scale = Coords(c.scale.x * self.scale.x, c.scale.y * self.scale.y)

    def render(self):
        output = ''
        for c in self.children:
            output += c.render()
        return svg_group.render(
            x = self.x,
            y = self.y,
            tags = self.tags,
            content = output,
            scale = self.scale,
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
            context['css_data'] = p.read_text()
        else:
            context['path'] = self.path
        
        return svg_style.render(**context)

#####################################################################
# User classes

class Label(Element):

    default_width = 70
    default_height = 30

    def __init__(self, text ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text

    def render(self):
        return svg_label.render(
            text = self.text,
            tags = self.tags,
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            scale = self.scale
        )

class TextBlock(Element):

    default_width = 7
    default_line_height = 20

    def __init__(self, text, line_height=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._line_height = line_height
        try:
            iterator = iter(text)
        except TypeError:
            text = [text]
        self.text = text

    @property
    def height(self):
        return len(self.text) * self.line_height

    @property
    def line_height(self):
        return self._line_height if self._line_height != None else self.default_line_height

    @line_height.setter
    def line_height(self, value):
        self._line_height = value

    def render(self):
        return svg_textblock.render(
            text = self.text,
            line_height = self.line_height,
            tags = ('textblock ' + self.tags).strip(),
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            scale = self.scale,
        )


class LeaderLine(Element):
    
    def __init__(self, route, *args, **kwargs):
        """[summary]

        :param route: Type of line to render. options are 'h' - horizontal line, and 'hv' - line a single bend 
        :type route: str
        """
        super().__init__(*args, **kwargs)
        self.route = route

    @property
    def width(self):
        return abs(self.x)

    @property
    def height(self):
        return abs(self.y)

    @property
    def bounding_coords(self):
        x1, x2 = sorted([0, self.x * self.scale.x])
        y1, y2 = sorted([0, self.y * self.scale.y])
        return BoundingCoords(x1, y1, x2, y2)

    def render(self):
        if self.route in ['HV', 'hv']:
            # Vertical then horizontal leader line
            d = f'M 0 0 H {self.x * self.scale.x} V {self.y * self.scale.y}'
        else:
            # Straight line (default)
            d = f'M 0 0 L {self.x * self.scale.x} {self.y * self.scale.y}'

        return svg_leaderline.render(
            d = d,
            tags = ('leaderline ' + self.tags).strip(),
        )


class Image(Element):
    
    def __init__(self, href, embed=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.href = href
        self.embed = embed

    @property
    def bounding_coords(self):
        x_min, x_max = sorted([self.x * self.scale.x, (self.x + self.width) * self.scale.x])
        y_min, y_max = sorted([self.y * self.scale.y, (self.y + self.height) * self.scale.y])
        return BoundingCoords(x_min, y_min, x_max, y_max)

    def render(self):
        """Generates SVG <image> tag using the image 'filename', Note that JPG and PNG are the only binary images files officially supported by the SVG format. If 'embed' is True the image is assigned to the path as a data URI. JPG and PNG image are base64 encoded, SVG files included verbatim. Otherwise the path 'src' is assigned 'filename'. Note: 'filename' includes the path to the file. Where a relative path is used it must be relative to the **exported file**.   

        :return: SVG <image> component
        :rtype: str
        """
        media_type = Path(self.href).suffix[1:]
        path = Path(self.href)
        if self.embed:
            if media_type == 'svg':
                with path.open() as f:
                    svg_data = f.read()
                return svg_group.render(
                    x = self.x,
                    y = self.y,
                    content = svg_data
                )
            else:
                encoded_img = base64.b64encode(open(self.href, "rb").read())
                path = 'data:image/{};base64,{}'.format(media_type, encoded_img.decode('utf-8'))

        return svg_image.render(
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            href = path
        )

class Rect(Element):
    
    def __init__(self, rx=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rx = rx

    def render(self):
        return svg_rect.render(
            rx = self.rx,
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            scale = self.scale,
            tags = self.tags,
        )