Legend
======

.. currentmodule:: pinout.components.legend

Legend
------

.. autoclass:: Legend

    *Note*: *pinout* does not calculate text widths. A manually provided width may be required to ensure text remains enclosed within the legend.

    :param data: [description]
    :type data: [type]
    :param max_height: [description], defaults to None
    :type max_height: [type], optional
    
    
Swatch
------

.. autoclass:: Swatch

    :param width: Width of swatch, defaults to None
    :type width: int, optional
    :param height: Height of swatch, defaults to None
    :type height: int, optional
    

Entry
-----

.. autoclass:: LegendEntry

    The swatch attribute accepts either a dictionary of Swatch attributes or a Swatch instance. Swatch styling (ie filling with color) is done via CSS and should reference the LegendEntry class(es). 

    :param content: Text displayed in entry
    :type content: [type]
    :param width: Width of entry, defaults to None
    :type width: int, optional
    :param height: height of entry, defaults to None
    :type height: int, optional
    :param swatch: Graphical icon included in entry, defaults to None
    :type swatch: dict or Swatch, optional
    
