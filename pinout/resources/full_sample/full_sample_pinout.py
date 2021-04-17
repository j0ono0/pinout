###########################################
#
# Example script to build a pinout diagram
# Includes examples of all features
#
###########################################

from pinout.diagram import Diagram
from pinout import file_manager

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
            [("1", "gpio"), ("Lc1a", "comms", (84, 0))],
            [("2", "gpio"), ("Lc2a", "analog"), ("Lc2b", "led")],
            [("RESET", "pwr", (72, 0), 132)],
        ],
    },
    # Right side vetical header
    {
        "x": 204,
        "y": 105,
        "pitch": (0, 30),
        "offset": (76, 0),
        "labels": [
            [("Vcc", "pwr", (72, 0), 132)],
            [("GND", "pwr", (72, 0), 132)],
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


# Override default config with user supplied values
file_manager.load_config("full_sample_config.yaml")

# Create a new diagram object
diagram = Diagram(tags="full_sample")

# Link external resources
diagram.add_stylesheet("full_sample_styles.css", embed=True)
diagram.add_image("full_sample_hardware.png", width=220, height=300, embed=True)

# Create components
diagram.add_legend(x=-274, y=400, tags="legend")
for data in pindata:
    diagram.add_pinlabelset(**data)

# Export final SVG diagram
diagram.export("full_sample_diagram.svg", True)