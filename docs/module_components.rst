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


Component(SVG)
==============

Container object that manages child Components and/or Elements as a group.

Child coordinates are all relative to their parent Component.

When scale is applied to a Component no direct affect to the <group> tag is applied but the scale setting is passed down to direct child **Elements**.

:param children: Component and/or Element objects, defaults to None
:type children: Union[Component, Element, StyleSheet], optional
:param config: Default configuration values.
:type config: dict, optional


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



class PinLabel(Component):
Comprised of a Line and Label element, this component encapsulates the requirement for a single pin label. All arguments have default settings in the components config.

:param text: Text displayed in the label
:type text: string
:param offset: x and y distance that the label is offset from its parent. A leader line graphically bridges from the parent origin to the the offset coords.
:type offset: (tuple)
:param box_width: Width of the label portion of the PinLabel. Total width is box_width + offset.x
:type box_width: int
:param box_height: Height of the label portion of the PinLabel.
:type box_height: int



class PinLabelRow(Component)
----------------------------

Assists with grouping and arranging pinlabels that relate to the same pin into a row.

:param offset: x and y distance that the row is offset from its parent. A leader line graphically bridges from the parent origin to the the offset coords.
:type offset: tuple in the form of (x, y)
:param labels: List of tuples documenting label attributes ("text", "tag", "offset", "box_width"). Only 'text' and 'tag' are required. The other optional values fallback to config defaults. :code:`offset=None` can be used to supply a 'box_width' but use the default 'offset' value.
:type labels: List of tuples


class PinLabelSet(Component)
----------------------------
This is the recommended method of adding pin labels to a diagram.
:param offset: Relative x and y offset from the pin location for the first label in a row
:type offset: tuple
:param labels: tuples nested within a 2 dimensional array. Each list within the 'labels' list represents a pin in the header. Each entry within those lists becomes a label.
:type labels: Tuples nested within a 2 dimensional array. Each list within 'labels' represents a pin in the header. Each entry within those lists becomes a label. The label is a tuple in the format :code:`(<text>, <css tag>, <offset>, <box_width>)` the second two arguments are optional.
:param pitch: 'x' and 'y' distance in pixels between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. (30, 0) creates a horizontal header. (-30, 0) creates a horizontal header in the reverse direction. This can be useful for 'stacking' rows in reversed order to avoid leader-lines overlapping.
:type pitch: tuple, optional
    


Legend(Component)
-----------------
Provide a colour coded legend to describe pin labels. All data to populate a legend must be documented in the diagram's config by adding an YAML formatted file::

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

    
