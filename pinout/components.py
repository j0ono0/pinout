import base64
from itertools import zip_longest
from pathlib import Path
from collections import namedtuple
from .templates import svg_group, svg_image, svg_legend, svg_style, svg_label, svg_pin


_BoundingBox = namedtuple('_BoundingBox',('x y w h'))
_Rect = namedtuple('_Rect',['x','y','w','h','r'])
_Line = namedtuple('_Line',('x1','x2','y1','y2'))
_Coords = namedtuple('_Coords',('x y'))



class Label:
    """Create an individual label. Labels must be associated to a Pin to be located and rendered in the final diagram. Pin.add_label() is the recommended method of creating labels.

    :param name: Text that appear on the label.
    :type name: str
    :param tags: Applied to the label as css class selector(s). Multiple tags can be included as a space separated list.
    :type name: str
    :param width: Width of the label rectangle.
    :type width: int
    :param height: Height of the label rectangle.
    :type height: int
    :param gap: Space between the label rectangle and proceeding label or pin location. The gap contains a graphical 'leader-line'.
    :type gap: int
    :param cnr: Corner radius or teh label rectangle.
    :type cnr: int
    """
    
    #:Default label box width.
    default_width = 70

    #:Default label box height.
    default_height = 25

    #:Default label gap.
    default_gap = 5

    #:Default label box corner-radius.
    default_cnr = 2

    def __init__(self, name, tags, width=None, height=None, gap=None, cnr=None):
        """ Constructor method
        """
        self.name = name
        self.tags = tags.strip()
        self._width = width
        self._height = height
        self._gap = gap
        self._cnr = cnr

    @property
    def width(self):
        return self._width or Label.default_width

    @property
    def height(self):
        return self._height or Label.default_height

    @property
    def gap(self):
        return self._gap or Label.default_gap

    @property
    def cnr(self):
        return self._cnr or Label.default_cnr


class Pin:
    def __init__(self, pin_x, pin_y, label_x=None, label_y=None, label_tuples=None):
        """Each Pin documents a location in the diagram and manages position and rendering of labels associated to it.

        :param pin_x: Location of the pin on the x axis 
        :type pin_x: int
        :param pin_y: location of the pin on the y axis
        :type pin_y: int
        :param label_x: X coordinate of the labels relative to the diagram's (0,0) coordinate.
        :type label_x: int
        :param label_y: Y coordinate of the labels relative to the diagram's (0,0) coordinate
        :type label_y: int
        :param label_tuples: A list of tuples can be supplied to streamline the pin and label creation process into a single step. Each tuple must represent the required arguments of Pin.add_label(). Defaults to None
        :type label_tuples: List, optional
        """
        self.pin_coords = _Coords(pin_x, pin_y)
        # Label_coords relative to pin_coords
        self.label_coords = _Coords(label_x - pin_x, label_y - pin_y) 
        self.labels = []
        if label_tuples:
            for label in label_tuples:
                self.add_label(*label)
    
    def add_label(self, name, tags=None, width=None, height=None, gap=None):
        """Add a label to the pin.

        :param name: Text that appear on the label
        :type name: str
        :param tags: Applied to the label as css class selector(s). Multiple tags can be included as a space separated list, defaults to None
        :type tags: str, optional
        :param width: Width of the label rectangle.
        :type width: int
        :param height: Height of the label rectangle.
        :type height: int
        :param gap: Space between the label rectangle and proceeding label or pin location. The gap contains a graphical 'leader-line'.
        :type gap: int
        """
        self.labels.append(Label(name, tags, width, height, gap))
    
    @property
    def width(self):
        """The total width of each pin is determined by the collective widths of all labels associated with the pin.

        :return: Sum of all label widths
        :rtype: int
        """       
        return sum([label.width for label in self.labels]) + sum([label.gap for label in self.labels[:-1]]) + abs(self.label_coords.x)

    @property
    def height(self):
        """Each label associated with a pin can have its height independently set. The overall height of the pin is thus dictated by its tallest labels.

        :return: Height of the tallest label.
        :rtype: int
        """
        return abs(self.label_coords.y) + max([label.height or Label.default_height for label in self.labels]) - self.tallest_label / 2

    @property
    def tallest_label(self):
        """Finds and returns the height of the tallest label associated with a pin.

        :return: Height of the tallest label.
        :rtype: int
        """
        return max([l.height for l in self.labels])

    @property
    def bounding_box(self):
        """Calculate a rectangular box that documents the bounds and location the rendered object 

        :return: namedTuple documenting x, y, width, and height.
        :rtype: diagram._BoundingBox
        """
        if self.label_coords.x > 0:
            # labels located right of pin
            x = self.pin_coords.x
        else:
            # labels located left of pin
            x = self.pin_coords.x - self.width

        if self.label_coords.y > 0:
            # labels located below pin
            y = self.pin_coords.y
        else:
            # labels located above pin
            y = self.pin_coords.y + self.label_coords.y - self.tallest_label / 2

        return _BoundingBox(x, y, self.width, self.height)
        

    def render(self):
        """Generates SVG tags of all associated labels.

        :return: SVG components
        :rtype: str
        """
        output = ''
        for i, label in enumerate(self.labels):
            tags = ('label ' + label.tags).strip()
            
            offset = sum(l.width + l.gap for l in self.labels[:i])
            output += svg_label.render(
                selectors = ' '.join(['label', label.tags]),
                leaderline_class = label.tags.split(' ')[0],
                label = label,
                offset = offset,
                flip = self.label_coords.x < 0,
            )
            
        return  svg_pin.render(
            x = self.pin_coords.x,
            y = self.pin_coords.y,
            label_coords = self.label_coords,
            leaderline = f'M 0 0 V {self.label_coords.y} H {self.label_coords.x}',
            leaderline_class = self.labels[0].tags.split(' ')[0],
            flip = self.label_coords.x < 0,
            content = output,
            selectors = 'pin'
        )


class Image:
    def __init__(self, x, y, width, height, filepath, embed=False):
        """Include an image in the diagram.

        :param x: Location of the image on the x axis
        :type x: int
        :param y: Location of the image on the y axis
        :type y: int
        :param width: Width of image in the diagram (may differ from actual image width)
        :type width: int
        :param height: Height of the image in the diagram (may differ from actual image height)
        :type height: int
        :param filepath: Filename, including path, to the image. Relative paths are relative to the current working directory.
        :type filepath: string
        :param embed: Elect to link or embed an external image. Embedded images are base64 encoded. Default to False.
        :type embed: bool
        """
        self.x = x
        self.y = y
        self.path = filepath
        self.width = width
        self.height = height
        self.embed = embed

    @property
    def bounding_box(self):
        """Calculate a rectangular box that documents the bounds and location the rendered object 

        :return: namedTuple documenting x, y, width, and height.
        :rtype: diagram._BoundingBox
        """
        return _BoundingBox(self.x, self.y, self.width, self.height)
    
    def render(self):
        """Generates SVG <image> tag using the image 'filename', Note that JPG and PNG are the only binary images files officially supported by the SVG format. If 'embed' is True the image is assigned to the path as a data URI. JPG and PNG image are base64 encoded, SVG files included verbatim. Otherwise the path 'src' is assigned 'filename'. Note: 'filename' includes the path to the file. Where a relative path is used it must be relative to the **exported file**.   

        :return: SVG <image> component
        :rtype: str
        """
        media_type = Path(self.path).suffix[1:]

        if self.embed:
            if media_type == 'svg':
                filepath = Path(self.path)
                with filepath.open() as f:
                    svg_data = f.read()
                return svg_group.render(
                    x = self.x,
                    y = self.y,
                    content = svg_data
                )
            else:
                encoded_img = base64.b64encode(open(self.path, "rb").read())
                path = 'data:image/{};base64,{}'.format(media_type, encoded_img.decode('utf-8'))
        else:
            path = self.path

        return svg_image.render(
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            path = path
        )


class StyleSheet:
        def __init__(self, filepath, embed=False):
            """Include a stylesheet in the diagram

            :param filepath: Filename, including path, of the external stylesheet. *NOTE*: If *embedding*, a relative filepath is relative to the current working directory. If *linking*, a relative filepath is relative to the location of the final SVG diagram. 
            :type filepath: str
            :param embed: Elect to link or embed the stylesheet, defaults to False
            :type embed: bool, optional
            """
            self.filepath = filepath
            self.embed = embed

        def render(self):
            context = {}
            if self.embed:
                p = Path(self.filepath)
                context['css_data'] = p.read_text()
            else:
                context['filepath'] = self.filepath
            
            return svg_style.render(**context)


class Legend:

    ITEM_HEIGHT = 20
    ITEM_PAD = 4
    TEXT_PAD = 5
    SWATCH_PAD = 5
    INSET = 20

    def __init__(self, x, y, width, tags='', items=None):
        self.x = x
        self.y = y
        self.width = width
        self.items = items or []
        self.tags = tags
    
    @property
    def height(self):
        """Legend overall height (calculated dynamically).

        :return: Number of entries * preset item height
        :rtype: int
        """
        return len(self.items) * (self.ITEM_HEIGHT + self.ITEM_PAD) - self.ITEM_PAD + 2 * self.INSET

    @property
    def bounding_box(self):
        """Calculate a rectangular box that documents the bounds and location the rendered object 

        :return: namedTuple documenting x, y, width, and height.
        :rtype: diagram._BoundingBox
        """
        return _BoundingBox(self.x, self.y, self.width, self.height)

    def render(self):
        """Generates SVG code of the legend.

        :return: SVG legend component
        :rtype: str
        """
        # Parse user submitted item data
        items = []
        keys = ['name','tags','color']
        for i, values in enumerate(self.items):
            # Ensure values are a list (ie not a single item in a tuple)
            if isinstance(values, str):
                values = [values]

            item = dict(zip_longest(keys, values, fillvalue=''))
            
            # Create a pin and blank label as a 'swatch' for each item
            tags = ('swatch ' + item['tags']).strip()
            swatch = Pin(0, 0, -1, 0, [('', tags, 20, 20, 5)])
            item['swatch'] = swatch.render()

            item['x'] = swatch.width + self.INSET
            item['y'] = i * (self.ITEM_HEIGHT + self.ITEM_PAD) + (self.ITEM_HEIGHT / 2) + self.INSET
            items.append(item)
            

        return svg_legend.render(
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            text_pad = self.TEXT_PAD,
            items = items,
            selectors = self.tags
        )
