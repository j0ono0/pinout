from arduino_components import PlbStart, PlbEnd, Plb
from copy import deepcopy

lbl_start = {"body": PlbStart(x=0, y=0, width=80, height=20)}
lbl_start_sm = {"body": PlbStart(x=0, y=0, width=50, height=20)}
lbl_end = {"body": PlbEnd(x=2, y=0, width=80, height=20)}
lbl_end_ext = {"body": PlbEnd(x=84, y=0, width=80, height=20)}
lbl = {"body": Plb(width=80, height=20, x=2, y=0)}
lbl_sm = {"body": Plb(width=30, height=20, x=0, y=0)}
lbl_single = {"body": Plb(width=80, height=20, x=2, y=0, corner_radius=10)}

# LEDs
led = {"body": {"width": 120, "height": 20}}


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
        ("D19/SCL", "digital", lbl_start),
        ("PC5", "mu-port", lbl),
        ("SCL", "default", lbl_end),
    ],
    [
        ("D18/SDA", "digital", lbl_start),
        ("PC4", "mu-port", lbl),
        ("SDA", "default", lbl_end),
    ],
    [
        ("AREF", "other", lbl_single),
    ],
    [
        ("GND", "gnd", lbl_single),
    ],
    [
        ("D13", "digital", lbl_start),
        ("PB5", "mu-port", lbl),
        ("SCK", "default", lbl_end),
    ],
    [
        ("D12", "digital", lbl_start),
        ("PB4", "mu-port", lbl),
        ("MISO", "default", lbl_end),
    ],
    [
        ("~D11", "digital", lbl_start),
        ("PB3", "mu-port", lbl),
        ("MOSI", "default", lbl_end),
    ],
    [
        ("~D10", "digital", lbl_start),
        ("PB2", "mu-port", lbl),
        ("SS", "default", lbl_end),
    ],
    [
        ("~D9", "digital", lbl_start),
        ("PB1", "mu-port", lbl_end),
    ],
    [
        ("D8", "digital", lbl_start),
        ("PB0", "mu-port", lbl_end),
    ],
]

header_rhs_b = [
    [
        ("D7", "digital", lbl_start),
        ("PD7", "default", lbl_end),
    ],
    [
        ("~D6", "digital", lbl_start),
        ("PD6", "default", lbl_end),
    ],
    [
        ("~D5", "digital", lbl_start),
        ("PD5", "mu-port", lbl_end),
    ],
    [
        ("D4", "digital", lbl_start),
        ("PD4", "mu-port", lbl_end),
    ],
    [
        ("~D3", "digital", lbl_start),
        ("PD3", "mu-port", lbl_end),
    ],
    [
        ("D2", "digital", lbl_start),
        ("PD2", "mu-port", lbl_end),
    ],
    [
        ("D1/TX", "digital", lbl_start),
        ("PD1", "mu-port", lbl_end),
    ],
    [
        ("D0/RX", "digital", lbl_start),
        ("PD0", "mu-port", lbl_end),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs_a = [
    [("NC", "nc", lbl_single)],
    [("IOREF", "other", lbl_single)],
    [
        ("RESET", "other", lbl_start),
        ("PC6", "default", lbl_end),
    ],
    [("+3V3", "pwr", lbl_single)],
    [("+5", "pwr", lbl_single)],
    [("GND", "gnd", lbl_single)],
    [("GND", "gnd", lbl_single)],
    [("VIN", "pwr", lbl_single)],
]

# Example of using a list comprehension to generate pin data


header_lhs_b = [
    [
        (f"D{14 + i}", "digital", lbl_start_sm),
        (f"A{i}", "analog", lbl_sm),
        (f"PC{i}", "mu-port", lbl),
        (f"ADC[{i}]", "default", lbl_end),
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
        ("RX LED", "led", lbl_start),
        ("PD4", "default", lbl_end),
    ],
    [
        ("TX LED", "led", lbl_start),
        ("PD5", "default", lbl_end),
    ],
]


leds_b = [
    [
        ("POWER", "led", lbl_single),
    ],
    [
        ("LED_BUILTIN", "led", lbl_start),
        ("PB5", "default", lbl_end),
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