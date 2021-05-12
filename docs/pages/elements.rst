Elements
========

.. currentmodule:: pinout.elements


SVG
---

.. autoclass:: SVG

    *NOTE*: :code:`self.config` is a local config used for customising appearance on a per-instance level. this config may, in part, be passed onto children. 

    .. autoproperty:: scale

        Scale is used in pinout to mirror horizontally (-1, 1), vertically (1, -1) or both (-1, -1)


    .. automethod:: extract_scale

        Scale and coordinates (or dimensions) can be defined by users as a combined attribute - such as *offset* in PinLabel - but are stored and processed as two separate values when rendering the SVG. *extract_scale* extracts the scale - a tuple of +/-1 representing direction - and converts the coordinates to absolute values. For example::
        
            >>> value, scale = extract_scale((-5, 30))
            >>> value == (5, 30)
            >>> scale == (-1, 1) 


Element
-------

.. autoclass:: Element
    :show-inheritance:
    
    All elements **must** have a width and height for accurate calculation of the final graphic's dimenions and viewbox settings.
    
    
    .. autoproperty:: bounding_coords
    
        **Values are relative to its parent.**. Effects of 'scale' on Elements may vary. Default behaviour expects an elements bounding coords remain unchanged when scale is applied. Typical use of scale on elements is to re-orientation text within an element.
    
    .. autoproperty:: bounding_rect
    
    .. automethod:: render
    

Image
-----

.. autoclass:: Image
    :show-inheritance:

    *IMPORTANT*: Image width and height parameters must be supplied for the image to display! *pinout* does not auto-detect these attributes. Using images at a **1:1 ratio** is strongly recommended.
    
    Where :code:`embed=False` the path is relative to the exported file. Where :code:`embed=True` the path is relative to the current working directory.

    .. automethod:: render


Rect
----

.. autoclass:: Rect
    :show-inheritance:


Path
----

.. autoclass:: Path
    :show-inheritance:

    *NOTE*: If the path forms part of the diagram bounding box a width and height must be **explicitly** passed to it for final dimensions to be calculated correctly.

    
Label
-----

.. autoclass:: Label
    :show-inheritance:

    *Note*: Text length is not auto-detected and the element's width should be set to ensure text will not overflow the rectangle in the final diagram export.
