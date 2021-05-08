###########################################
#
# Example script to build a pinout diagram
# with some annotation labels
#
###########################################

from pinout.diagram import Diagram
from pinout.components import Component


# Create a new diagram
# This will server as a container for several 'child' diagrams
# for a single diagram you would normally add component directly into this object.
diagram = Diagram(tag="annotation_sample")


#
# annotations_01
# --------------
#
# Annotation labels using only shared common settings
#


# Create a child diagram
# NOTE: This nesting of diagrams is not normally a necessary but done here so multiple boards can be presented in a single graphic
annotations_01 = diagram.add(Diagram())

# Supply config settings. These override default settings
annotations_01.add_config("annotations_config.yaml")

# Add the hardware board image
annotations_01.add_image("hardware_board.svg", width=220, height=300)

# Add some annotations.
# These are using ONLY default settings. Outcome is functional but not optimal.
# NOTE: multiple lines can be created with '\n' or supplying text in a list
annotations_01.add_annotation(["Micro", "USB-C"], x=110, y=24)
annotations_01.add_annotation("Onboard LED", x=87, y=85)
annotations_01.add_annotation("STM32L0 \nSingle core Cortex-M0+", x=110, y=185)
annotations_01.add_annotation("Additional 4 pin header", x=110, y=284)

# If your needs are simple and some care is taken with the config this might be adequate, but probably not ideal for most situations.

#
# annotations_02
# --------------
#
# Annotation labels with minimal additional config
# to aid with layout flexibilty and clarity
#

# This diagram will be position below 'annotations_01'
annotations_02 = diagram.add(Diagram(y=380))
annotations_02.add_config("annotations_config.yaml")
annotations_02.add_image("hardware_board.svg", width=220, height=300)

# Config can be supplied per annotation in the form of a dict matching the config.yaml annotation entry
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

# Supplying configs as a dict can get frustrating to read and write for complex components. As an alternative component config can be documented in the YAML config file and reference here.

annotations_02.add_annotation(
    ["Micro", "USB-C"],
    x=110,
    y=24,
    scale=(-1, -1),
    config=annotations_02.config["anno_2_usb"],
)
# NOTE: The sign of offset can be overridden by supplying a 'scale=(<+/-1>,<+/-1>)'

#
# annotations_03
# --------------
#
# Creative flexibilty within the set svg markup structure
# Whilst aspects of this component are set there
# is still scope for broad customisations.
#

# This diagram will be position below 'annotations_02'
annotations_03 = diagram.add(Diagram(y=710))
annotations_03.add_config("annotations_config.yaml")
annotations_03.add_image("hardware_board.svg", width=220, height=300)

# An optional step due to using a single config file: we are going to patch config["annotation"] with config["anno_3_defaults"]. Usually you might use two separate YAML files.
annotations_03.patch_config(
    annotations_03.config, {"annotation": annotations_03.config["anno_3_defaults"]}
)

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

annotations_03.add_annotation(
    "Additional 4 pin header",
    x=110,
    y=284,
    config=annotations_03.config["anno_3_header"],
)


diagram.export("annotated_diagram.svg", overwrite=True)
