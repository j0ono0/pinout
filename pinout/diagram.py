import os
from pathlib import Path
from collections import namedtuple
from itertools import zip_longest
from .templates import svg_pin_label, svg_group, svg_image, svg_legend, svg

BoundingBox = namedtuple('BoundingBox',('x y w h'))
Rect = namedtuple('Rect',['x','y','w','h','r'])
Line = namedtuple('Line',('x1','x2','y1','y2'))
LegendItem = namedtuple('LegendItem',('name tags label'))

class Label:

    PAD = 1
    CNR = 2

    def __init__(self, name, tags, width=60, height=20, gap=5):
        self.name = name
        self.width = width
        self.height = height
        self.tags = tags.strip()            # tags used as css classes
        self.gap = gap                      # Distance to previous box (filled with leader-line)


class Pin:
    def __init__(self, x, y, direction='right', label_tuples=None):
        self.x = x
        self.y = y
        self.labels = []
        self.direction = direction

        if label_tuples:
            for label in label_tuples:
                self.add_label(*label)
    
    def add_label(self, name, tags=None, width=60, height=20, gap=5):
        self.labels.append(Label(name, tags, width, height, gap))
    
    @property
    def width(self):
        return sum([label.width + label.gap for label in self.labels])

    @property
    def height(self):
        try:
            return max([label.height for label in self.labels])
        except ValueError:
            return 0

    @property
    def bounding_box(self):
        if self.direction == 'right':
            # labels sit right of pin
            x = self.x
        else:
            # labels sit left of pin
            x = self.x - self.width

        return BoundingBox(x, self.y - self.height/2, self.width, self.height)

    def render(self):
        offset_x = 0
        output = ''
        
        for label in self.labels:
            if self.direction == 'right':
                # RHS label
                output += svg_pin_label.render(
                    x = offset_x,
                    y = -label.height/2,
                    line = Line(label.PAD, label.gap, label.height/2, label.height/2),
                    box = Rect(label.gap, 0, label.width, label.height, label.CNR),
                    text = label.name,
                    selectors = label.tags
                )
            else:
                # LHS label
                output += svg_pin_label.render(
                    x = (label.width + label.gap + offset_x) * -1,
                    y = label.height / 2 * -1,
                    line = Line(label.width, label.width + label.gap - label.PAD, label.height/2, label.height/2),
                    box = Rect(0, 0, label.width, label.height, label.CNR),
                    text = label.name,
                    selectors = label.tags
                )
            offset_x += label.width + label.gap
        
        return  svg_group.render(
            x = self.x,
            y = self.y,
            content = output
        )


class Image:
    def __init__(self, x, y, width, height, filename):
        self.x = x
        self.y = y
        self.path = filename
        self.width = width
        self.height = height

    @property
    def bounding_box(self):
        return BoundingBox(self.x, self.y, self.width, self.height)
    
    def render(self):
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
    SWATCH_PAD = 5
    INSET = 20

    def __init__(self, x, y, width, items=None, tags=None):
        self.x = x
        self.y = y
        self.width = width
        self.items = items or {}
        self.tags = tags
    
    @property
    def height(self):
        return len(self.items) * (self.ITEM_HEIGHT + self.ITEM_PAD) - self.ITEM_PAD + 2 * self.INSET

    @property
    def bounding_box(self):
        return BoundingBox(self.x, self.y - self.ITEM_HEIGHT/2, self.width, self.height)

    def render(self):
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
            items = items,
            selectors = self.tags
        )
    

class Diagram:
    def __init__(self):
        self.components = []
        self.stylesheet = None
        self._rendered = ''

    def add_image(self, x, y, width, height, filename):
        self.components.append(Image(x, y, width, height, filename))

    def add_pin(self, x , y, direction='right', label_data=None):
        label_data = label_data or []
        pin = Pin(x, y, direction)
        for label_args in label_data:
            pin.add_label(*label_args)
        self.components.append(pin)

    def export(self, filename, overwrite=False):
        filepath = Path(filename)
        
        if filepath.is_file() and not overwrite:
            print('This file already exists! To enable overwrite add \'overwrite=True\' to the Diagram.export arguments.')
            return

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
                    viewbox = BoundingBox(viewbox_x, viewbox_y, viewbox_w, viewbox_h),
                    selectors = 'pinout-diagram',
                    rendered_components = self._rendered,
                    stylesheet = self.stylesheet,
                )  
            )
            print(f'\'{filename}\' exported successfully.')