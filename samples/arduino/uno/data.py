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
cfg.set_pitch((90, -80), (0, 8))
header_rhs_a = [
    [
        (FirstLabel, "D19/SCL", "digital", cfg("start")),
        (Label, "PC5", "mu-port", cfg("block")),
        (LabelLast, "SCL", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D18/SDA", "digital", cfg("start")),
        (Label, "PC4", "mu-port", cfg("block")),
        (LabelLast, "SDA", "default", cfg("end")),
    ],
    [
        (Label, "AREF", "other", cfg("single")),
    ],
    [
        (Label, "GND", "gnd", cfg("single")),
    ],
    [
        (FirstLabel, "D13", "digital", cfg("start")),
        (Label, "PB5", "mu-port", cfg("block")),
        (LabelLast, "SCK", "default", cfg("end")),
    ],
    [
        (FirstLabel, "D12", "digital", cfg("start")),
        (Label, "PB4", "mu-port", cfg("block")),
        (LabelLast, "MISO", "default", cfg("end")),
    ],
    [
        (FirstLabel, "~D11", "digital", cfg("start")),
        (Label, "PB3", "mu-port", cfg("block")),
        (LabelLast, "MOSI", "default", cfg("end")),
    ],
    [
        (FirstLabel, "~D10", "digital", cfg("start")),
        (Label, "PB2", "mu-port", cfg("block")),
        (LabelLast, "SS", "default", cfg("end")),
    ],
    [
        (FirstLabel, "~D9", "digital", cfg("start")),
        (LabelLast, "PB1", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D8", "digital", cfg("start")),
        (LabelLast, "PB0", "mu-port", cfg("end")),
    ],
]
cfg.set_pitch((90, 8), (0, 8))
header_rhs_b = [
    [
        (FirstLabel, "D7", "digital", cfg("start")),
        (LabelLast, "PD7", "default", cfg("end")),
    ],
    [
        (FirstLabel, "~D6", "digital", cfg("start")),
        (LabelLast, "PD6", "default", cfg("end")),
    ],
    [
        (FirstLabel, "~D5", "digital", cfg("start")),
        (LabelLast, "PD5", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D4", "digital", cfg("start")),
        (LabelLast, "PD4", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "~D3", "digital", cfg("start")),
        (LabelLast, "PD3", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D2", "digital", cfg("start")),
        (LabelLast, "PD2", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D1/TX", "digital", cfg("start")),
        (LabelLast, "PD1", "mu-port", cfg("end")),
    ],
    [
        (FirstLabel, "D0/RX", "digital", cfg("start")),
        (LabelLast, "PD0", "mu-port", cfg("end")),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################
cfg.set_pitch((90, -64), (0, 8))
header_lhs_a = [
    [(Label, "NC", "nc", cfg("single"))],
    [(Label, "IOREF", "other", cfg("single"))],
    [
        (FirstLabel, "RESET", "other", cfg("start")),
        (LabelLast, "PC6", "default", cfg("end")),
    ],
    [(Label, "+3V3", "pwr", cfg("single"))],
    [(Label, "+5", "pwr", cfg("single"))],
    [(Label, "GND", "gnd", cfg("single"))],
    [(Label, "GND", "gnd", cfg("single"))],
    [(Label, "VIN", "pwr", cfg("single"))],
]

# Example of using a list comprehension to generate pin data
cfg.set_pitch((90, 8), (0, 8))
header_lhs_b = [
    [
        (FirstLabel, f"D{14 + i}", "digital", cfg("start", width=50)),
        (Label, f"A{i}", "analog", cfg("block_sm")),
        (Label, f"PC{i}", "mu-port", cfg("block")),
        (LabelLast, f"ADC[{i}]", "default", cfg("end")),
    ]
    for i in range(6)
]

#########################################################
#
# LED labels
#
#########################################################
cfg.set_pitch((279, 120), (17, 23))
leds_a = [
    [
        (FirstLabel, "RX LED", "led", cfg("start", width=110, style="cnr")),
        (LabelLast, "PD4", "default", cfg("end")),
    ],
    [
        (FirstLabel, "TX LED", "led", cfg("start", width=110, style="cnr")),
        (LabelLast, "PD5", "default", cfg("end")),
    ],
]

cfg.set_pitch((38, 90), (39, 208))
leds_b = [
    [
        (Label, "POWER", "led", cfg("single", width=110, style="cnr")),
    ],
    [
        (FirstLabel, "LED_BUILTIN", "led", cfg("start", width=110, style="cnr")),
        (LabelLast, "PB5", "default", cfg("end")),
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