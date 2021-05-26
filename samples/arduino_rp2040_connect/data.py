from pinout import config


cfg = config.PinConfig(
    {
        "block": {
            "width": 80,
            "height": 20,
            "offset": (2, 0),
            "label_style": "block",
        },
        "block_sm": {
            "width": 30,
            "height": 20,
            "offset": (0, 0),
            "label_style": "block",
        },
        "start": {
            "width": 80,
            "height": 20,
            "label_style": "start",
        },
        "end": {
            "width": 80,
            "height": 20,
            "offset": (2, 0),
            "label_style": "end",
        },
        "single": {
            "r": 10,
            "width": 80,
            "height": 20,
            "style": "smooth_bend",
            "label_style": "block",
        },
    }
)

#########################################################
#
# Header: Right-hand-side
#
#########################################################
cfg.set_pitch((80, 0), (0, 0))
header_rhs = [
    [
        ("D12", "digital", cfg("start")),
        ("GPIO4", "mu-port", cfg("block")),
        ("CIPO", "default", cfg("end")),
    ],
    [
        ("D11", "digital", cfg("start")),
        ("GPIO7", "mu-port", cfg("block")),
        ("CIPI", "default", cfg("end")),
    ],
    [("D10", "digital", cfg("start")), ("GPIO5", "mu-port", cfg("end"))],
    [("D9", "digital", cfg("start")), ("GPIO21", "mu-port", cfg("end"))],
    [("D8", "digital", cfg("start")), ("GPIO20", "mu-port", cfg("end"))],
    [("D7", "digital", cfg("start")), ("GPIO19", "mu-port", cfg("end"))],
    [("D6", "digital", cfg("start")), ("GPIO18", "mu-port", cfg("end"))],
    [("D5", "digital", cfg("start")), ("GPIO17", "mu-port", cfg("end"))],
    [("D4", "digital", cfg("start")), ("GPIO16", "mu-port", cfg("end"))],
    [("D3", "digital", cfg("start")), ("GPIO15", "mu-port", cfg("end"))],
    [("D2", "digital", cfg("start")), ("GPIO25", "mu-port", cfg("end"))],
    [("GND", "gnd", cfg("single"))],
    [("RESET", "other", cfg("start")), ("RESET", "mu-port", cfg("end"))],
    [("RX", "digital", cfg("start")), ("GPIO1", "mu-port", cfg("end"))],
    [("TX", "digital", cfg("start")), ("GPIO0", "mu-port", cfg("end"))],
]


#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs = [
    [
        ("D13", "digital", cfg("start")),
        ("GPIO6", "mu-port", cfg("block")),
        ("SCK", "default", cfg("end")),
    ],
    [("+3V3", "pwr", cfg("single"))],
    [("AREF", "other", cfg("start")), ("PA03", "mu-port", cfg("end"))],
    [
        ("D14", "digital", cfg("start", width=50)),
        ("A0", "analog", cfg("block_sm")),
        ("GPIO26", "mu-port", cfg("block")),
        ("A0/DAC0", "default", cfg("end")),
    ],
    [
        ("D15", "digital", cfg("start", width=50)),
        ("A1", "analog", cfg("block_sm")),
        ("GPIO27", "mu-port", cfg("block")),
        ("A1", "default", cfg("end")),
    ],
    [
        ("D16", "digital", cfg("start", width=50)),
        ("A2", "analog", cfg("block_sm")),
        ("GPIO28", "mu-port", cfg("block")),
        ("A2", "default", cfg("end")),
    ],
    [
        ("D17", "digital", cfg("start", width=50)),
        ("A3", "analog", cfg("block_sm")),
        ("GPIO29", "mu-port", cfg("block")),
        ("A3", "default", cfg("end")),
    ],
    [
        ("D18", "digital", cfg("start", width=50)),
        ("A4", "analog", cfg("block_sm")),
        ("GPIO12", "mu-port", cfg("block")),
        ("A4", "default", cfg("end")),
    ],
    [
        ("D19", "digital", cfg("start", width=50)),
        ("A5", "analog", cfg("block_sm")),
        ("GPIO13", "mu-port", cfg("block")),
        ("A5", "default", cfg("end")),
    ],
    [
        ("D20", "digital", cfg("start", width=50)),
        ("A6", "analog", cfg("block_sm")),
        ("A6", "default show-leader", cfg("end", offset=(84, 0))),
    ],
    [
        ("D21", "digital", cfg("start", width=50)),
        ("A7", "analog", cfg("block_sm")),
        ("A7", "default show-leader", cfg("end", offset=(84, 0))),
    ],
    [("+5V", "pwr", cfg("single"))],
    [("RESET", "other", cfg("start")), ("QSPI_CSn", "default", cfg("end"))],
    [("GND", "gnd", cfg("single"))],
    [("VIN", "pwr", cfg("single"))],
]


#########################################################
#
# LED labels
#
#########################################################
cfg.set_pitch((230, 70), (-112, -22))
leds = [
    [("Power", "led", cfg("single", width=120))],
    [("LED_BUILTIN", "led", cfg("single", width=120))],
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
    '<tspan class="p">Pinout diagram create with <tspan class="italic">pinout (v0.0.10)</tspan></tspan>',
    '<tspan class="p">A Python package for creating pinout diagrams.</tspan>',
    '<tspan class="p"><tspan class="strong"><a href="https://pinout.readthedocs.io">pinout.readthedocs.io</a></tspan></tspan>',
]
para_2 = [
    '<tspan class="p">NOTE: This is not official documentation.</tspan>',
    '<tspan class="p">Diagram aesthetics from Arduino docs.</tspan>',
    '<tspan class="p"><tspan class="strong"><a href="https://www.arduino.cc/">https://www.arduino.cc/</a></tspan></tspan>',
]