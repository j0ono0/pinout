Components
==========

class SVG
=========
    """Common base for all SVG entities that ultimately have a graphical representation."""

    scale
    -----

    Scale is abstracted as a property here and overridden by Component
    :return: (x, y) where x and y are either 1 or -1
    :rtype: tuple



    extract_scale
    -------------

    Separate scale information from a tuple that represents (x, y) or (width, height) values. Components and elements control orientation via the scale property rather than negative dimension/direction values. **NOTE**: Existing scale property is only overridded if the provided coords include a negative value.

    :param coords: tuple representing  (x, y) or (width, height). values may be positive or negative.
    :type coords: Union(tuple, Coords)
    :return: nametuple with absolute values
    :rtype: Coords

patch_config
-------------
    Recursively update source with patch dict items.

    :param source: Dict to apply updates to
    :type source: dict
    :param patch: Dict of new item values
    :type patch: dict
    :return: Source dict updated with patch dict.
    :rtype: dict


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



class Component
===============

    Container object that manages child Components and/or Elements as a group.

    Child coordinates are all relative to their parent Component.

    When scale is applied to a Component no direct affect to the <group> tag is applied but the scale setting is passed down to direct child **Elements**.

    :param children: Component and/or Element objects, defaults to None
    :type children: Union[Component, Element, StyleSheet], optional
    :param config: Default configuration values.
    :type config: dict, optional
    """


    bounding_coords
    ---------------
    
    Coordinates, relative to its parent, representing sides of a rectangle that encompass all child elements of the rendered Component.

        :return: (x_min, y_min, x_max, y_max)
        :rtype: tuple

    width
    -----
    Calculated width that encompasses all child elements

        :return: value representing a width in pixels
        :rtype: int


    height
    ------
    
    Calculated height that encompasses all child elements

    :return: value representing a height in pixels
    :rtype: int

    scale
    -----
    
    Scale has no direct effect of components however all immediate element children of a component inherit their parents scale value.

    :return: tuple in the form of (x, y) where expected values are either 1 or -1.
    :rtype: tuple

    bounding_rect
    -------------

    Coordinates representing the location of a components origin (usually top-left corner) within its parent along with a width and height that encompass all child elements.

    :return: (x, y, width, height)
    :rtype: tuple

    add_and_instantiate
    -------------------
    
    Instantiate an instance of a class and add it to the components children. This is done as a method to allow attributes to be added/amended in the single process.

    :return: Instance of the instantiated class
    :rtype: object


    render
    ------

    Render Component, and children, as SVG markup.
    NOTE: *scale* only affects Elements! It does not affect the grapical appearance of Components.

    :return: SVG markup of component including all children.
    :rtype: str


class StyleSheet
================
   
    :param path: Filename, including path, of the external stylesheet. *NOTE*: If *embedding*, a relative path is relative to the current working directory. If *linking*, a relative path is relative to the location of the final SVG diagram.
    :type path: str
    :param embed: Elect to link or embed the stylesheet, defaults to False
    :type embed: bool, optional


    render
    ------
    
    Create SVG tag with content to either embed or link styles.

        :return: SVG <link> or <style> code
        :rtype: string


#####################################################################
# SVG tag classes


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



#####################################################################
Composite classes
===================


class Label(Element):
    """A single line of text infront of a rectangle. *Note*: Text length is not auto-detected and the element's width should be set to ensure text will not overflow the rectangle in the final diagram export.

    :param text: Text to appear on the label
    :type text: string
    """

    def render(self):
create an SVG <group> tag that includes text and an rectangle.

        :return: SVG <group> code
        :rtype: string


class PinLabel(Component):
    """Comprised of a Line and Label element, this component encapsulates the requirement for a single pin label. All arguments have default settings in the components config.

    :param text: Text displayed in the label
    :type text: string
    :param offset: x and y distance that the label is offset from its parent. A leader line graphically bridges from the parent origin to the the offset coords.
    :type offset: (tuple)
    :param box_width: Width of the label portion of the PinLabel. Total width is box_width + offset.x
    :type box_width: int
    :param box_height: Height of the label portion of the PinLabel.
    :type box_height: int
    """



class PinLabelRow(Component):
    """Assists with grouping and arranging pinlabels that relate to the same pin into a row.

    :param offset: x and y distance that the row is offset from its parent. A leader line graphically bridges from the parent origin to the the offset coords.
    :type offset: tuple in the form of (x, y)
    :param labels: List of tuples documenting label attributes ("text", "tag", "offset", "box_width"). Only 'text' and 'tag' are required. The other optional values fallback to config defaults. :code:`offset=None` can be used to supply a 'box_width' but use the default 'offset' value.
    :type labels: List of tuples
    """

   

    def render(self):
Prior to rendering, a leaderline is automatically added, joining the first label to the components origin.

        :return: SVG <group> containing a row of pin labels
        :rtype: string



class PinLabelSet(Component):
    """This is the recommended method of adding pin labels to a diagram.
    :param offset: Relative x and y offset from the pin location for the first label in a row
    :type offset: tuple
    :param labels: tuples nested within a 2 dimensional array. Each list within the 'labels' list represents a pin in the header. Each entry within those lists becomes a label.
    :type labels: Tuples nested within a 2 dimensional array. Each list within 'labels' represents a pin in the header. Each entry within those lists becomes a label. The label is a tuple in the format :code:`(<text>, <css tag>, <offset>, <box_width>)` the second two arguments are optional.
    :param pitch: 'x' and 'y' distance in pixels between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. (30, 0) creates a horizontal header. (-30, 0) creates a horizontal header in the reverse direction. This can be useful for 'stacking' rows in reversed order to avoid leader-lines overlapping.
    :type pitch: tuple, optional
    """



class Legend(Component):
    """Provide a colour coded legend to describe pin labels. All data to populate a legend must be documented in the diagram's config by adding an YAML formatted file::

        # config.yaml

        legend:
            categories: [
                # [<Title>, <CSS class 'tag'>]
                ["Analog", "analog"],
                ["GPIO", "gpio"],
                ["PWM", "pwm"],
            ]

    *Note*: *pinout* does not calculate text widths. a manually provided with should be included to ensure text remains enclosed within the legend.

    A complete set of *pinout* defaults can be duplicated from the command line for reference::

            >>> py -m pinout.file_manager --duplicate config

    config.yaml includes all legend attributes that can be altered.

    """


class Annotation
================
