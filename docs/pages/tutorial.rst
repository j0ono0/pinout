.. _tutorial:

Tutorial
===============

This tutorial walks through the main features available in *pinout*. If you have not installed *pinout* already please read the :ref:`install` section. This tutorial duplicates code from *quick_start_pinout.py*. To access a copy of this file and other resources see :ref:`quickstart`.

.. figure:: /_static/quick_start_diagram.*

   The finished diagram from this tutorial.


Import modules
--------------

Start by importing the pinout diagram module and creating a new diagram object::

    from pinout import layout


Document measurments
--------------------

Taking some critical measurements of the hardware image before starting will streamline processes and save adjusting by trial-and-error later. Where pins are arranged in 'headers' (a line of evenly spaced pins) the *PinLabelSet* class can be used to automate pin and label placement.

.. figure:: /_static/quick_start_measurements_left_header.*

- **x, y**: Coordinates of the first pin in the header.
- **pitch**: Distance between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. *TIP*: (30, 0) creates a horizontal header.
- **offset**: **Relative to the pin's (x, y) coodinates**. Locates the start position for a row of labels.
- **labels**: Data that documents each label and its position in the header. Each list within 'labels' represents a pin in the header. Each entry within those lists becomes a label. Label entries must include a 'title', 'tag', and optionally a dict of custom configurations.

These details are documented in a dict. Multiple headers can be grouped into a list for convenient processing later.Note some labels are demonstrated with customisations::
    
    # Custom pinlabel configuration
    long_label_config = {"label": {"rect": {"width": 108}}}

    pin_headers = [
        {
            # LHS header
            "x": 16,
            "y": 100,
            "pitch": (0, 30),
            "offset": (-58, 0),
            "labels": [
                [("Vcc", "pwr", long_label_config)],
                [("1", "gpio"), ("A1", "analog")],
                [("2", "gpio"), ("PWM", "pwm", {"offset": (66, 0)})],
            ],
        },
        # x2 more headers are included in 'quick_start_pinout.py'
    ]
    
**Note on coodinates**: SVG format sets (0, 0) as top-left with increasing x and y values moving to the right and down respectively. Component placement in pinout is made from an arbitrary (0, 0) location. The final diagram size and boundaries are calculated on export ensuring all components are visible - ie negative coordinates do not risk being outside the final diagram boundaries.

In this tutorial all (x, y) coordinates are relative to the hardware images's top-left corner which is positioned at (0, 0).


Create a new diagram
--------------------
::

    diagram = layout.Diagram()


Add a config file
-----------------
Many design settings in *pinout* can be overridden by supplying properties to component directly or by supplying a 'default' value via a configuration file. The latter is ideal for consistency across the entire diagram.

The configuration file is in YAML format. 'quick_start_config.yaml' demonstrates the format with a few example settings::

    diagram.add_config("quick_start_config.yaml") 

Loading the config file should be done before other components are added as values may be referenced at that time. 

.. important::

    Tags must be supplied in a YAML config file to apply color coding to pin-labels - no default is provided by *pinout*.

Add an image
------------

A width and height must be supplied (*pinout* does no auto detect this dimensions). It is recommended to use images at a **1:1 ratio** to simplify documenting component locations. Optionally 'x' and 'y' attributes can be supplied to position the top-left of the images to more suitable coordinates::

    diagram.add_image("quick_start_hardware.png", width=220, height=260, embed=True)


Add a legend
------------

The legend documents pin-label categories. Content to popluate the legend is sourced 'quick_start_config.yaml'. All that is left to do is add the legend, with its coordinates, to the diagram::

    diagram.add_legend(x=250, y=200)


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

.. figure:: /_static/quick_start_diagram.*

    The finished diagram from this tutorial.

    
The most convenient method of viewing the newly exported SVG file is with your browser.


Next steps
----------

This guide has glossed over many attribute and configuration definitions. Experimenting with changing values and re-exporting the diagram will quickly reveal their purpose. All function are documented in the :ref:`modules` section.

The default config.yaml file can be duplicated and makes a good resource of what attributes can be modified::

    py -m pinout.file_manager --duplicate config

Depending on you intended usage, linking (instead of embedding) the image might be desirable. Set `embed=False` when adding an image to achieve this outcome. *Note:* When linking, URLs are relative to the exported diagram file. When embedding these URLs are relative to the current working directory (the directory you run the script from).

**TIP:** Embedding the image allows the SVG display correctly in InkScape. This might be an appealing work-flow option for encorporating the diagram into other media.

A more feature-rich example is also available that extends this tutorial with more varied examples::

    py -m pinout.file_manager --duplicate full_sample