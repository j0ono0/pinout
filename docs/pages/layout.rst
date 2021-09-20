Layout
======

.. currentmodule:: pinout.components.layout

Diagram
--------

.. autoclass:: Diagram
    :show-inheritance:

    :param width: width of diagram
    :type width: int
    :param height: height of diagram
    :type height: int
    :param tag: CSS class applied to diagram, defaults to None
    :type tag: string (must comply to CSS naming rules), optional

    .. automethod:: Diagram.add_stylesheet

        Pinout relies on cascading-style-sheet (CSS) rules to control presentation attributes of components.

        The path attribute is dependent on whether the styles are linked or embedded. When linked, the path is relative to the exported file. When embedded the path is relative to the diagram script file.

        :param path: Path to stylesheet file
        :type path: string
        :param embed: embed stylesheet in exported file, defaults to True
        :type embed: bool, optional
    

    .. automethod:: Diagram.render

        :return: SVG markup
        :rtype: string

Panel
-----
.. autoclass:: Panel
    :show-inheritance:

    The basic building block to control layout (grouping and location) of components that make up a complete diagram document. The Panel component renders two rectangles - and outer and inner rectangle - behind all child components to assist with graphical styling.

    The inset attribute controls dimensions of the 'inner rectangle'. All children are aligned relative to the inset coordinate (x1, y1).

    The inner dimensions can be accessed via the properties ``Panel.inset_width`` and ``Panel.inset_height``.

    :param width: Width of component
    :type width: int
    :param height: Height of component
    :type height: int
    :param inset: Inset of inner dimensions, defaults to None
    :type inset: Tuple (x1, y1, x2, y2), optional
