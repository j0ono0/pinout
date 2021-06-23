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
        ("D19/SCL", "digital"),
        ("PC5", "mu-port"),
        ("SCL", "default"),
    ],
    [
        ("D18/SDA", "digital"),
        ("PC4", "mu-port"),
        ("SDA", "default"),
    ],
    [
        ("AREF", "other"),
    ],
    [
        ("GND", "gnd"),
    ],
    [
        ("D13", "digital"),
        ("PB5", "mu-port"),
        ("SCK", "default"),
    ],
    [
        ("D12", "digital"),
        ("PB4", "mu-port"),
        ("MISO", "default"),
    ],
    [
        ("~D11", "digital"),
        ("PB3", "mu-port"),
        ("MOSI", "default"),
    ],
    [
        ("~D10", "digital"),
        ("PB2", "mu-port"),
        ("SS", "default"),
    ],
    [
        ("~D9", "digital"),
        ("PB1", "mu-port"),
    ],
    [
        ("D8", "digital"),
        ("PB0", "mu-port"),
    ],
]

header_rhs_b = [
    [
        ("D7", "digital"),
        ("PD7", "default"),
    ],
    [
        ("~D6", "digital"),
        ("PD6", "default"),
    ],
    [
        ("~D5", "digital"),
        ("PD5", "mu-port"),
    ],
    [
        ("D4", "digital"),
        ("PD4", "mu-port"),
    ],
    [
        ("~D3", "digital"),
        ("PD3", "mu-port"),
    ],
    [
        ("D2", "digital"),
        ("PD2", "mu-port"),
    ],
    [
        ("D1/TX", "digital"),
        ("PD1", "mu-port"),
    ],
    [
        ("D0/RX", "digital"),
        ("PD0", "mu-port"),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs_a = [
    [("NC", "nc")],
    [("IOREF", "other")],
    [
        ("RESET", "other"),
        ("PC6", "default"),
    ],
    [("+3V3", "pwr")],
    [("+5", "pwr")],
    [("GND", "gnd")],
    [("GND", "gnd")],
    [("VIN", "pwr")],
]

# Example of using a list comprehension to generate pin data


header_lhs_b = [
    [
        (f"D{14 + i}", "digital"),
        (f"A{i}", "analog"),
        (f"PC{i}", "mu-port"),
        (f"ADC[{i}]", "default"),
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
        ("RX LED", "led"),
        ("PD4", "default"),
    ],
    [
        ("TX LED", "led"),
        ("PD5", "default"),
    ],
]


leds_b = [
    [
        ("POWER", "led"),
    ],
    [
        ("LED_BUILTIN", "led"),
        ("PB5", "default"),
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