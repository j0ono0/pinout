from pinout import config
from pinout.components import leaderline as lline


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

header_rhs_a = [
    [
        ("D19/SCL", "digital", cfg["rgt_first"]),
        ("PC5", "mu-port", cfg["rgt"]),
        ("SCL", "default", cfg["rgt"]),
    ],
    [
        ("D18/SDA", "digital", cfg["rgt_first"]),
        ("PC4", "mu-port", cfg["rgt"]),
        ("SDA", "default", cfg["rgt"]),
    ],
    [
        ("AREF", "other", cfg["rgt_first"]),
    ],
    [
        ("GND", "gnd", cfg["rgt_first"]),
    ],
    [
        ("D13", "digital", cfg["rgt_first"]),
        ("PB5", "mu-port", cfg["rgt"]),
        ("SCK", "default", cfg["rgt"]),
    ],
    [
        ("D12", "digital", cfg["rgt_first"]),
        ("PB4", "mu-port", cfg["rgt"]),
        ("MISO", "default", cfg["rgt"]),
    ],
    [
        ("~D11", "digital", cfg["rgt_first"]),
        ("PB3", "mu-port", cfg["rgt"]),
        ("MOSI", "default", cfg["rgt"]),
    ],
    [
        ("~D10", "digital", cfg["rgt_first"]),
        ("PB2", "mu-port", cfg["rgt"]),
        ("SS", "default", cfg["rgt"]),
    ],
    [
        ("~D9", "digital", cfg["rgt_first"]),
        ("PB1", "mu-port", cfg["rgt"]),
    ],
    [
        ("D8", "digital", cfg["rgt_first"]),
        ("PB0", "mu-port", cfg["rgt"]),
    ],
]

header_rhs_b = [
    [
        ("D7", "digital", cfg["rgt_first"]),
        ("PD7", "default", cfg["rgt"]),
    ],
    [
        ("~D6", "digital", cfg["rgt_first"]),
        ("PD6", "default", cfg["rgt"]),
    ],
    [
        ("~D5", "digital", cfg["rgt_first"]),
        ("PD5", "mu-port", cfg["rgt"]),
    ],
    [
        ("D4", "digital", cfg["rgt_first"]),
        ("PD4", "mu-port", cfg["rgt"]),
    ],
    [
        ("~D3", "digital", cfg["rgt_first"]),
        ("PD3", "mu-port", cfg["rgt"]),
    ],
    [
        ("D2", "digital", cfg["rgt_first"]),
        ("PD2", "mu-port", cfg["rgt"]),
    ],
    [
        ("D1/TX", "digital", cfg["rgt_first"]),
        ("PD1", "mu-port", cfg["rgt"]),
    ],
    [
        ("D0/RX", "digital", cfg["rgt_first"]),
        ("PD0", "mu-port", cfg["rgt"]),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs_a = [
    [("NC", "nc", cfg["lft_first"])],
    [("IOREF", "other", cfg["lft_first"])],
    [
        ("RESET", "other", cfg["lft_first"]),
        ("PC6", "default", cfg["lft"]),
    ],
    [("+3V3", "pwr", cfg["lft_first"])],
    [("+5", "pwr", cfg["lft_first"])],
    [("GND", "gnd", cfg["lft_first"])],
    [("GND", "gnd", cfg["lft_first"])],
    [("VIN", "pwr", cfg["lft_first"])],
]

# Example of using a list comprehension to generate pin data


header_lhs_b = [
    [
        (f"D{14 + i}", "digital", cfg["lft_first_sm"]),
        (f"A{i}", "analog", cfg["lft_sm"]),
        (f"PC{i}", "mu-port", cfg["lft"]),
        (f"ADC[{i}]", "default", cfg["lft"]),
    ]
    for i in range(6)
]

#########################################################
#
# LED labels
#
#########################################################

leds_a = [
    [
        ("RX LED", "led", cfg["led"]),
        # ("PD4", "default", {**cfg["led"], "x": 2, "y": 0}),
    ],
    [
        ("TX LED", "led", cfg["led"]),
        # ("PD5", "default", {**cfg["led"], "x": 2, "y": 0}),
    ],
]


leds_b = [
    [
        ("POWER", "led", cfg["led"]),
    ],
    [
        ("LED_BUILTIN", "led", cfg["led"]),
        # ("PB5", "default", {**cfg["led"], "x": 2, "y": 0}),
    ],
]

#########################################################
#
# Text blocks
#
#########################################################

title_1 = [
    '<tspan class="h1">ARDUINO</tspan>',
    '<tspan class="h1">UNO REV3</tspan>',
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