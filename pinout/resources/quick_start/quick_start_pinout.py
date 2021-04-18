from pinout import diagram
from pinout import file_manager

# Pin label information grouped into dicts that render sets of labels
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
    {
        # RHS header
        "x": 204,
        "y": 100,
        "pitch": (0, 30),
        "offset": (55, 0),
        "labels": [
            [("GND", "pwr", (0, 0), 155)],
            [("7", "gpio"), ("A3", "analog")],
            [("6", "gpio"), ("A2", "analog"), ("PWM", "pwm")],
        ],
    },
    {
        # Lower header
        "x": 65,
        "y": 244,
        "pitch": (30, 0),
        "offset": (-104, 40),
        "labels": [
            [("RESET", "pwr", (0, 0), 155)],
            [("3", "gpio"), ("ADC0", "analog")],
            [("4", "gpio"), ("ADC1", "analog"), ("PWM", "pwm")],
            [("5", "gpio"), ("PWM", "pwm", (-100, 0))],
        ],
    },
]

# Override default config with user supplied values
file_manager.load_config("quick_start_config.yaml")

# Create a new diagram
diagram = diagram.Diagram()

# Add a stylesheet
diagram.add_stylesheet("quick_start_styles.css", embed=True)

# Add an image
diagram.add_image("quick_start_hardware.png", width=220, height=260, embed=True)

# Add a legend. Note, categories are documented in config.yaml
diagram.add_legend(x=260, y=236, tags="legend")

# Create pinout labels
for header in pin_headers:
    diagram.add_pinlabelset(**header)

# Export the finished diagram
diagram.export("quick_start_diagram.svg", overwrite=True)
