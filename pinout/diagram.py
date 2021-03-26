import os
from pathlib import Path
from collections import namedtuple
from .templates import svg
from . import style_tools
from . import file_manager
from .components import Pin, Label, Legend, Image, StyleSheet, _BoundingBox, _Coords


class Diagram:
    """Components are collated and the final diagram is exported with this class. A typical diagram will include an image, pins with labels, and a stylesheet.
    """
    def __init__(self):
        self.components = []
        self.stylesheets = []

    def add_image(self, x, y, width, height, filename, embed=False):
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
        :param embed: Base64 encodes the image and embeds it in the SVG file, defaults to False
        :type embed: bool, optional
        """
        self.components.append(Image(x, y, width, height, filename, embed))

    def add_stylesheet(self, filepath, embed=False):
        """Link an external stylesheet to the diagram. Multiple stylesheets can be added. They are referenced in the order added, this may be important where one style overrides another.

        :param filename: filename of stylesheet (include path to file)
        :type filename: str
        :param embed: Elect to embed the css file contents into the SVG file, defaults to False.
        "type embed: bool, optional
        """
        self.components.append(StyleSheet(filepath, embed))

    def add_pin(self, pin_x , pin_y, label_x=None, label_y=None, label_data=None):
        """Create a pin component, with associated labels, and file it into the diagram in a single action.

        :param pin_x: Location of the pin on the x axis 
        :type pin_x: int
        :param pin_y: location of the pin on the y axis
        :type pin_y: int
        :param direction: Specify which direction labels are to be aligned from the pin location. Valid values are 'left' and 'right'. Defaults to 'right'.
        :type direction: str, optional
        :param label_data: A tuple with parameters required for Label(), defaults to None
        :type label_data: [type], optional
        """
        label_data = label_data or []
        pin = Pin(pin_x, pin_y, label_x, label_y, label_data)
        self.components.append(pin)

    def add_pin_header(self, pin_header):
        pin = _Coords(*pin_header['pin_coords'])
        lbl = _Coords(*pin_header['label_coords'])
        try:
            pitch = pin_header['pitch']
        except KeyError as e:
            pitch = 0
            if len(lbl) == 1:
                print('No \'pitch\' attribute present but \'label\' includes multiple lists.')
                print(pin_header)
                raise
        
        for i, lbl_data in enumerate(pin_header['labels']):
        
            # Calc coords for label locations (left & right)
            if lbl.y == pin.y:
                # Left or Right
                pin_ = _Coords(pin.x, pin.y + pitch * i)
                lbl_ = _Coords(lbl.x, lbl.y + pitch * i)
            elif lbl.y < pin.y:
                # Up
                if lbl.x < pin.x:
                    # Up Left 
                    pin_ = _Coords(pin.x + pitch * i, pin.y)
                    lbl_ = _Coords(lbl.x, lbl.y - pitch * i)
                else:
                    # Up Right
                    y_offset = lbl.y - (len(pin_header['labels']) - 1) * pitch
                    pin_ = _Coords(pin.x + pitch * i, pin.y)
                    lbl_ = _Coords(lbl.x, y_offset + pitch * i)
            else:
                # Down
                    if lbl.x < pin.x:
                        # Down Left
                        pin_ = _Coords(pin.x + pitch * i, pin.y)
                        lbl_ = _Coords(lbl.x, lbl.y + pitch * i)

                    else:
                        # Down Right
                        y_offset = lbl.y + (len(pin_header['labels']) - 1) * pitch
                        pin_ = _Coords(pin.x + pitch * i, pin.y)
                        lbl_ = _Coords(lbl.x, y_offset - pitch * i)
            

            self.add_pin(pin_.x, pin_.y, lbl_.x, lbl_.y, pin_header['labels'][i])
        

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

    def export(self, svgname, overwrite=False):
        """Output the diagram in SVG format. If no stylesheet(s) are included one will be generated automatically and linked to. See style_tools.default_css() for more details.

        :param svgname: Name of svg file to be created, including path to export.
        :type svgname: str
        :param overwrite: When set to False, this function aborts if the file already exists avoiding accidental overwriting. Defaults to False.
        :type overwrite: bool, optional
        """

        # Create export location and unique filename if required
        svgpath = Path(svgname)
        svgpath.parent.mkdir(parents=True, exist_ok=True)
        if not overwrite:
            svgpath = file_manager.unique_filepath(svgpath)
        svgpath.touch(exist_ok=True)

        styles = ''
        rendered_components = ''

        # Generate default styles if none supplied
        stylesheets = [s for s in self.components if isinstance(s, StyleSheet)]
        if not stylesheets:
            default_css = style_tools.default_css(self)
            cssname = svgpath.name[:-len(svgpath.suffix)]
            csspath = Path(svgpath.parent, '{}.css'.format(cssname))
            # File name may change if overwrite is False
            actual_csspath = file_manager.export_file(default_css, csspath, overwrite)
            
            self.components.insert(0, StyleSheet(actual_csspath.name))

        # Render all components
        for component in self.components:
            rendered_components += component.render()
        
        # Calculate viewbox to display all components
        viewbox_x = min([p.bounding_box.x for p in self.components if hasattr(p,'bounding_box')])
        viewbox_y = min([p.bounding_box.y for p in self.components if hasattr(p,'bounding_box')])
        viewbox_w = max([p.bounding_box.x + p.bounding_box.w for p in self.components if hasattr(p,'bounding_box')]) - viewbox_x
        viewbox_h = max([p.bounding_box.y + p.bounding_box.h for p in self.components if hasattr(p,'bounding_box')]) - viewbox_y
        
        # Render final SVG file
        svgpath.write_text(
            svg.render(
                x = 0,
                y = 0,
                width = viewbox_w,
                height = viewbox_h,
                viewbox = _BoundingBox(viewbox_x, viewbox_y, viewbox_w, viewbox_h),
                selectors = 'pinout-diagram',
                rendered_components = rendered_components,
                stylesheets = self.stylesheets,
                styles = styles or None
            )  
        )
        print(f'\'{svgpath}\' exported successfully.')