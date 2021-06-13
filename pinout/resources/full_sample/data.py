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

lhs = [
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
    [
        ("RESET", "pwr"),
    ],
]

btm_lhs = [
    [
        ("3", "gpio"),
        ("A2", "analog"),
        ("PWM", "pwm"),
    ],
    [
        ("4", "gpio"),
        ("A3", "analog"),
    ],
]

btm_rhs = [
    [
        ("6", "gpio"),
        ("PWM", "pwm"),
    ],
    [
        ("5", "gpio"),
        ("A4", "analog"),
        ("PWM", "pwm"),
    ],
]
rhs = [
    [
        ("Vcc", "pwr"),
    ],
    [
        ("GND", "gnd"),
    ],
    [
        ("3", "gpio"),
        ("A6", "analog"),
        ("TOUCH", "touch"),
    ],
    [
        ("4", "gpio"),
        ("A5", "analog"),
    ],
]


aux = [
    [
        ("TOUCH", "touch"),
        ("A7", "analog"),
    ],
    [
        ("TOUCH", "touch"),
    ],
]


# Text

annotation_usb = ["USB-C", "port"]
annotation_led = ["Status", "LED"]

title = "<tspan class='h1'>pinout</tspan>"

desc = """<tspan class='panel__name'>Description</tspan>
Demonstration diagram displaying pin-out
information of non-existent hardware.
Created with version 0.0.10
"""

notes = """<tspan class='panel__name'>Notes</tspan>
<tspan class='italic'>pinout</tspan> is a Python application to assist
with documentation of electronic hardware. 
Development is active with a goal to convert 
a promising idea into a useful tool.

Current release: 
<tspan class='strong'>pinout.readthedocs.io</tspan>"""
