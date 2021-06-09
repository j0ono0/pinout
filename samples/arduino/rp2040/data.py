from pinout import config
from pinout.components import leaderline as lline

from arduino_components import Label, FirstLabel, LabelLast


cfg = {
    # Right header
    "rgt_first": {"body": {"width": 80, "height": 20}},
    "rgt_single": {"body": {"width": 80, "height": 20}},
    "rgt": {"body": {"width": 80, "height": 20, "x": 2, "y": 0}},
    # Left header
    "lft_first": {"body": {"width": 80, "height": 20, "scale": (-1, 1)}},
    "lft_first_sm": {"body": {"width": 50, "height": 20, "scale": (-1, 1)}},
    "lft": {"body": {"width": 80, "height": 20, "scale": (-1, 1), "x": 2, "y": 0}},
    "lft_sm": {"body": {"width": 30, "height": 20, "scale": (-1, 1), "x": 0, "y": 0}},
    "lft_single": {"body": {"width": 80, "height": 20, "scale": (-1, 1)}},
    # LEDs
    "led": {
        "body": {
            "width": 120,
            "height": 20,
            "scale": (-1, -1),
            "leaderline": lline.Curved("vh"),
        },
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
# cfg\.set_origin((0, 0), (0, 24.6))
# cfg\.set_offset((80, 0), (0, 0))
header_rhs = [
    [
        ("D12", "digital", cfg["rgt_first"]),
        ("GPIO4", "mu-port", cfg["rgt"]),
        ("CIPO", "default", cfg["rgt"]),
    ],
    [
        ("D11", "digital", cfg["rgt_first"]),
        ("GPIO7", "mu-port", cfg["rgt"]),
        ("CIPI", "default", cfg["rgt"]),
    ],
    [
        ("D10", "digital", cfg["rgt_first"]),
        ("GPIO5", "mu-port", cfg["rgt"]),
    ],
    [
        ("D9", "digital", cfg["rgt_first"]),
        ("GPIO21", "mu-port", cfg["rgt"]),
    ],
    [
        ("D8", "digital", cfg["rgt_first"]),
        ("GPIO20", "mu-port", cfg["rgt"]),
    ],
    [
        ("D7", "digital", cfg["rgt_first"]),
        ("GPIO19", "mu-port", cfg["rgt"]),
    ],
    [
        ("D6", "digital", cfg["rgt_first"]),
        ("GPIO18", "mu-port", cfg["rgt"]),
    ],
    [
        ("D5", "digital", cfg["rgt_first"]),
        ("GPIO17", "mu-port", cfg["rgt"]),
    ],
    [
        ("D4", "digital", cfg["rgt_first"]),
        ("GPIO16", "mu-port", cfg["rgt"]),
    ],
    [
        ("D3", "digital", cfg["rgt_first"]),
        ("GPIO15", "mu-port", cfg["rgt"]),
    ],
    [
        ("D2", "digital", cfg["rgt_first"]),
        ("GPIO25", "mu-port", cfg["rgt"]),
    ],
    [
        ("GND", "gnd", cfg["rgt_single"]),
    ],
    [
        ("RESET", "other", cfg["rgt_first"]),
        ("RESET", "mu-port", cfg["rgt"]),
    ],
    [
        ("RX", "digital", cfg["rgt_first"]),
        ("GPIO1", "mu-port", cfg["rgt"]),
    ],
    [
        ("TX", "digital", cfg["rgt_first"]),
        ("GPIO0", "mu-port", cfg["rgt"]),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################


# cfg\.set_origin((0, 0), (0, 24.6))
# cfg\.set_offset((80, 0), (0, 0))
header_lhs = [
    [
        ("D13", "digital", cfg["lft_first"]),
        ("GPIO6", "mu-port", cfg["lft"]),
        ("SCK", "default", cfg["lft"]),
    ],
    [
        ("+3V3", "pwr", cfg["lft_single"]),
    ],
    [
        ("AREF", "other", cfg["lft_first"]),
        ("PA03", "mu-port", cfg["lft"]),
    ],
    [
        ("D14", "digital", cfg["lft_first_sm"]),
        ("A0", "analog", cfg["lft_sm"]),
        ("GPIO26", "mu-port", cfg["lft"]),
        ("A0/DAC0", "default", cfg["lft"]),
    ],
    [
        ("D15", "digital", cfg["lft_first_sm"]),
        ("A1", "analog", cfg["lft_sm"]),
        ("GPIO27", "mu-port", cfg["lft"]),
        ("A1", "default", cfg["lft"]),
    ],
    [
        ("D16", "digital", cfg["lft_first_sm"]),
        ("A2", "analog", cfg["lft_sm"]),
        ("GPIO28", "mu-port", cfg["lft"]),
        ("A2", "default", cfg["lft"]),
    ],
    [
        ("D17", "digital", cfg["lft_first_sm"]),
        ("A3", "analog", cfg["lft_sm"]),
        ("GPIO29", "mu-port", cfg["lft"]),
        ("A3", "default", cfg["lft"]),
    ],
    [
        ("D18", "digital", cfg["lft_first_sm"]),
        ("A4", "analog", cfg["lft_sm"]),
        ("GPIO12", "mu-port", cfg["lft"]),
        ("A4", "default", cfg["lft"]),
    ],
    [
        ("D19", "digital", cfg["lft_first_sm"]),
        ("A5", "analog", cfg["lft_sm"]),
        ("GPIO13", "mu-port", cfg["lft"]),
        ("A5", "default", cfg["lft"]),
    ],
    [
        ("D20", "digital", cfg["lft_first_sm"]),
        ("A6", "analog", cfg["lft_sm"]),
        ("A6", "default show-leader", cfg["lft"]),
    ],
    [
        ("D21", "digital", cfg["lft_first_sm"]),
        ("A7", "analog", cfg["lft_sm"]),
        ("A7", "default show-leader", cfg["lft"]),
    ],
    [
        ("+5V", "pwr", cfg["lft_single"]),
    ],
    [
        ("RESET", "other", cfg["lft_first"]),
        ("QSPI_CSn", "default", cfg["lft"]),
    ],
    [("GND", "gnd", cfg["lft_single"])],
    [("VIN", "pwr", cfg["lft_single"])],
]


#########################################################
#
# LED labels
#
#########################################################
# cfg\.set_origin((0, 0), (112, 0))
# cfg\.set_offset((112, 60), (112, 22))
leds = [
    [("Power", "led", cfg["led"])],
    [("LED_BUILTIN", "led", cfg["led"])],
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
