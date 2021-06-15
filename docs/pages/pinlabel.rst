Pin Labels
==========

.. currentmodule:: pinout.components.pinlabel


PinLabel
--------
.. autoclass:: PinLabel

Body
----
.. autoclass:: Body

Leaderline
----------
.. autoclass:: Leaderline

Group
-----
.. autoclass:: PinLabelGroup

    This is the recommended method of adding pin labels to a diagram. Locate the PinLabelSet by setting *x* and *y* attributes. 
    
    Pitch is the distance, in pixels, between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. (30, 0) creates a horizontal header. (-30, 0) creates a horizontal header in the reverse direction. This can be useful for 'stacking' rows in reversed order to avoid leader-lines overlapping.
