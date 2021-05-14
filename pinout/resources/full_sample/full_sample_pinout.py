###########################################
#
# Example script to build a pinout diagram
# Includes examples of all features
#
###########################################

from pinout.diagram import Diagram
from pinout import components as cmpt
from pinout import elements as elem

# Custom pinlabel config
long_label_cfg = {"offset": (66, 0), "label": {"rect": {"width": 108}}}

# Pin label information grouped into dicts that render sets of labels
pindata = [
    # Left side vetical header
    {
        "x": 16,
        "y": 105,
        "pitch": (0, 30),
        "offset": (-76, 0),
        "labels": [
            [("0", "gpio"), ("Lb0a", "gpio"), ("Lb03", "comms")],
            [("1", "gpio"), ("Lc1a", "comms")],
            [("2", "gpio"), ("Lc2a", "analog"), ("Lc2b", "led")],
            [("RESET", "pwr", long_label_cfg)],
        ],
    },
    # Right side vetical header
    {
        "x": 204,
        "y": 105,
        "pitch": (0, 30),
        "offset": (76, 0),
        "labels": [
            [("Vcc", "pwr", long_label_cfg)],
            [("GND", "pwr", long_label_cfg)],
            [("3", "gpio"), ("Lc2a", "analog"), ("Lc2b", "led")],
            [("4", "gpio"), ("Lc3a", "analog")],
        ],
    },
    # Bottom horizontal header (Left half)
    {
        "x": 65,
        "y": 284,
        "pitch": (30, 0),
        "offset": (-125, 40),
        "labels": [
            [("3", "gpio"), ("Lc2a", "analog"), ("Lc2b", "led")],
            [("4", "gpio"), ("Lc2a", "pwm"), ("Lc2b", "led")],
        ],
    },
    # Bottom horizontal header (Right half)
    {
        "x": 155,
        "y": 284,
        "pitch": (-30, 0),
        "offset": (125, 40),
        "labels": [
            [("6", "gpio"), ("Lc3a", "analog")],
            [("5", "gpio"), ("Lc2a", "pwm"), ("Lc2b", "led")],
        ],
    },
    # Left interior pin
    {
        "x": 47,
        "y": 80,
        "offset": (-107, -100),
        "labels": [
            [("a", "led"), ("AUX_a", "analog")],
        ],
    },
    # Right interior pin
    {
        "x": 62,
        "y": 95,
        "pitch": (30, 0),
        "offset": (-122, -145),
        "labels": [
            [("b", "led"), ("AUX_b", "pwm"), ("PWM", "pwm")],
        ],
    },
]

diagram = Diagram(tag="diagram")

# Override default config with user supplied values
# This file includes 'tag' information to style pinlabels
diagram.add_config("full_sample_config.yaml")

# Create the 'main' panel
panel_main = diagram.add(cmpt.Panel(x=0, y=0, width=500, height=500, tag="panel__main"))


# Add and embed external image
panel_main.add(
    elem.Image("full_sample_hardware.png", width=220, height=300, embed=True)
)


# Add pinlabels
pinlabel_config = cmpt.Component.config["pinlabel"]
for data in pindata:
    panel_main.add(cmpt.PinLabelSet(**data, config=pinlabel_config))

# Add an annotation sample
panel_main.add(
    cmpt.Annotation(
        "USB-C connector  \nHost/Device functionality",
        x=110,
        y=20,
        config=cmpt.Component.config["annotation"],
    )
)

# Add pinlabel legend panel
panel_legend = diagram.add(cmpt.Panel(x=500, y=0, tag="legend__pinlabels"))

panel_legend.add(
    cmpt.Legend(
        x=-234,
        y=380,
        categories=["analog", "comms", "gpio", "led", "pwm", "pwr"],
        config=cmpt.Component.config["legend"],
    )
)

# Calculate left over space
x = panel_legend.x
y = panel_legend.height + 20  # INVESTIGATE: padding not in dimensions???
w = panel_legend.width + 20
h = panel_main.height - panel_legend.height + 30  ### NOTSURE  WHY THIS IS OUT?

panel_text = diagram.add(
    cmpt.Panel(x=x, y=y, width=w, height=h, tag="experimental_text")
)
panel_text.add(
    elem.TextBlock(
        text_content="*pinout* is a Python application \nthat creates SVG diagrams. Development is active \nand ongoing to convert a promising idea \ninto a useful tool to assist \nwith documentation of electronic hardware.",
        x=0,
        y=0,
        width=w,
        height=h,
        config=cmpt.Component.config["label"],
    )
)
# Export final SVG diagram
diagram.export("full_sample_diagram.svg", True)