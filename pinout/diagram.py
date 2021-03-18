import os
from pathlib import Path
from collections import namedtuple
from itertools import zip_longest
from .templates import svg_pin_label, svg_group, svg_image, svg_legend, svg

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
    def __init__(self, x, y, width, height, filename):
        """Include an image in the diagram.

        :param x: Location of the image on the x axis
        :type x: int
        :param y: Location of the image on the y axis
        :type y: int
        :param width: Width of image in the diagram (may differ from actual image width)
        :type width: int
        :param height: Height of the image in the diagram (may differ from actual image height)
        :type height: int
        :param filename: Filename, including path, to the image.
        :type filename: string
        """
        self.x = x
        self.y = y
        self.path = filename
        self.width = width
        self.height = height

    @property
    def bounding_box(self):
        """Calculate a rectangular box that documents the bounds and location the rendered object 

        :return: namedTuple documenting x, y, width, and height.
        :rtype: diagram._BoundingBox
        """
        return _BoundingBox(self.x, self.y, self.width, self.height)
    
    def render(self):
        """Generates and SVG <image> tag linking to the image 'filename'.

        :return: SVG <image> component
        :rtype: str
        """
        return svg_image.render(
            x = self.x,
            y = self.y,
            width = self.width,
            height = self.height,
            path = self.path
        )


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
    

class Diagram:
    """Components are collated and the final diagram is exported with this class. A typical diagram will include an image, pins with labels, and a stylesheet.
    """
    def __init__(self):
        self.components = []
        self.stylesheets = []
        self._rendered = ''

    def add_image(self, x, y, width, height, filename):
        """Create an image component and file it into the diagram in a single action.

        :param x: Location of the image on the x axis
        :type x: int
        :param y: Location of the image on the y axis
        :type y: int
        :param width: Width of image in the diagram (may differ from actual image width)
        :type width: int
        :param height: Height of the image in the diagram (may differ from actual image height)
        :type height: int
        :param filename: Filename, including path, to the image.
        :type filename: string
        """
        self.components.append(Image(x, y, width, height, filename))

    def add_stylesheet(self, filename):
        """Link an external stylesheet to the diagram. Multiple stylesheets can be added. They are referenced in the order added, this may be important where one style overrides another.

        :param filename: filename of stylesheet (include path to file)
        :type filename: str
        """
        self.stylesheets.append(filename)

    def add_pin(self, x , y, direction='right', label_data=None):
        """Create a pin component, with associated labels, and file it into the diagram in a single action.

        :param x: Location of the pin on the x axis 
        :type x: int
        :param y: location of the pin on the y axis
        :type y: int
        :param direction: Specify which direction labels are to be aligned from the pin location. Valid values are 'left' and 'right'. Defaults to 'right'.
        :type direction: str, optional
        :param label_data: A tuple with parameters required for Label(), defaults to None
        :type label_data: [type], optional
        """
        label_data = label_data or []
        pin = Pin(x, y, direction)
        for label_args in label_data:
            pin.add_label(*label_args)
        self.components.append(pin)

    def add_legend(self, x, y, width, tags, items):
        """Create a legend component and file it into the diagram in a single action.

        :param x: Location of the image on the x axis
        :type x: int
        :param y: Location of the image on the y axis
        :type y: int
        :param width: Width of the legend component. Set manually as font styling can unexpectedly affect content widths. 
        :type width: int
        :param tags: Applied to the legend as css class selector(s). Multiple tags can be included as a space separated list.
        :type tags: str, optional
        :param items: List of tuples documenting legend entries and associated tags. eg `[('GPIO', 'gpio'), ('GND', 'pwr-mgt')]`
        :type items: List
        """
        self.components.append(Legend(x, y, width, tags, items))

    def export(self, filename, embed_styles=True, overwrite=False):
        """Output diagram in SVG format. 

        :param filename: filename and path for exporting.
        :type filename: str
        :param embed_styles: Collates and embeds stylesheets as styles in the SVG file, defaults to True
        :type embed_styles: bool, optional
        :param overwrite: [description], defaults to False
        :type overwrite: bool, optional
        """

        """Output an SVG formatted diagram.

        :param filename: filename and path for exporting.
        :type filename: str
        :param overwrite: If set to False, export function aborts if the file already exists avoiding accidental overwriting. Defaults to False.
        :type overwrite: bool, optional
        """

        filepath = Path(filename)
        
        if filepath.is_file() and not overwrite:
            print('This file already exists! To enable overwrite add \'overwrite=True\' to the Diagram.export arguments.')
            return

        styles = ''
        if embed_styles:
            for stylesheet in self.stylesheets:
                with open(stylesheet, 'r') as f:
                    styles += f.read()

        for pin in self.components:
            self._rendered += pin.render()
        
        viewbox_x = min([p.bounding_box.x for p in self.components])
        viewbox_y = min([p.bounding_box.y for p in self.components])
        viewbox_w = max([p.bounding_box.x + p.bounding_box.w for p in self.components]) - viewbox_x
        viewbox_h = max([p.bounding_box.y + p.bounding_box.h for p in self.components]) - viewbox_y
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        except FileNotFoundError:
            pass # filename provided has no directory included.

        with open(filename, 'w') as f:
            f.write(
                svg.render(
                    x = 0,
                    y = 0,
                    width = viewbox_w,
                    height = viewbox_h,
                    viewbox = _BoundingBox(viewbox_x, viewbox_y, viewbox_w, viewbox_h),
                    selectors = 'pinout-diagram',
                    rendered_components = self._rendered,
                    stylesheets = self.stylesheets,
                    styles = styles or None
                )  
            )
            print(f'\'{filename}\' exported successfully.')