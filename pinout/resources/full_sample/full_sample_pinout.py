###########################################
#
# Example script to build a pinout diagram
# Includes examples of all features
#
###########################################

from pinout.diagram import Diagram

# Custom pinlabel config
long_label_cfg = {"offset": (74, 0), "label": {"rect": {"width": 110}}}

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
        "offset": (-122, -145),
        "labels": [
            [("b", "led"), ("AUX_b", "pwm"), ("PWM", "pwm")],
        ],
    },
]


# Create a new diagram object
diagram = Diagram(tag="full_sample")

# Override default config with user supplied values
diagram.add_config("full_sample_config.yaml")

# Patch config with style tags
diagram.add_config("full_sample_config_tags.yaml")

# Link external resources
diagram.add_image("full_sample_hardware.png", width=220, height=300, embed=True)

# Add pinlabel legend
diagram.add_legend(
    x=-242, y=400, categories=["analog", "comms", "gpio", "led", "pwm", "pwr"]
)

# Add pinlabels
for data in pindata:
    diagram.add_pinlabelset(**data)

# Export final SVG diagram
diagram.export("full_sample_diagram.svg", True)