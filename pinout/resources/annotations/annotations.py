###########################################
#
# Example script to build a pinout diagram
# with some annotation labels
#
###########################################

from pinout.diagram import Diagram
from pinout.components import Component


# Create a new diagram
diagram = Diagram()


# annotations_01
# --------------

# Create a child diagram
annotations_01 = diagram.add(Diagram())

# Supply config settings.
annotations_01.add_config("annotations_config.yaml")

# Add the hardware board image
annotations_01.add_image("hardware_board.svg", width=220, height=300)

# Add some annotations.
annotations_01.add_annotation(["Micro", "USB-C"], x=110, y=24)
annotations_01.add_annotation("Onboard LED", x=87, y=85)
annotations_01.add_annotation("STM32L0 \nSingle core Cortex-M0+", x=110, y=185)
annotations_01.add_annotation("Additional 4 pin header", x=110, y=284)

# If your needs are simple and some care is taken with the config this might be adequate, but probably not ideal for most situations.


# annotations_02
# --------------

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

# As an alternative component config can be documented in the YAML config file and reference here.
annotations_02.add_annotation(
    ["Micro", "USB-C"],
    x=110,
    y=24,
    scale=(-1, -1),
    config=annotations_02.config["anno_2_usb"],
)
# NOTE: The sign of offset can be overridden by supplying a 'scale=(<+/-1>,<+/-1>)'


# annotations_03
# --------------

# This diagram will be position below 'annotations_02'
annotations_03 = diagram.add(Diagram(y=710))
annotations_03.add_config("annotations_config.yaml")
annotations_03.add_image("hardware_board.svg", width=220, height=300)

# Patch config["annotation"] with config["anno_3_defaults"].
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

# Pin header
annotations_03.add_annotation(
    "Additional 4 pin header",
    x=110,
    y=284,
    config=annotations_03.config["anno_3_header"],
)


diagram.export("annotated_diagrams.svg", overwrite=True)