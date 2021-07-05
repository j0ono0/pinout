Pin Labels
==========

.. currentmodule:: pinout.components.pinlabel

Base
----
.. autoclass:: Base
    :show-inheritance:

    :param content: Text displayed in label, defaults to ""
    :type content: str, optional
    :param x: position of label on x-axis , defaults to 0
    :type x: int, optional
    :param y: position of label on y-axis, defaults to 0
    :type y: int, optional
    :param tag: categorise the label - applied as a CSS class, defaults to None
    :type tag: str (CSS name compliant), optional
    :param body: replace or configure the default body component, defaults to None
    :type body: dict or pinlabel.Body instance, optional
    :param leaderline: replace or configure the default leaderline component, defaults to None
    :type leaderline: dict or pinlabel.Leaderline, optional
    


PinLabel
--------
.. autoclass:: PinLabel
    :show-inheritance:
    
    See Base for details of this component.

Body
----
.. autoclass:: Body 
    :show-inheritance:

    :param x: position of label on x-axis
    :type x: int
    :param y: position of label on y-axis
    :type y: int
    :param width: Width of label body
    :type width: int
    :param height: Height of label body
    :type height: int
    :param corner_radius: Corner radius of label body, defaults to 0
    :type corner_radius: int, optional


Leaderline
----------
.. autoclass:: Leaderline
    :show-inheritance:

    :param lline: Override configuration or replace the pinlabel's leaderline.
    :type lline: dict of leaderline attributes or replacement Leaderline instance

PinLabelGroup
-------------
.. autoclass:: PinLabelGroup
    :show-inheritance:

    This is the recommended method of adding pin labels to a diagram. Locate the PinLabelSet by setting *x* and *y* attributes. 
    
    Pitch is the distance, in pixels, between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. (30, 0) creates a horizontal header. (-30, 0) creates a horizontal header in the reverse direction. This can be useful for 'stacking' rows in reversed order to avoid leader-lines overlapping.

    :param x: x-coordinate of the first pin in the header
    :type x: int
    :param y:  y-coordinate of the first pin in the header
    :type y: int
    :param pin_pitch: Distance between pins in the header
    :type pin_pitch: tuple: (x,y)
    :param label_start: Offset of the first label from the first pin
    :type label_start: tuple: (x,y)
    :param label_pitch: Distance between each row of labels
    :type label_pitch: tuple: (x,y)
    :param labels: Label data
    :type labels: List
    :param leaderline: Leaderline customisations, defaults to None
    :type leaderline: dict or Leaderline object, optional
    :param body: Label body customisations, defaults to None
    :type body: dict or LabelBody object, optional
