.. _tutorial:

Tutorial
===============

This tutorial walks through the features available in *pinout* and duplicates code from *sample_diagram.py* (see :ref:`quickstart`).

*Before you start*: Each diagram requires a hardware image and stylesheet to display successfully. If you haven't already, please read the :ref:`install` section that includes access to samples files.

.. figure:: _static/finished_sample_diagram.*

   The finished diagram from this tutorial.

Start a new diagram
-------------------

Start by importing the pinout diagram module and creating a new diagram object::

    from pinout import diagram
    
    pinout_diagram = diagram.Diagram()

Add a stylesheet
----------------

Strictly speaking this step is optional as *pinout* will create a stylesheet for you in the absence of one but relies on some guess work so output may vary. To ensure a predictable outcome add `sample_styles.css` to the diagram::
    
    pinout_diagram.add_stylesheet('sample_styles.css')


Add an image
------------

Adding an image is similar to the stylesheet. The extra arguments are *x*, *y*, *width*, and *height*. All function are documented with more detail in the :ref:`modules` section::

    pinout_diagram.add_image(0, 0, 220, 300, 'sample_hardware_board.png')

This is also a good moment to do some planning and preparation. Measuring critical dimensions on the board now will streamline accurate placement of pins and labels. 

.. figure:: _static/hardware_measurements.*
   
   Hardware measurements before beginning will aid with accurate pin and label placement.

**TIP, Component coordinates:** On export the final diagram dimensions are calculated and all components shifted into view (via the SVG viewBox). Consequently, component 'x' and 'y' positioning is relative to  an arbitary (0, 0) location and not the final diagram. It is recommended to position the board image to make easier calculations for subsequent pin placements.

In this tutorial all (x, y) coordinates are relative to the board's top-left corner. 


Add a legend
------------

The legend documents label categories. These categories are visually represented by styles documented in the stylesheet. The first step in creating a legend is to create a list that *tags* category *names*. The names appear in the legend, and tags become css classes that associate each label with a style::

    items = [
        # (<name>, <tags>),
        ('GPIO', 'gpio'),
        ('GPI', 'gpi'),
        ('Analog', 'analog'),
        ('PWM', 'pwm'),
        ('Power Management', 'pwr-mgt'),
    ]

With items documented adding a legend to the diagram is done with a single line of code::

    pinout_diagram.add_legend(-230, 160, 200, 'legend legend-labels', label_categories)

The legend should not obscure, or be obscured, by other components. Returning to tweak this feature after labels have been completed may be required for the best result.

.. figure:: _static/legend_measurements.*
   
Measurements for this component were finalised *after* labels were added. 


Set default label values
------------------------

.. figure:: _static/pin_and_label_detail.*

   Measurements for pin placement and label sizing 

Labels have several settings that control their size and appearance. These values can be applied per label, however most labels are likely to share common traits. Default values exist to serve this requirement in the form of class variables. Setting them is as simple as assigning a new value::

    diagram.Label.default_width = 70
    diagram.Label.default_height = 25
    diagram.Label.default_gap = 5

*Note:* 'gap' is the distance between labels, or in the instance of the first label, the distance from the label to the pin location.


Create a Pin with Labels
------------------------

This is slow way, included to provide an idea of the steps going on behind the scene::

    leftpin = diagram.Pin(16, 105, 'left')

Add some labels to the pin. *Note*: label width, height, and gap, can be 
controlled per label and overrides default settings::

    leftpin.add_label('#1', 'gpio', 60, 25, 60)
    leftpin.add_label('A1', 'analog')
    leftpin.add_label('PWM', 'pwm')

Add this pin to the diagram::

    pinout_diagram.components.append(leftpin)


Create multiple Pins and Labels
-------------------------------

The fast and recommended way::

    label_data = [('#2', 'gpio',60, 25, 60),('GPI', 'gpi')]  
    pinout_diagram.add_pin(16, 135, 'left', label_data)

With a little 'python-foo' this process can be streamlined dramatically::

    custom_specs = (60, 25, 60) 
    pin_label_data = [
            [('Vss', 'pwr-mgt', 40, 20, 190)], 
            [('GND', 'pwr-mgt', 40, 20, 190)], 
            [('#6', 'gpi',*custom_specs),('A3', 'analog'),('CLK', 'gpi')], 
            [('#5', 'gpio',*custom_specs),('A2', 'analog')], 
        ]

Hardware headers have evenly spaced pins - which can be taken advantage of in a loop. These variables were determined by 
measuring pin locations on the image::

    y_offset = 105
    x_offset = 204
    pitch = 30

    for i, label_data in enumerate(pin_label_data):
        y = y_offset + pitch * i
        pinout_diagram.add_pin(x_offset, y, 'right', label_data)


Export the diagram
------------------

.. figure:: _static/finished_sample_diagram.*

   The finished diagram from this tutorial.

The final diagram can be exported as a graphic in SVG format and should match the finished diagram shown here. This format and excellent for high quality printing but still an effecient size for web-based usage. Note: the 'overwrite' argument is a safeguard to prevent unintentionally losing existing files. Set it to *True* for easier tinkering on a single SVG graphic::

    pinout_diagram.export('sample_diagram.svg', overwrite=False)

    # expected output:
    # > 'sample_diagram.svg' exported successfully.

The most convenient method of viewing the newly exported SVG file is with your browser.

Next steps
----------

This guide has glossed over many argument definitions used in functions. Experimenting with changing values and re-exporting the diagram will quickly reveal their purpose. All function are also documented in the :ref:`modules` section.

Rerunning this guide with no css file added to the diagram will create an auto-generated stylesheet. It makes some educated guesses about approriate styles and is a handy method for 'bootstrapping' a stylesheet for your own diagrams.

Depending on you intended usage embedding the stylesheet and/or image (the latter via base64 encoding) can be implemented by adding `embed=True` to as an argument when adding those components.

**TIP:** Embedding the image and styles allows the SVG display correctly in InkScape. This might be an appealing work-flow option for encorporating the diagram into other media.