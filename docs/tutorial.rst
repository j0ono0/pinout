.. _tutorial:

Tutorial
===============

This tutorial walks through the main features available in *pinout*. If you have not installed *pinout* already please read the :ref:`install` section. This tutorial duplicates code from *quick_start_pinout.py*. To access a copy of this file and other resources see :ref:`quickstart`.

.. figure:: _static/quick_start_diagram.*

   The finished diagram from this tutorial.


Import modules
--------------

Start by importing the pinout diagram module and creating a new diagram object::

    from pinout import diagram
    from pinout import file_manager

The 'file_manager' modules has also been imported here - this is optional but will be used to show how to configure some stylistic aspect of the diagram in this tutorial.

Diagram measurements
--------------------

Taking some critical measurements of the hardware image before starting will streamline processes and save adjusting by trial-and-error later. Where pins are arranged in 'headers' the *PinLabelSet* class can be used place labels once a starting location has been documented.

.. figure:: _static/quick_start_measurements_left_header.*

- **x, y**: Coordinates of the first pin in the header.
- **pitch**: Distance between each pin of the header. (0, 30) steps 0px right and 30px down for each pin.
- **offset**: **Relative to the pin's (x, y) coodinates**. Locates the start position for a row of labels.
- **labels**: Data that documents each label and its relation in the header. Each list within 'labels' represents a pin in the header. Each entry within those lists becomes a label.  

These details are documented in a dict. Multiple headers can be grouped into a list for convenient processing later::

    pin_headers = [
        {
            # LHS header
            "x": 16,
            "y": 100,
            "pitch": (0, 30),
            "offset": (-55, 0),
            "labels": [
                [("Vcc", "pwr", (0, 0), 155)],
                [("1", "gpio"), ("A1", "analog")],
                [("2", "gpio"), ("PWM", "pwm", (-100, 0))],
            ],
        },
        # x2 more headers are included in 'quick_start_pinout.py'
    ]

Load a config file
------------------
Many of the default stylistic settings can be overridden by supplying new values in a yaml formatted file::

    file_manager.load_config("quick_start_config.yaml") 

**Note on coodinates**: SVG format sets (0, 0) as top-left with increasing x and y values moving to the right and down respectively. Component placement in pinout is made from an arbitrary (0, 0) location. The final diagram size and boundaries are calculated on export ensuring all components are visible - ie negative coordinates do not risk being outside the final diagram boundaries.

In this tutorial all (x, y) coordinates are relative to the hardware images's top-left corner which is positioned at (0, 0).


Add a stylesheet
----------------

Strictly speaking this step is optional as *pinout* will create a stylesheet for you in the absence of one but relies on some guess work so output may vary. To ensure a predictable outcome add `get_started_styles.css` to the diagram::
    
    pinout_diagram.add_stylesheet('get_started_styles.css', embed=True)


Add an image
------------

Adding an image is similar to the stylesheet. The extra arguments are *x*, *y*, *width*, and *height*. All function are documented with more detail in the :ref:`modules` section::

    pinout_diagram.add_image(0, 0, 220, 260, 'get_started_board.png', embed=True)


Add a legend
------------

The legend documents label categories. These categories are visually represented by styles documented in the stylesheet. The first step in creating a legend is to create a list that *tags* category *names*. The names appear in the legend, and tags become css classes that associate each label with a style::

    label_categories = [
        # (name, tag(s), color),
        ('GPIO', 'gpio'),
        ('Analog', 'analog'),
        ('PWM', 'pwm'),
        ('Power Management', 'pwr'),
    ]

With items documented adding a legend to the diagram is done with a single line of code::

    pinout_diagram.add_legend(-160, 310, 225, 'legend legend-labels', label_categories)


Set default label values
------------------------

.. figure:: _static/label_dimensions.*

   Label dimensions 

Labels have several settings that control their size and appearance. These values can be applied per label, however most labels are likely to share common traits. Default values exist to serve this requirement in the form of class variables. Setting them is as simple as assigning a new value::

    diagram.Label.default_width = 70
    diagram.Label.default_height = 25
    diagram.Label.default_gap = 6
    diagram.Label.default_cnr = 3

*Note:* 'gap' is the distance between labels and graphically contains a leader-line. In the instance of the first label it is still present but joins seamlessly onto the pin leader-line.


Create a Pin with Labels
------------------------

This is slow way, included to provide an idea of the steps going on behind the scene::

    pin01 = diagram.Pin(16, 100, -50, 100)

Add associated labels to the pin::

    pin01.add_label('1', 'gpio')
    pin01.add_label('A1', 'analog')
    pin01.add_label('PWM', 'pwm')

*Note*: label width, height, and gap, can be controlled per label by including *width*, *height*, and *gap* arguments `pin01.add_label('A1', 'analog', 50, 25, 26)`.

Add this pin to the diagram::

    pinout_diagram.components.append(pin01)

A Pin *with* its labels can be created with by a single line of code. This method provides the most control over pin and label placements::

    pinout_diagram.add_pin(65, 244, -50, 280, [('AREF', 'pwr')])


Create multiple Pins and Labels
-------------------------------

Electronics hardware typically groups pins into 'headers' - groups of evenly spaced pins. *pinout* takes advantage of this and provides a convenient way to add pins and labels to the diagram. 

Pin and label data can be documented in a dict::

    pin_headers = [
        {
            # LHS header - lower half
            'pin_coords': (16, 130),
            'label_coords': (-50 ,130),
            'pitch': 30,
            'labels': [
                [('Vcc', 'pwr')], 
                [('2', 'gpio'),('A2', 'analog')],
            ]
        },{
            # RHS header
            'pin_coords': (204, 100),
            'label_coords': (270 ,100),
            'pitch': 30,
            'labels': [
                [('8', 'gpio'),('A3', 'analog')], 
                [('7', 'gpio'),('A3', 'analog'), ('PWM','pwm')],
                [('GND', 'pwr')],
            ]
        },{
            # Lower header - remaining 3 pins
            'pin_coords': (95, 244),
            'label_coords': (270 ,280),
            'pitch': 30,
            'labels': [
                [('4', 'gpio'),('ADC', 'analog')], 
                [('5', 'gpio'),('ADC', 'analog'), ('PWM','pwm')],
                [('6', 'gpio'),('PWM', 'pwm', 70, 25, 82)],
            ]
        }
    ]

Single Pins can be included in this data structure. 'pitch' can be excluded in these instances.

With data neatly documented, adding it to the diagram is straight forward::

    for header in pin_headers:
        pinout_diagram.add_pin_header(header)

Pin locations in each header are calculated top-to-bottom or left-to-right depending on label coordinates in relation to pin coordinates.

Export the diagram
------------------


The final diagram can be exported as a graphic in SVG format and should match the finished diagram shown here. This format and excellent for high quality printing but still an effecient size for web-based usage::

    pinout_diagram.export('get_started_diagram.svg', overwrite=True)

    # expected output:
    # > 'get_started_pinout.svg' exported successfully.

.. figure:: _static/quick_start_diagram.*

    The finished diagram from this tutorial.

    
The most convenient method of viewing the newly exported SVG file is with your browser.


Next steps
----------

This guide has glossed over many argument definitions used in functions. Experimenting with changing values and re-exporting the diagram will quickly reveal their purpose. All function are documented in the :ref:`modules` section.

Rerunning this guide with no css file added to the diagram will create an auto-generated stylesheet. It makes some educated guesses about approriate styles and is a handy method for 'bootstrapping' a stylesheet for your own diagrams.

Depending on you intended usage linking (instead of embedding) the stylesheet and/or image might be desirable. Set `embed=False` when adding these components to achieve this outcome. *Note:* When linking, relative URLs for stylesheets and images are relative to the exported diagram file. When embedding these URLs are relative to the current working directory (the directory you run the script from).

**TIP:** Embedding the image and styles allows the SVG display correctly in InkScape. This might be an appealing work-flow option for encorporating the diagram into other media.