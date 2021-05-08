Components
==========

.. currentmodule:: pinout.components

Component
---------

.. autoclass:: Component
    :show-inheritance:
    
    Children should be added via :code:`Component.add`

    Default diagram config settings are accessible via the class variable :code:`Component.config`.

    .. autoproperty:: bounding_coords

    .. autoproperty:: bounding_rect

    .. autoproperty:: width

    .. autoproperty:: height
    
    .. autoproperty:: scale

    .. autoproperty:: add

        This is a convenience function that appends an object to instance.children. It also returns the instance allowing instance creation and adding a single line of code. 

    .. automethod:: patch_config
    
        Used to modify existing config values as they are passed to children
    
    .. automethod:: render



Diagram
--------

.. autoclass:: pinout.diagram.Diagram
    :show-inheritance:
    
    .. automethod:: add_config
        
        Add configuration settings to the diagram. Parameters set in this fashion override the existing 'defaults' and referenced by components when parameters are not explicitly assigned.

        A complete set of *pinout* defaults can be duplicated from the command line for reference::

            >>> py -m pinout.file_manager --duplicate config

    .. automethod:: add_image
                
        .. important ::
            
            Image width and height parameters must be supplied for the image to display! *pinout* does not auto-detect these attributes. 
            
            Using images at a **1:1 ratio** is strongly recommended.

        :param path: Path to the image file. *Note*: Where :code:`embed=False` the path is relative to the exported file. Where :code:`embed=True` the path is relative to the current working directory.
        :type path: string
        :param embed: Embed or link the image in the exported file, defaults to False
        :type embed: bool, optional

    .. automethod:: add_legend


    .. automethod:: add_pinlabelset

    .. automethod:: add_annotation

    .. automethod:: export


PinLabelSet
-----------

.. autoclass:: PinLabelSet
    :show-inheritance:

    This is the recommended method of adding pin labels to a diagram. Locate the PinLabelSet by setting *x* and *y* attributes. 
    
    Pitch is the distance, in pixels, between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. (30, 0) creates a horizontal header. (-30, 0) creates a horizontal header in the reverse direction. This can be useful for 'stacking' rows in reversed order to avoid leader-lines overlapping.

Legend
------

.. autoclass:: Legend
    :show-inheritance:

*Note*: *pinout* does not calculate text widths. A manually provided width may be required to ensure text remains enclosed within the legend.

Annotation
----------

.. autoclass:: Annotation

    An alternative method to 'label' a diagram, suitable for highlighting hardware details.  