legend = [
    ("Analog", "analog"),
    ("Communication", "comms"),
    ("Ground", "gnd"),
    ("GPIO", "gpio"),
    ("Touch", "touch"),
    ("Power", "pwr"),
    ("PWM", "pwm"),
]

# Pinlabels

left_header = [
    [
        ("0", "gpio"),
        ("A0", "analog"),
        ("MISO", "comms"),
    ],
    [
        ("1", "gpio"),
        ("MOSI", "comms", {"body": {"x": 92}}),
    ],
    [
        ("2", "gpio"),
        ("A1", "analog"),
        ("SCLK", "comms"),
    ],
]

lower_header = [
    [
        ("3", "gpio"),
        ("PWM", "pwm"),
    ],
    [
        ("4", "gpio"),
        ("A2", "analog"),
        ("TOUCH", "touch"),
    ],
    [
        ("5", "gpio"),
        ("A3", "analog"),
    ],
]

right_header = [
    [
        ("Vcc", "pwr"),
    ],
    [
        ("GND", "gnd"),
    ],
    [
        ("6", "gpio"),
        ("A4", "analog"),
        ("TOUCH", "touch"),
    ],
]


# Text

title = "<tspan class='h1'>Pinout Quick start</tspan>"

description = """Python tool kit to assist with 
documentation of electronic hardware. 
More info at <tspan class='italic strong'>pinout.readthedocs.io</tspan>"""
