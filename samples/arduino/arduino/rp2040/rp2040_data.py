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
        ("D12", "digital"),
        ("GPIO4", "mu-port"),
        ("CIPO", "default"),
    ],
    [
        ("D11", "digital"),
        ("GPIO7", "mu-port"),
        ("CIPI", "default"),
    ],
    [
        ("D10", "digital"),
        ("GPIO5", "mu-port"),
    ],
    [
        ("D9", "digital"),
        ("GPIO21", "mu-port"),
    ],
    [
        ("D8", "digital"),
        ("GPIO20", "mu-port"),
    ],
    [
        ("D7", "digital"),
        ("GPIO19", "mu-port"),
    ],
    [
        ("D6", "digital"),
        ("GPIO18", "mu-port"),
    ],
    [
        ("D5", "digital"),
        ("GPIO17", "mu-port"),
    ],
    [
        ("D4", "digital"),
        ("GPIO16", "mu-port"),
    ],
    [
        ("D3", "digital"),
        ("GPIO15", "mu-port"),
    ],
    [
        ("D2", "digital"),
        ("GPIO25", "mu-port"),
    ],
    [
        ("GND", "gnd"),
    ],
    [
        ("RESET", "other"),
        ("RESET", "mu-port"),
    ],
    [
        ("RX", "digital"),
        ("GPIO1", "mu-port"),
    ],
    [
        ("TX", "digital"),
        ("GPIO0", "mu-port"),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs = [
    [
        ("D13", "digital"),
        ("GPIO6", "mu-port"),
        ("SCK", "default"),
    ],
    [
        ("+3V3", "pwr"),
    ],
    [
        ("AREF", "other"),
        ("PA03", "mu-port"),
    ],
    [
        ("D14", "digital"),
        ("A0", "analog"),
        ("GPIO26", "mu-port"),
        ("A0/DAC0", "default"),
    ],
    [
        ("D15", "digital"),
        ("A1", "analog"),
        ("GPIO27", "mu-port"),
        ("A1", "default"),
    ],
    [
        ("D16", "digital"),
        ("A2", "analog"),
        ("GPIO28", "mu-port"),
        ("A2", "default"),
    ],
    [
        ("D17", "digital"),
        ("A3", "analog"),
        ("GPIO29", "mu-port"),
        ("A3", "default"),
    ],
    [
        ("D18", "digital"),
        ("A4", "analog"),
        ("GPIO12", "mu-port"),
        ("A4", "default"),
    ],
    [
        ("D19", "digital"),
        ("A5", "analog"),
        ("GPIO13", "mu-port"),
        ("A5", "default"),
    ],
    [
        ("D20", "digital"),
        ("A6", "analog"),
        ("A6", "default show-leader"),
    ],
    [
        ("D21", "digital"),
        ("A7", "analog"),
        ("A7", "default show-leader"),
    ],
    [
        ("+5V", "pwr"),
    ],
    [
        ("RESET", "other"),
        ("QSPI_CSn", "default"),
    ],
    [
        ("GND", "gnd"),
    ],
    [
        ("VIN", "pwr"),
    ],
]


#########################################################
#
# LED labels
#
#########################################################

leds = [
    [("Power", "led")],
    [("LED_BUILTIN", "led")],
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
