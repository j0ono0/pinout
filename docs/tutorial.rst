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


Document measurments
--------------------

Taking some critical measurements of the hardware image before starting will streamline processes and save adjusting by trial-and-error later. Where pins are arranged in 'headers' (a line of evenly spaced pins) the *PinLabelSet* class can be used to automate pin and label placement.

.. figure:: _static/quick_start_measurements_left_header.*

- **x, y**: Coordinates of the first pin in the header.
- **pitch**: Distance between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. *TIP*: (30, 0) creates a horizontal header.
- **offset**: **Relative to the pin's (x, y) coodinates**. Locates the start position for a row of labels.
- **labels**: Data that documents each label and its position in the header. Each list within 'labels' represents a pin in the header. Each entry within those lists becomes a label.  

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
    
**Note on coodinates**: SVG format sets (0, 0) as top-left with increasing x and y values moving to the right and down respectively. Component placement in pinout is made from an arbitrary (0, 0) location. The final diagram size and boundaries are calculated on export ensuring all components are visible - ie negative coordinates do not risk being outside the final diagram boundaries.

In this tutorial all (x, y) coordinates are relative to the hardware images's top-left corner which is positioned at (0, 0).


Create a new diagram
--------------------
::

    diagram = diagram.Diagram()


Add a config file
-----------------
Many design settings in *pinout* can be overridden by editing properties of a component directly or by supplying a 'default' value via a configuration file. The latter is ideal for consistency across the entire diagram.

The configuration file is in YAML format. 'quick_start_config.yaml' demonstrates the format with a few example settings::

    diagram.add_config("quick_start_config.yaml") 

Loading the config file should be done before other components are added as values may be referenced at that time.


Add a stylesheet
----------------

Strictly speaking this step is optional as *pinout* will create a stylesheet for you in the absence of one but relies on some guess work so output may vary. To ensure a predictable outcome add `quick_start_styles.css` to the diagram::
    
    diagram.add_stylesheet("quick_start_styles.css", embed=True)


Add an image
------------

Adding an image is similar to the stylesheet. The extra arguments are *x*, *y*, *width*, and *height*. All function are documented with more detail in the :ref:`modules` section::

    diagram.add_image("quick_start_hardware.png", width=220, height=260, embed=True)


Add a legend
------------

The legend documents pin-label categories. These categories are graphically represented by styles documented in the previously added stylesheet. The first step in creating a legend is to create a list that *tags* category *names*. this list is stored in the configuration file and has already been done for this tutorial in 'quick_start_config.yaml'. All that is left to do is add the graphical representation into the diagram::

    diagram.add_legend(x=260, y=236, tags="legend")


Create pin labels
-----------------
With pin-labels already documented and grouped in to headers they can now be added to the diagram::

    for header in pin_headers:
        diagram.add_pinlabelset(**header)


Export the diagram
------------------


The final diagram can be exported as a graphic in SVG format and should match the finished diagram shown here. This format is excellent for high quality printing but still an effecient size for web-based usage::

    diagram.export("quick_start_diagram.svg", overwrite=True)

    # expected output:
    # > 'quick_start_diagram.svg' exported successfully.

.. figure:: _static/quick_start_diagram.*

    The finished diagram from this tutorial.

    
The most convenient method of viewing the newly exported SVG file is with your browser.


Next steps
----------

This guide has glossed over many argument and configuration definitions. Experimenting with changing values and re-exporting the diagram will quickly reveal their purpose. All function are documented in the :ref:`modules` section.

Rerunning this guide with no css file added to the diagram will create an auto-generated stylesheet. It makes some educated guesses about approriate styles and is a handy method for 'bootstrapping' a stylesheet for your own diagrams.

Depending on you intended usage, linking (instead of embedding) the stylesheet and/or image might be desirable. Set `embed=False` when adding these components to achieve this outcome. *Note:* When linking, relative URLs for stylesheets and images are relative to the exported diagram file. When embedding these URLs are relative to the current working directory (the directory you run the script from).

**TIP:** Embedding the image and styles allows the SVG display correctly in InkScape. This might be an appealing work-flow option for encorporating the diagram into other media.