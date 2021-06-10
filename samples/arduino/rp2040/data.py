from arduino_components import PlbStart, PlbEnd, Plb


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

header_rhs = [
    [
        ("D12", "digital", lbl_start),
        ("GPIO4", "mu-port", lbl),
        ("CIPO", "default", lbl_end),
    ],
    [
        ("D11", "digital", lbl_start),
        ("GPIO7", "mu-port", lbl),
        ("CIPI", "default", lbl_end),
    ],
    [
        ("D10", "digital", lbl_start),
        ("GPIO5", "mu-port", lbl_end),
    ],
    [
        ("D9", "digital", lbl_start),
        ("GPIO21", "mu-port", lbl_end),
    ],
    [
        ("D8", "digital", lbl_start),
        ("GPIO20", "mu-port", lbl_end),
    ],
    [
        ("D7", "digital", lbl_start),
        ("GPIO19", "mu-port", lbl_end),
    ],
    [
        ("D6", "digital", lbl_start),
        ("GPIO18", "mu-port", lbl_end),
    ],
    [
        ("D5", "digital", lbl_start),
        ("GPIO17", "mu-port", lbl_end),
    ],
    [
        ("D4", "digital", lbl_start),
        ("GPIO16", "mu-port", lbl_end),
    ],
    [
        ("D3", "digital", lbl_start),
        ("GPIO15", "mu-port", lbl_end),
    ],
    [
        ("D2", "digital", lbl_start),
        ("GPIO25", "mu-port", lbl_end),
    ],
    [
        ("GND", "gnd", lbl_single),
    ],
    [
        ("RESET", "other", lbl_start),
        ("RESET", "mu-port", lbl_end),
    ],
    [
        ("RX", "digital", lbl_start),
        ("GPIO1", "mu-port", lbl_end),
    ],
    [
        ("TX", "digital", lbl_start),
        ("GPIO0", "mu-port", lbl_end),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs = [
    [
        ("D13", "digital", lbl_start),
        ("GPIO6", "mu-port", lbl),
        ("SCK", "default", lbl_end),
    ],
    [
        ("+3V3", "pwr", lbl_single),
    ],
    [
        ("AREF", "other", lbl_start),
        ("PA03", "mu-port", lbl_end),
    ],
    [
        ("D14", "digital", lbl_start_sm),
        ("A0", "analog", lbl_sm),
        ("GPIO26", "mu-port", lbl),
        ("A0/DAC0", "default", lbl_end),
    ],
    [
        ("D15", "digital", lbl_start_sm),
        ("A1", "analog", lbl_sm),
        ("GPIO27", "mu-port", lbl),
        ("A1", "default", lbl_end),
    ],
    [
        ("D16", "digital", lbl_start_sm),
        ("A2", "analog", lbl_sm),
        ("GPIO28", "mu-port", lbl),
        ("A2", "default", lbl_end),
    ],
    [
        ("D17", "digital", lbl_start_sm),
        ("A3", "analog", lbl_sm),
        ("GPIO29", "mu-port", lbl),
        ("A3", "default", lbl_end),
    ],
    [
        ("D18", "digital", lbl_start_sm),
        ("A4", "analog", lbl_sm),
        ("GPIO12", "mu-port", lbl),
        ("A4", "default", lbl_end),
    ],
    [
        ("D19", "digital", lbl_start_sm),
        ("A5", "analog", lbl_sm),
        ("GPIO13", "mu-port", lbl),
        ("A5", "default", lbl_end),
    ],
    [
        ("D20", "digital", lbl_start_sm),
        ("A6", "analog", lbl_sm),
        ("A6", "default show-leader", lbl_end_ext),
    ],
    [
        ("D21", "digital", lbl_start_sm),
        ("A7", "analog", lbl_sm),
        ("A7", "default show-leader", lbl_end_ext),
    ],
    [
        ("+5V", "pwr", lbl_single),
    ],
    [
        ("RESET", "other", lbl_start),
        ("QSPI_CSn", "default", lbl_end),
    ],
    [
        ("GND", "gnd", lbl_single),
    ],
    [
        ("VIN", "pwr", lbl_single),
    ],
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
