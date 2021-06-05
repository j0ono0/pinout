from pinout import config
from pinout.components import leaderline as lline
from arduino_components import Label, FirstLabel, LabelLast


cfg = config.PinConfig(
    {
        # Right header
        "rgt_first": {"width": 80, "height": 20},
        "rgt_single": {"width": 80, "height": 20},
        "rgt": {"width": 80, "height": 20, "offset": (2, 0)},
        # Left header
        "lft_first": {"width": 80, "height": 20, "scale": (-1, 1)},
        "lft_first_sm": {"width": 50, "height": 20, "scale": (-1, 1)},
        "lft": {"width": 80, "height": 20, "scale": (-1, 1), "offset": (2, 0)},
        "lft_sm": {"width": 30, "height": 20, "scale": (-1, 1), "offset": (0, 0)},
        # LEDs
        "leds_1": {
            "width": 120,
            "height": 20,
            "scale": (-1, -1),
            "leaderline": lline.Curved("vh"),
        },
        "leds_2": {
            "width": 120,
            "height": 20,
            "scale": (-1, 1),
            "leaderline": lline.Curved("vh"),
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
cfg.set_origin((0, 0), (0, 15.35))
cfg.set_offset((90, -80), (0, 8))
header_rhs_a = [
    [
        FirstLabel("D19/SCL", "digital", **cfg("rgt_first")),
        Label("PC5", "mu-port", **cfg("rgt")),
        LabelLast("SCL", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("D18/SDA", "digital", **cfg("rgt_first")),
        Label("PC4", "mu-port", **cfg("rgt")),
        LabelLast("SDA", "default", **cfg("rgt")),
    ],
    [
        Label("AREF", "other", **cfg("rgt_first")),
    ],
    [
        Label("GND", "gnd", **cfg("rgt_first")),
    ],
    [
        FirstLabel("D13", "digital", **cfg("rgt_first")),
        Label("PB5", "mu-port", **cfg("rgt")),
        LabelLast("SCK", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("D12", "digital", **cfg("rgt_first")),
        Label("PB4", "mu-port", **cfg("rgt")),
        LabelLast("MISO", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("~D11", "digital", **cfg("rgt_first")),
        Label("PB3", "mu-port", **cfg("rgt")),
        LabelLast("MOSI", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("~D10", "digital", **cfg("rgt_first")),
        Label("PB2", "mu-port", **cfg("rgt")),
        LabelLast("SS", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("~D9", "digital", **cfg("rgt_first")),
        LabelLast("PB1", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D8", "digital", **cfg("rgt_first")),
        LabelLast("PB0", "mu-port", **cfg("rgt")),
    ],
]

cfg.set_origin((0, 0), (0, 15.35))
cfg.set_offset((90, 8), (0, 8))
header_rhs_b = [
    [
        FirstLabel("D7", "digital", **cfg("rgt_first")),
        LabelLast("PD7", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("~D6", "digital", **cfg("rgt_first")),
        LabelLast("PD6", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("~D5", "digital", **cfg("rgt_first")),
        LabelLast("PD5", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D4", "digital", **cfg("rgt_first")),
        LabelLast("PD4", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("~D3", "digital", **cfg("rgt_first")),
        LabelLast("PD3", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D2", "digital", **cfg("rgt_first")),
        LabelLast("PD2", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D1/TX", "digital", **cfg("rgt_first")),
        LabelLast("PD1", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D0/RX", "digital", **cfg("rgt_first")),
        LabelLast("PD0", "mu-port", **cfg("rgt")),
    ],
]

#########################################################
#
# Header: Left-hand-side
#
#########################################################
cfg.set_origin((0, 0), (0, 15.35))
cfg.set_offset((90, -64), (0, 8))
header_lhs_a = [
    [Label("NC", "nc", **cfg("lft_first"))],
    [Label("IOREF", "other", **cfg("lft_first"))],
    [
        FirstLabel("RESET", "other", **cfg("lft_first")),
        LabelLast("PC6", "default", **cfg("lft")),
    ],
    [Label("+3V3", "pwr", **cfg("lft_first"))],
    [Label("+5", "pwr", **cfg("lft_first"))],
    [Label("GND", "gnd", **cfg("lft_first"))],
    [Label("GND", "gnd", **cfg("lft_first"))],
    [Label("VIN", "pwr", **cfg("lft_first"))],
]

# Example of using a list comprehension to generate pin data
cfg.set_origin((0, 0), (0, 15.35))
cfg.set_offset((90, 8), (0, 8))
header_lhs_b = [
    [
        FirstLabel(f"D{14 + i}", "digital", **cfg("lft_first_sm")),
        Label(f"A{i}", "analog", **cfg("lft_sm")),
        Label(f"PC{i}", "mu-port", **cfg("lft")),
        LabelLast(f"ADC[{i}]", "default", **cfg("lft")),
    ]
    for i in range(6)
]

#########################################################
#
# LED labels
#
#########################################################
cfg.set_origin((0, 0), (17, 0))
cfg.set_offset((279, 120), (17, 23))
leds_a = [
    [
        FirstLabel("RX LED", "led", **cfg("leds_1")),
        LabelLast("PD4", "default", **cfg("leds_1", offset=(2, 0))),
    ],
    [
        FirstLabel("TX LED", "led", **cfg("leds_1")),
        LabelLast("PD5", "default", **cfg("leds_1", offset=(2, 0))),
    ],
]

cfg.set_origin((0, 0), (39, -185))
cfg.set_offset((38, 90), (39, 208))
leds_b = [
    [
        Label("POWER", "led", **cfg("leds_2")),
    ],
    [
        FirstLabel("LED_BUILTIN", "led", **cfg("leds_2")),
        LabelLast("PB5", "default", **cfg("leds_2", offset=(2, 0))),
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