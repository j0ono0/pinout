Core
====

.. currentmodule:: pinout.core

Layout
------

.. autoclass:: Layout
    :show-inheritance:
    
    :param x: x-axis location, defaults to 0
    :type x: int, optional
    :param y: y-axis location, defaults to 0
    :type y: int, optional
    :param tag: css class tag, defaults to None
    :type tag: string (must be valid css class name), optional
    
    Currently **scale** is the only vaid additional argument that may be included in key-word-arguments (kwargs).

    .. autoproperty:: add

        This is a convenience function that appends an object to instance.children. It also returns the instance allowing instance creation and adding a single line of code. 

    .. autoproperty:: add_def

    .. autoproperty:: add_tag

    .. autoproperty:: update_config
    
    .. autoproperty:: bounding_rect
        
    .. autoproperty:: bounding_coords

    .. autoproperty:: render_defs
    
    .. automethod:: render_children


StyleSheet
----------

.. autoclass:: StyleSheet
    :show-inheritance:

    This class should be added to a diagram via Diagram.add_stylesheet()

    :param path: Path to stylesheet file
    :type path: string
    :param embed: Embed stylesheet in exported file, defaults to False
    :type embed: bool, optional

    .. automethod:: render


Raw
--------

.. autoclass:: Raw
    :show-inheritance:

    :param content: SVG code
    :type content: string


Group
-----

.. autoclass:: Group
    :show-inheritance:

    :param x: Coordinate of top-left point in x-axis, defaults to 0
    :type x: int, optional
    :param y: Coordinate of top-left point in y-axis, defaults to 0
    :type y: int, optional
    :param tag: CSS class, defaults to None
    :type tag: string (must meet css class naming rules), optional

    
SvgShape
--------
.. autoclass:: SvgShape
    :show-inheritance:

    :param x: Location coordinate in x-axis, defaults to 0
    :type x: int, optional
    :param y: Location coordinate in y-axis, defaults to 0
    :type y: int, optional
    :param width: Width of the component, defaults to 0
    :type width: int, optional
    :param height: Height of the component, defaults to 0
    :type height: int, optional
    :param tag: CSS class, defaults to None
    :type tag: string (must meet css class naming rules), optional


Path
----
.. autoclass:: Path 

    :param path_definition: Path definition, defaults to ""
    :type path_definition: str, optional
 
    
 Rect
 ----
.. autoclass:: Rect
    :show-inheritance:
    
    :param corner_radius: Round rectangle corners, defaults to 0
    :type corner_radius: int, optional


Text
----
.. autoclass:: Text
    :show-inheritance:

    :param content: Text to be included in the tag
    :type content: string


Image
-----

.. autoclass:: Image
    :show-inheritance:

    Valid bitmap formats are PNG and JPG - matching the SVG specifications. SVG images can be added via this Image class however they must provided at **1:1 dimensions** and include their own dimensions in the <svg> tag. Additional care needs to be taken when incorporating SVG files as it is possible for CSS classes to clash.

    Image size can be controlled by supplying a width and height property. Omiting one, or both, properties results in the supplied image's pixel dimensions to be used. 
    
    Images are scaled proportionally. Where supplied dimensions differ in proportions to the images pixel dimensions the image is scaled to fit, and centred, in the user supplied dimensions.

    :param path: Path to either an image file on the local file system or a URL. Path is relative to image file if *not* embedding, otherwise it is relative to the script exporting the file. 
    :type path: string
    :param embed: Embed image in exported file, defaults to False
    :type embed: bool, optional

    
    .. autoproperty:: add_coord

        When returned with Image.coord() the values are scaled, and offset if required, to match the image scaling and ensuring the coordinate remains correctly aligned on the image.

        :param name: Name of coordinate
        :type name: string
        :param x: x-axis coordinate
        :type x: int
        :param y: y-axis coordinate
        :type y: int

    
    .. autoproperty:: coord
    
    Coordinates are stored with Image.add_coord() and scaled to match user nominated image dimensions. As images are scaled proportionally an offset can result where suppled width and height are not proportional to the images pixel dimensions. By default returned coordinates include any offset ensuring a coordinate remains aligned correctly. By setting `raw=True` the coordinates are scaled purely on actual size vs. user nominated size. This is useful for documenting `pin_pitch`.
    
    :param name: Name of coordinate
    :type name: string
    :param raw: Return a scaled values without image offset, defaults to False
    :type raw: bool, optional
    :return: Coordinates scaled to match image scaling
    :rtype: tuple (x, y)