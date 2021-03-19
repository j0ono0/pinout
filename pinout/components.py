import base64
from pathlib import Path
from collections import namedtuple
from .templates import svg_pin_label, svg_group, svg_image, svg_legend, svg_style


_BoundingBox = namedtuple('_BoundingBox',('x y w h'))
_Rect = namedtuple('_Rect',['x','y','w','h','r'])
_Line = namedtuple('_Line',('x1','x2','y1','y2'))



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
    :param pad: Blank space between the leader-line and proceeding label or pin location.
    :type pad: int
    """
    
    #:Default label box width.
    default_width = 70

    #:Default label box height.
    default_height = 25

    #:Default label gap.
    default_gap = 5

    #:Default label box corner-radius.
    default_cnr = 2

    #:Default label box pad.
    default_pad = 1

    def __init__(self, name, tags, width=None, height=None, gap=None, cnr=None, pad=None):
        """ Constructor method
        """
        self.name = name
        self.tags = tags.strip()
        self.width = width
        self.height = height
        self.gap = gap
        self.cnr = cnr
        self.pad = pad


class Pin:
    def __init__(self, x, y, direction='right', label_tuples=None):
        """Each Pin documents a location in the diagram and manages position and rendering of labels associated to it.

        :param x: Location of the pin on the x axis 
        :type x: int
        :param y: location of the pin on the y axis
        :type y: int
        :param direction: Specify which direction labels are to be aligned from the pin location. Valid values are 'left' and 'right'. Defaults to 'right'.
        :type direction: str, optional
        :param label_tuples: A list of tuples can be supplied to streamline the pin and label creation process into a single step. Each tuple must represent the required arguments of Pin.add_label(). Defaults to None
        :type label_tuples: List, optional
        """
        self.x = x
        self.y = y
        self.labels = []
        self.direction = direction

        if label_tuples:
            for label in label_tuples:
                self.add_label(*label)
    
    def add_label(self, name, tags=None, width=None, height=None, gap=None):
        """Add a label to the pin. This is the recommended method of creating labels.

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
        return sum([label.width + label.gap for label in self.labels])

    @property
    def height(self):
        """Each label associated with a pin can have its height independently set. The overall height of the pin is thus dictated by its tallest labels.

        :return: Height of the tallest label.
        :rtype: int
        """
        try:
            return max([label.height for label in self.labels])
        except ValueError:
            return 0

    @property
    def bounding_box(self):
        """Calculate a rectangular box that documents the bounds and location the rendered object 

        :return: namedTuple documenting x, y, width, and height.
        :rtype: diagram._BoundingBox
        """
        if self.direction == 'right':
            # labels sit right of pin
            x = self.x
        else:
            # labels sit left of pin
            x = self.x - self.width

        return _BoundingBox(x, self.y - self.height/2, self.width, self.height)

    def render(self):
        """Generates SVG tags of all associated labels.

        :return: SVG components
        :rtype: str
        """
        offset_x = 0
        output = ''
        
        for label in self.labels:

            # Update unset properties with defaults
            label.width = label.width or label.default_width
            label.height = label.height or label.default_height
            label.gap = label.gap or label.default_gap       
            label.cnr = label.cnr or label.default_cnr
            label.pad = label.pad or label.default_pad

            tags = ('label ' + label.tags).strip()
            
            if self.direction == 'right':
                # RHS label
                output += svg_pin_label.render(
                    x = offset_x,
                    y = -label.height/2,
                    line = _Line(label.pad, label.gap, label.height//2, label.height//2),
                    box = _Rect(label.gap, 0, label.width, label.height, label.cnr),
                    text = label.name,
                    selectors = tags
                )
            else:
                # LHS label
                output += svg_pin_label.render(
                    x = (label.width + label.gap + offset_x) * -1,
                    y = label.height / 2 * -1,
                    line = _Line(label.width, label.width + label.gap - label.pad, label.height//2, label.height//2),
                    box = _Rect(0, 0, label.width, label.height, label.cnr),
                    text = label.name,
                    selectors = tags
                )
            offset_x += label.width + label.gap
        
        return  svg_group.render(
            x = self.x,
            y = self.y,
            content = output
        )


class Image:
    def __init__(self, x, y, width, height, filename, embed=False):
        """Include an image in the diagram.

        :param x: Location of the image on the x axis
        :type x: int
        :param y: Location of the image on the y axis
        :type y: int
        :param width: Width of image in the diagram (may differ from actual image width)
        :type width: int
        :param height: Height of the image in the diagram (may differ from actual image height)
        :type height: int
        :param filename: Filename, including path, to the image. Relative paths are relative to the current working directory.
        :type filename: string
        :param embed: Elect to link or embed an external image. Embedded images are base64 encoded. Default to False.
        :type embed: bool
        """
        self.x = x
        self.y = y
        self.path = filename
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
        """Generates SVG <image> tag using the image 'filename'. If 'embed' is True the image is base64 encoded and assigned to the path as data. Otherwise the path is assigned 'filename'

        :return: SVG <image> component
        :rtype: str
        """

        if self.embed:
            media_type = self.path.split('.')[-1]
            encoded_img = base64.b64encode(open(self.path, "rb").read())
            path = 'data:image/{};base64,'.format(media_type) + encoded_img.decode('utf-8')
        else:
            path = self.path

        return svg_image.render(
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            path = path
        )

    def render_base64(self):
        """Generates SVG <image> tag **embedding** the image 'filename' as base64 encoded data. This feature assumes images have a predictable suffix indicating the file type.

        :return: SVG <image> component
        :rtype: str
        """

        media_type = self.path.split('.')[-1]
        encoded_img = base64.b64encode(open(self.path, "rb").read())
        
        return svg_image.render(
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            path = 'data:image/{};base64,'.format(media_type) + encoded_img.decode('utf-8')
        )


class StyleSheet:
        def __init__(self, filepath, embed=False):
            """Include a stylesheet in the diagram

            :param filepath: Location of the external stylesheet. *NOTE*: If enbedding, a relative filepath is relative to the current working directory. If linking, a relative filepath is relative to the location of the final SVG diagram. 
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
            swatch = Pin(0, 0, 'left', [('', tags, 20, 20, 5)])
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
