legend = [
    ("Analog", "analog"),
    ("I2C", "i2c"),
    ("GPIO", "gpio"),
    ("Touch", "touch"),
    ("PWM", "pwm"),
    ("Power", "pwr"),
    ("Ground", "gnd"),
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
    [
        ("3", "gpio"),
        ("PWM", "pwm"),
    ],
]

lower_header_out = [
    [
        ("VBAT", "pwr"),
    ],
    [
        ("3.3V", "pwr"),
    ],
    [
        ("GND", "gnd"),
    ],
    [
        ("AREF", "pwr"),
    ],
]
lower_header_in = [
    [
        ("A2", "analog"),
        ("TOUCH", "touch"),
    ],
    [
        ("PWM", "pwm"),
    ],
    [
        ("6", "gpio"),
        ("SDA1", "i2c"),
    ],
    [
        ("A5", "analog"),
        ("SCL1", "i2c"),
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
        ("RESET", "reset"),
    ],
    [
        ("8", "gpio"),
        ("A6", "analog"),
    ],
]


# Text

title = "<tspan class='h1'>Pinout sample: Section pull-out</tspan>"

description = """Pinout is a Python tool kit to assist with documentation of electronic hardware. 
This sample demonstrates documenting a section of hardware. 
More info at <tspan class='italic strong'>pinout.readthedocs.io</tspan>"""

section_a_text = """<tspan class='section_title'>Section A</tspan>
Detail of double row header."""