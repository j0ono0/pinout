from pinout import config
from arduino_components import Label, FirstLabel, LabelLast


cfg = config.PinConfig(
    {
        "block": {
            "width": 80,
            "height": 20,
            "offset": (2, 0),
        },
        "block_sm": {
            "width": 30,
            "height": 20,
            "offset": (0, 0),
        },
        "start": {
            "width": 80,
            "height": 20,
        },
        "end": {
            "width": 80,
            "height": 20,
            "offset": (2, 0),
        },
        "single": {
            "r": 10,
            "width": 80,
            "height": 20,
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
        (FirstLabel, "D12", "digital", cfg("start")),
        (Label, "GPIO4", "mu-port", cfg("block")),
        (LabelLast, "CIPO", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D11", "digital", cfg("start")),
        (Label, "GPIO7", "mu-port", cfg("block")),
        (LabelLast, "CIPI", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D10", "digital", cfg("start")),
        (LabelLast, "GPIO5", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D9", "digital", cfg("start")),
        (LabelLast, "GPIO21", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D8", "digital", cfg("start")),
        (LabelLast, "GPIO20", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D7", "digital", cfg("start")),
        (LabelLast, "GPIO19", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D6", "digital", cfg("start")),
        (LabelLast, "GPIO18", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D5", "digital", cfg("start")),
        (LabelLast, "GPIO17", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D4", "digital", cfg("start")),
        (LabelLast, "GPIO16", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D3", "digital", cfg("start")),
        (LabelLast, "GPIO15", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D2", "digital", cfg("start")),
        (LabelLast, "GPIO25", "mu-port", cfg("end")),
    ],
    [(Label, "GND", "gnd", cfg("single"))],
    [
        (FirstLabel, "RESET", "other", cfg("start")),
        (LabelLast, "RESET", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "RX", "digital", cfg("start")),
        (LabelLast, "GPIO1", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "TX", "digital", cfg("start")),
        (LabelLast, "GPIO0", "mu-port", cfg("end")),
    ],
]


#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs = [
    [
        (FirstLabel, "D13", "digital", cfg("start")),
        (Label, "GPIO6", "mu-port", cfg("block")),
        (LabelLast, "SCK", "default", cfg("end")),
    ],
    [(FirstLabel, "+3V3", "pwr", cfg("single"))],
    [
        (FirstLabel, "AREF", "other", cfg("start")),
        (LabelLast, "PA03", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D14", "digital", cfg("start", width=50)),
        (Label, "A0", "analog", cfg("block_sm")),
        (Label, "GPIO26", "mu-port", cfg("block")),
        (LabelLast, "A0/DAC0", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D15", "digital", cfg("start", width=50)),
        (Label, "A1", "analog", cfg("block_sm")),
        (Label, "GPIO27", "mu-port", cfg("block")),
        (LabelLast, "A1", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D16", "digital", cfg("start", width=50)),
        (Label, "A2", "analog", cfg("block_sm")),
        (Label, "GPIO28", "mu-port", cfg("block")),
        (LabelLast, "A2", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D17", "digital", cfg("start", width=50)),
        (Label, "A3", "analog", cfg("block_sm")),
        (Label, "GPIO29", "mu-port", cfg("block")),
        (LabelLast, "A3", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D18", "digital", cfg("start", width=50)),
        (Label, "A4", "analog", cfg("block_sm")),
        (Label, "GPIO12", "mu-port", cfg("block")),
        (LabelLast, "A4", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D19", "digital", cfg("start", width=50)),
        (Label, "A5", "analog", cfg("block_sm")),
        (Label, "GPIO13", "mu-port", cfg("block")),
        (LabelLast, "A5", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D20", "digital", cfg("start", width=50)),
        (Label, "A6", "analog", cfg("block_sm")),
        (LabelLast, "A6", "default show-leader", cfg("end", offset=(84, 0))),
    ],
    [
        (FirstLabel, "D21", "digital", cfg("start", width=50)),
        (Label, "A7", "analog", cfg("block_sm")),
        (LabelLast, "A7", "default show-leader", cfg("end", offset=(84, 0))),
    ],
    [(Label, "+5V", "pwr", cfg("single"))],
    [
        (FirstLabel, "RESET", "other", cfg("start")),
        (LabelLast, "QSPI_CSn", "default", cfg("end")),
    ],
    [(Label, "GND", "gnd", cfg("single"))],
    [(Label, "VIN", "pwr", cfg("single"))],
]


#########################################################
#
# LED labels
#
#########################################################
cfg.set_pitch((230, 70), (-112, -22))
leds = [
    [(Label, "Power", "led", cfg("single", width=120, style="cnr"))],
    [(Label, "LED_BUILTIN", "led", cfg("single", width=120, style="cnr"))],
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