Core
====

.. currentmodule:: pinout.core

Layout
------

.. autoclass:: Layout
    :show-inheritance:
    
    **This class is not designed to be used directly.** Methods listed here are inherted by child classes.

    :param x: x-axis location, defaults to 0
    :type x: int, optional
    :param y: y-axis location, defaults to 0
    :type y: int, optional
    :param tag: css class tag, defaults to None
    :type tag: string (must be valid css class name), optional

    .. autoproperty:: add

        This is a convenience function that appends an object to Layout.children. It also returns the instance allowing instance creation and adding a single line of code. 

    .. autoproperty:: add_def

        :param instance: Component class instance
        :return: instance
        :rtype: Component instance

        The 'defs' section of the SVG file provides a location for renderable elements to be included in the file but not directly rendered in output. this becomes a useful feature where a instances of a component appears in multiple locations or a component is applied to another rendered component.

        **Example: ClipPath**

        ClipPath instances include renderable shapes (eg. the Rect component) that are not to be directly rendered in output. As such they should be included in a diagram's defs section::

            from pinout.components.layout import Diagram, ClipPath
            from pinout.core import Rect
            
            # Setup a minimal example
            diagram = Diagram(800, 400)
            rect_01 = diagram.add(Rect(0, 0, 400, 200), 
            rect_02 = diagram.add(Rect(400, 200, 400, 200), 
            
            # Create a clip-path storing it in the diagram's defs section.
            # Add a shape for the clip-path to use.
            clip = diagram.add_def(ClipPath())
            clip.add(Rect(x=100, y=100, width=50, height=50))

            # The clip-path can now be applied to other components.
            rect_01.clip_id = clip.id
            rect_02.clip_id = clip.id

            # Changes to 'clip' will affect both 'rect_01' and 'rect_02'
            # as they reference the same component instance.

        **Example: Images**

        To avoid including multiple instances of an image in the diagram, a single image can be included in the defs section and referenced multiple times from their::  

            from pinout.components.layout import Diagram, Image

            # Setup a minimal example
            diagram = Diagram(800, 400)

            # Add an image into the diagram's defs section
            img_01 = diagram.add_def(Image("hardware.png"))

            # New Image instances can now be created referencing
            # 'img_01' and positioned independently.
            img_02 = diagram.add(Image(img_01, x=400, y=200, rotate=90)) 


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
     
    Where supplied dimensions differ to the image's pixel dimensions the image is scaled proportionally, and centred, to fit supplied dimensions.

    Image instances can be added to any component that inherits from the Layout class::

        from pinout.components.layout import Diagram
        from pinout.core import Image

        diagram = Diagram(800,400)

        # Add an image to the diagram at coordinates (20,20)
        diagram.add(Image("hardware.png", x=20, y=20))

    If an image is to be used multiple times in a single diagram a single instance should be included into the diagram's 'defs' and referenced from there::
        
        from pinout.components.layout import Diagram
        from pinout.core import Image

        diagram = Diagram(800,400)

        # Add an image into the diagram's 'defs'
        img_src = diagram.add_def(Image("hardware.png"))

        # Create x2 new image instances both referencing 'img_src'
        img_01 = diagram.add(Image(img_src, x=20, y=20)) 
        img_02 = diagram.add(Image(img_src, x=400, y=20)) 

    :param path: Path to either an image file on the local file system or a URL. Path is relative to image file if *not* embedding, otherwise it is relative to the script exporting the file. 
    :type path: string
    :param embed: Embed image in exported file, defaults to False
    :type embed: bool, optional


    .. autoproperty:: coord
    
    Coordinates stored in an Image instance can be retrieved with Image.coord(<coord_name>). On retrieval, coordinates are transformed to remain in the correct relative location on image instance regardless of the image's position, width, height, and rotation, for example::

        from pinout.components.layout import Diagram
        from pinout.core import Image

        diagram = Diagram(800,400)
        
        # Create an Image instance 'img'
        # Parameters match desired output and may 
        # differ from the image's actual dimensions
        img = diagram.add(Image(
            "hardware.png", 
            x=50, 
            y=10, 
            width=100, 
            height=200, 
            rotate=30
        ))

        # Add a coordinate to 'img'
        # This coordinate is measured against the original image at 1:1 scale
        img.add_coord("pin_a", 110, 150)

        # The transformed coordinate aligns correctly on the transformed image
        pin_a = img.coord("pin_a")

    By default returned coordinates include any offset that occurs when non-proportional width and height are set. By setting `raw=True` the coordinates are scaled purely on actual size vs. user nominated size. This is useful for documenting `pin_pitch`.
    
    :param name: Name of coordinate
    :type name: string
    :param raw: Return a scaled values without image offset, defaults to False
    :type raw: bool, optional
    :return: Coordinates scaled to match image scaling
    :rtype: tuple (x, y)
    
    .. autoproperty:: add_coord

        When returned with Image.coord() the values are scaled, and offset if required, to match the image scaling and ensuring the coordinate remains correctly aligned on the image.

        :param name: Name of coordinate
        :type name: string
        :param x: x-axis coordinate
        :type x: int
        :param y: y-axis coordinate
        :type y: int

    