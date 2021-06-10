from pinout import config
from pinout.components import leaderline as lline

from arduino_components import Label, FirstLabel, LabelLast


# Right header
lbl_first = {
    "body": {"width": 80, "height": 20},
}
lbl = {"body": {"width": 80, "height": 20, "x": 2}}

# Left header
lbl_first_sm = {"body": {"width": 50, "height": 20}}
lbl_sm = {"body": {"width": 30, "height": 20, "x": 0, "y": 0}}

# LEDs
led = {
    "body": {
        "width": 120,
        "height": 20,
    },
}


#########################################################
#
# Legend
#
#########################################################

legend = [
    ("Ground", "gnd"),
    ("Power", "pwr"),
    ("LED", "led"),
    ("Internal Pin", "internal"),
    ("SWD Pin", "swd"),
    ("Digital Pin", "digital"),
    ("Analog Pin", "analog"),
    ("Other Pin", "other"),
    ("Microcontroller's Port", "mu-port"),
    ("Default", "default"),
]


#########################################################
#
# Header: Right-hand-side
#
#########################################################

header_rhs = [
    [
        ("D12", "digital", lbl_first),
        ("GPIO4", "mu-port", lbl),
        ("CIPO", "default", lbl),
    ],
    [
        ("D11", "digital", lbl_first),
        ("GPIO7", "mu-port", lbl),
        ("CIPI", "default", lbl),
    ],
    [
        ("D10", "digital", lbl_first),
        ("GPIO5", "mu-port", lbl),
    ],
    [
        ("D9", "digital", lbl_first),
        ("GPIO21", "mu-port", lbl),
    ],
    [
        ("D8", "digital", lbl_first),
        ("GPIO20", "mu-port", lbl),
    ],
    [
        ("D7", "digital", lbl_first),
        ("GPIO19", "mu-port", lbl),
    ],
    [
        ("D6", "digital", lbl_first),
        ("GPIO18", "mu-port", lbl),
    ],
    [
        ("D5", "digital", lbl_first),
        ("GPIO17", "mu-port", lbl),
    ],
    [
        ("D4", "digital", lbl_first),
        ("GPIO16", "mu-port", lbl),
    ],
    [
        ("D3", "digital", lbl_first),
        ("GPIO15", "mu-port", lbl),
    ],
    [
        ("D2", "digital", lbl_first),
        ("GPIO25", "mu-port", lbl),
    ],
    [
        ("GND", "gnd", lbl_first),
    ],
    [
        ("RESET", "other", lbl_first),
        ("RESET", "mu-port", lbl),
    ],
    [
        ("RX", "digital", lbl_first),
        ("GPIO1", "mu-port", lbl),
    ],
    [
        ("TX", "digital", lbl_first),
        ("GPIO0", "mu-port", lbl),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs = [
    [
        ("D13", "digital", lbl_first),
        ("GPIO6", "mu-port", lbl),
        ("SCK", "default", lbl),
    ],
    [
        ("+3V3", "pwr", lbl_first),
    ],
    [
        ("AREF", "other", lbl_first),
        ("PA03", "mu-port", lbl),
    ],
    [
        ("D14", "digital", lbl_first_sm),
        ("A0", "analog", lbl_sm),
        ("GPIO26", "mu-port", lbl),
        ("A0/DAC0", "default", lbl),
    ],
    [
        ("D15", "digital", lbl_first_sm),
        ("A1", "analog", lbl_sm),
        ("GPIO27", "mu-port", lbl),
        ("A1", "default", lbl),
    ],
    [
        ("D16", "digital", lbl_first_sm),
        ("A2", "analog", lbl_sm),
        ("GPIO28", "mu-port", lbl),
        ("A2", "default", lbl),
    ],
    [
        ("D17", "digital", lbl_first_sm),
        ("A3", "analog", lbl_sm),
        ("GPIO29", "mu-port", lbl),
        ("A3", "default", lbl),
    ],
    [
        ("D18", "digital", lbl_first_sm),
        ("A4", "analog", lbl_sm),
        ("GPIO12", "mu-port", lbl),
        ("A4", "default", lbl),
    ],
    [
        ("D19", "digital", lbl_first_sm),
        ("A5", "analog", lbl_sm),
        ("GPIO13", "mu-port", lbl),
        ("A5", "default", lbl),
    ],
    [
        ("D20", "digital", lbl_first_sm),
        ("A6", "analog", lbl_sm),
        ("A6", "default show-leader", lbl),
    ],
    [
        ("D21", "digital", lbl_first_sm),
        ("A7", "analog", lbl_sm),
        ("A7", "default show-leader", lbl),
    ],
    [
        ("+5V", "pwr", lbl_first),
    ],
    [
        ("RESET", "other", lbl_first),
        ("QSPI_CSn", "default", lbl),
    ],
    [("GND", "gnd", lbl_first)],
    [("VIN", "pwr", lbl_first)],
]


#########################################################
#
# LED labels
#
#########################################################

leds = [
    [("Power", "led", led)],
    [("LED_BUILTIN", "led", led)],
]


#########################################################
#
# Text blocks
#
#########################################################

title_1 = [
    '<tspan class="h1">Arduino</tspan>',
    '<tspan class="h1">Nano RP2024 Connect</tspan>',
]
para_1 = [
    '<tspan class="p">Pinout diagram created with <tspan class="italic">pinout (v0.0.10)</tspan></tspan>',
    '<tspan class="p">A Python package for creating pinout diagrams.</tspan>',
    '<tspan class="p"><tspan class="strong"><a href="https://pinout.readthedocs.io">pinout.readthedocs.io</a></tspan></tspan>',
]
para_2 = [
    '<tspan class="p">NOTE: This is not official documentation.</tspan>',
    '<tspan class="p">Diagram aesthetics from Arduino docs.</tspan>',
    '<tspan class="p"><tspan class="strong"><a href="https://www.arduino.cc/">https://www.arduino.cc/</a></tspan></tspan>',
]
