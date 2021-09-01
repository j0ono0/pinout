Manager
=======

The manager module provides various functions to assist *pinout* create diagrams. For users, Manager is primarily accessed via the command-line for the following.

Duplicate quick_start files
---------------------------

A fast way to get started exploring *pinout* is by trying out the quick_start diagram that is featured in the tutorial. Required files can be duplicated from the *pinout* package via command line::

    py -m pinout.manager --duplicate quick_start

    # expected output:
    # >>> data.py duplicated.
    # >>> hardware.png duplicated.
    # >>> pinout_diagram.py duplicated.
    # >>> styles.css duplicated.

*-d* works as a short-hand version of *--duplicate*

Export an SVG diagram
---------------------

Once a diagram has been documented it can be exported to SVG format via the command-line. The following example assumes the diagram file is named *'pinout_diagram.py'*, the pinout.Diagram instance is called *'diagram'* and the destination file is named *'my_diagram.svg'*::

    >>> py pinout.manager --export pinout_diagram my_diagram.svg

    # expected response:
    # 'my_diagram.svg' exported successfully.

    # Example where pinout.Diagram instance is named 'board_x_diagram'
    >>> py pinout.manager --export pinout_diagram my_diagram.svg board_x_diagram

Details to note:

- *pinout_diagram* does not have a *.py* suffix as it is referred to as a module name.
- *--export* can be expressed as a single letter *-e*
- An *--overwrite* (*-o*) can also be included to overwrite an existing file
- if the instance name is not 'diagram' the alternative name can be added as as third argument

Export in other formats
-----------------------

With the addition of CairoSVG *pinout* is able to export to PNG, PDF, and PS formats. Installation is done via pip::

    pip install cairosvg

.. note::

    CairoSVG has it's own (non-Python) dependencies. See :ref:`Install` for more details.

Once these dependencies have been installed replace the filename suffix to export in the desired format::

    # Export as png
    >>> py pinout.manager --export pinout_diagram my_diagram.png

    # Export as pdf
    >>> py pinout.manager --export pinout_diagram my_diagram.pdf
    
    # Export as ps
    >>> py pinout.manager --export pinout_diagram my_diagram.ps


Generate a cascading stylesheet
-------------------------------

Provided with a diagram file, the manager can extract components and tags, then export a stylesheet based on this data to assist with styling. The resulting stylesheet can then be further edited or a second stylesheet created to supplement the default styles::

    >>> py pinout.manager --css pinout_diagram diagram_styles.css

    # expected response:
    # Stylesheet created: 'diagram_styles.css'

As with exporting an SVG, the *-o* flag can be used to overwrite and existing file. Note, there is no short-hand for the *-css* flag.