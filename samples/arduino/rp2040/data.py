from pinout import config

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
        "lft_single": {"width": 80, "height": 20, "scale": (-1, 1)},
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
cfg.set_origin((0, 0), (0, 24.6))
cfg.set_offset((80, 0), (0, 0))
header_rhs = [
    [
        FirstLabel("D12", "digital", **cfg("rgt_first")),
        Label("GPIO4", "mu-port", **cfg("rgt")),
        LabelLast("CIPO", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("D11", "digital", **cfg("rgt_first")),
        Label("GPIO7", "mu-port", **cfg("rgt")),
        LabelLast("CIPI", "default", **cfg("rgt")),
    ],
    [
        FirstLabel("D10", "digital", **cfg("rgt_first")),
        LabelLast("GPIO5", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D9", "digital", **cfg("rgt_first")),
        LabelLast("GPIO21", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D8", "digital", **cfg("rgt_first")),
        LabelLast("GPIO20", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D7", "digital", **cfg("rgt_first")),
        LabelLast("GPIO19", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D6", "digital", **cfg("rgt_first")),
        LabelLast("GPIO18", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D5", "digital", **cfg("rgt_first")),
        LabelLast("GPIO17", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D4", "digital", **cfg("rgt_first")),
        LabelLast("GPIO16", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D3", "digital", **cfg("rgt_first")),
        LabelLast("GPIO15", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("D2", "digital", **cfg("rgt_first")),
        LabelLast("GPIO25", "mu-port", **cfg("rgt")),
    ],
    [Label("GND", "gnd", **cfg("rgt_single"))],
    [
        FirstLabel("RESET", "other", **cfg("rgt_first")),
        LabelLast("RESET", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("RX", "digital", **cfg("rgt_first")),
        LabelLast("GPIO1", "mu-port", **cfg("rgt")),
    ],
    [
        FirstLabel("TX", "digital", **cfg("rgt_first")),
        LabelLast("GPIO0", "mu-port", **cfg("rgt")),
    ],
]


#########################################################
#
# Header: Left-hand-side
#
#########################################################


cfg.set_origin((0, 0), (0, 24.6))
cfg.set_offset((80, 0), (0, 0))
header_lhs = [
    [
        FirstLabel("D13", "digital", **cfg("lft_first")),
        Label("GPIO6", "mu-port", **cfg("lft")),
        LabelLast("SCK", "default", **cfg("lft")),
    ],
    [Label("+3V3", "pwr", **cfg("lft_single"))],
    [
        FirstLabel("AREF", "other", **cfg("lft_first")),
        LabelLast("PA03", "mu-port", **cfg("lft")),
    ],
    [
        FirstLabel("D14", "digital", **cfg("lft_first_sm")),
        Label("A0", "analog", **cfg("lft_sm")),
        Label("GPIO26", "mu-port", **cfg("lft")),
        LabelLast("A0/DAC0", "default", **cfg("lft")),
    ],
    [
        FirstLabel("D15", "digital", **cfg("lft_first_sm")),
        Label("A1", "analog", **cfg("lft_sm")),
        Label("GPIO27", "mu-port", **cfg("lft")),
        LabelLast("A1", "default", **cfg("lft")),
    ],
    [
        FirstLabel("D16", "digital", **cfg("lft_first_sm")),
        Label("A2", "analog", **cfg("lft_sm")),
        Label("GPIO28", "mu-port", **cfg("lft")),
        LabelLast("A2", "default", **cfg("lft")),
    ],
    [
        FirstLabel("D17", "digital", **cfg("lft_first_sm")),
        Label("A3", "analog", **cfg("lft_sm")),
        Label("GPIO29", "mu-port", **cfg("lft")),
        LabelLast("A3", "default", **cfg("lft")),
    ],
    [
        FirstLabel("D18", "digital", **cfg("lft_first_sm")),
        Label("A4", "analog", **cfg("lft_sm")),
        Label("GPIO12", "mu-port", **cfg("lft")),
        LabelLast("A4", "default", **cfg("lft")),
    ],
    [
        FirstLabel("D19", "digital", **cfg("lft_first_sm")),
        Label("A5", "analog", **cfg("lft_sm")),
        Label("GPIO13", "mu-port", **cfg("lft")),
        LabelLast("A5", "default", **cfg("lft")),
    ],
    [
        FirstLabel("D20", "digital", **cfg("lft_first_sm")),
        Label("A6", "analog", **cfg("lft_sm")),
        LabelLast("A6", "default show-leader", **cfg("lft", offset=(84, 0))),
    ],
    [
        FirstLabel("D21", "digital", **cfg("lft_first_sm")),
        Label("A7", "analog", **cfg("lft_sm")),
        LabelLast("A7", "default show-leader", **cfg("lft", offset=(84, 0))),
    ],
    [Label("+5V", "pwr", **cfg("lft_single"))],
    [
        FirstLabel("RESET", "other", **cfg("lft_first")),
        LabelLast("QSPI_CSn", "default", **cfg("lft")),
    ],
    [Label("GND", "gnd", **cfg("lft_single"))],
    [Label("VIN", "pwr", **cfg("lft_single"))],
]


#########################################################
#
# LED labels
#
#########################################################
cfg.set_offset((230, 70), (-112, -22))
leds = [
    [Label("Power", "led", **cfg("rgt_single", width=120, style="cnr"))],
    [Label("LED_BUILTIN", "led", **cfg("rgt_single", width=120, style="cnr"))],
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
