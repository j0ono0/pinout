from pinout import diagram

# Custom pinlabel configuration
long_label_config = {"label": {"rect": {"width": 108}}}

# Pin label information grouped into dicts that render sets of labels
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
    {
        # RHS header
        "x": 204,
        "y": 100,
        "pitch": (0, 30),
        "offset": (58, 0),
        "labels": [
            [("GND", "pwr", long_label_config)],
            [("7", "gpio"), ("A3", "analog")],
            [("6", "gpio"), ("A2", "analog"), ("PWM", "pwm")],
        ],
    },
    {
        # Lower header
        "x": 65,
        "y": 244,
        "pitch": (30, 0),
        "offset": (-107, 40),
        "labels": [
            [("RST", "pwr", long_label_config)],
            [("3", "gpio"), ("ADC0", "analog")],
            [("4", "gpio"), ("ADC1", "analog"), ("PWM", "pwm")],
            [("5", "gpio"), ("PWM", "pwm", {"offset": (66, 0)})],
        ],
    },
]

# Create a new diagram
diagram = diagram.Diagram()

# Override default config with user supplied values
diagram.add_config("quick_start_config.yaml")

# Add an image
diagram.add_image("quick_start_hardware.png", width=220, height=260, embed=True)

# Add a legend. Note, categories are documented in config.yaml
diagram.add_legend(x=250, y=200)

# Create pinout labels
for header in pin_headers:
    diagram.add_pinlabelset(**header)

# Export the finished diagram
diagram.export("quick_start_diagram.svg", overwrite=True)
