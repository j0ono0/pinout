.. _Annotation samples:

Annotations
===========


Sample code for this section is included with *pinout* and can be duplicated from the commandline::

    py -m pinout.file_manager --duplicate annotations


Create a new diagram to get started. This will server as a container for several 'child' diagrams so we can see them all together at the end. Normally you might add components directly into this base diagram::

    diagram = Diagram()


Basic inclusion
---------------

To get started we will build a diagram using default configurations with just a few additional settings. These will be applied to all annotations labels. Note that `diagram.add()` returns the component created allowing us to create + add in a single action.::

    annotations_01 = diagram.add(Diagram())

An image and annotations can now be added to *annotations_01*::

    # Add image
    annotations_01.add_image("hardware_board.svg", width=220, height=300)

    # Add annotations
    # NOTE: multiple lines can be created with a line return '\n' or supplying text in a list
    annotations_01.add_annotation(["Micro", "USB-C"], x=110, y=24)
    annotations_01.add_annotation("Onboard LED", x=87, y=85)
    annotations_01.add_annotation("STM32L0 \nSingle core Cortex-M0+", x=110, y=185)
    annotations_01.add_annotation("Additional 4 pin header", x=110, y=284)

If your needs are simple and some care is taken with the config this might be adequate, but probably not ideal for most situations.

By adding an export command at the bottom of the file progress can now be exported::

    diagram.export("annotated_diagrams.svg", overwrite=True)


.. figure:: /_static/annotations_simple.*

.. important::

    Keep this as the LAST line in your script! Anthing added after won't appear in the export.


Enhanced configuration
----------------------

Adding another diagram into the base diagram is almost identical. A 'y' value has been included to move this one below annotations_01::

    annotations_02 = diagram.add(Diagram(y=380))
    annotations_02.add_config("annotations_config.yaml")
    annotations_02.add_image("hardware_board.svg", width=220, height=300)

Modifying each annotation as it is being added is possible and done by supplying configuration attributes in the python script. These values will override any configurations supplied via an added YAML file. The format must be a dictorary and match the 'annotation' entry found in config.yaml (the default configuration file)::

    annotations_02.add_annotation(
        "Onboard LED",
        x=87,
        y=85,
        config={
            "offset": (163, 40),
            "leaderline": {
                "rect": {
                    "width": 36,
                    "height": 36,
                    "fill_opacity": 0,
                }
            },
        },
    )
    annotations_02.add_annotation(
        "STM32L0 \nSingle core Cortex-M0+", x=110, y=185, config={"offset": (-140, 0)}
    )
    annotations_02.add_annotation(
        "Additional 4 pin header",
        x=110,
        y=284,
        config={
            "leaderline": {"rect": {"width": 134, "height": 46, "fill_opacity": 0}},
            "offset": (140, -46),
        },
    )

Supplying configs as a dict can get frustrating to read and write for complex components. As an alternative component config can be documented in the config file and reference here::

    annotations_02.add_annotation(
        ["Micro", "USB-C"],
        x=110,
        y=24,
        scale=(-1, -1),
        config=annotations_02.config["anno_2_usb"],
    )
    # NOTE: config["offset'] can be overridden by supplying 
    # 'scale=(<+/-1>,<+/-1>)' to flip a component's layout.'

Exporting the diagram will now display two diagrams. The second more graphically nuanced. 

.. figure:: /_static/annotations_enhanced.*


Further customisations
----------------------

Whilst aspects of this component are set there is still scope for broad customisations to suit the character of a product or publication.

Create our third and final diagram, adding it to the base diagram::

    # This diagram will be position below 'annotations_02'
    annotations_03 = diagram.add(Diagram(y=710))
    annotations_03.add_config("annotations_config.yaml")
    annotations_03.add_image("hardware_board.svg", width=220, height=300)

To keep the file structure simple for this demonstration an alternative config ('anno_3_defaults') has been included in 'annotations_config.yaml'. We can override the existing config["annotation"] with this one::

    annotations_03.patch_config(
    annotations_03.config, {"annotation": annotations_03.config["anno_3_defaults"]}
    )

With all unique component configurations documented in the config file the python script is neat and easy to read and write::

    # USB connection
    annotations_03.add_annotation(
        "Micro USB-C", x=110, y=24, config=annotations_03.config["anno_3_usb"]
    )

    # Microprocessor
    orange = [246, 148, 30]
    annotations_03.add_annotation(
        "STM32L0 \n Single core Cortex-M0+ \n32kb Flash \n USART, SPI, I2C, USB",
        x=110,
        y=171,
        config=annotations_03.config["anno_3_mc"],
    )

    # Onboard LED
    annotations_03.add_annotation(
        "Onboard LED", x=87, y=85, config=annotations_03.config["anno_3_led"]
    )

    # Pin header
    annotations_03.add_annotation(
        "Additional 4 pin header",
        x=110,
        y=284,
        config=annotations_03.config["anno_3_header"],
    )

Doing a final export will now display all three versions for comparison.

.. figure:: /_static/annotations_custom.*