# Helper function to calculate locations of label rows
def pitch_generator(start, pitch):
    x = start[0]
    y = start[1]
    while True:
        yield (x, y)
        x += pitch[0]
        y += pitch[1]


# Common label configuration settings
cfg0 = {"r": 0, "width": 80, "height": 23, "offset": (60, 0), "label_style": "start"}
cfg1 = {"r": 0, "width": 80, "height": 23, "offset": (2, 0), "label_style": "box"}
cfg2 = {"r": 13, "width": 80, "height": 23, "offset": (60, 0)}
cfg_end = {"r": 0, "width": 80, "height": 23, "offset": (2, 0), "label_style": "end"}

cfg_digital_short = {
    "r": 0,
    "width": 50,
    "height": 23,
    "offset": (60, 0),
    "label_style": "start",
}
cfg_analog_short = {
    "r": 0,
    "width": 30,
    "height": 23,
    "offset": (0, 0),
    "label_style": "block",
}


# setup some automation for pinrow positioning
pitch = pitch_generator((80, 0), (0, 3))


#########################################################
#
# Header: Right-hand-side
#
#########################################################

header_rhs = [
    [
        ("D12", "digital", cfg0),
        ("GPIO4", "mu-port", cfg1),
        ("CIPO", "default", cfg_end),
    ],
    [
        ("D11", "digital", cfg0),
        ("GPIO7", "mu-port", cfg1),
        ("CIPI", "default", cfg_end),
    ],
    [("D10", "digital", cfg0), ("GPIO5", "mu-port", cfg_end)],
    [("D9", "digital", cfg0), ("GPIO21", "mu-port", cfg_end)],
    [("D8", "digital", cfg0), ("GPIO20", "mu-port", cfg_end)],
    [("D7", "digital", cfg0), ("GPIO19", "mu-port", cfg_end)],
    [("D6", "digital", cfg0), ("GPIO18", "mu-port", cfg_end)],
    [("D5", "digital", cfg0), ("GPIO17", "mu-port", cfg_end)],
    [("D4", "digital", cfg0), ("GPIO16", "mu-port", cfg_end)],
    [("D3", "digital", cfg0), ("GPIO15", "mu-port", cfg_end)],
    [("D2", "digital", cfg0), ("GPIO25", "mu-port", cfg_end)],
    [("GND", "gnd", cfg2)],
    [("RESET", "other", cfg0), ("RESET", "mu-port", cfg_end)],
    [("RX", "digital", cfg0), ("GPIO1", "mu-port", cfg_end)],
    [("TX", "digital", cfg0), ("GPIO0", "mu-port", cfg_end)],
]


#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs = [
    [("D13", "digital", cfg0), ("GPIO6", "mu-port", cfg1), ("SCK", "default", cfg_end)],
    [("+3V3", "pwr", cfg2)],
    [("+AREF", "other", cfg0), ("PA03", "mu-port", cfg_end)],
    [
        ("D14", "digital", cfg_digital_short),
        (
            "A0",
            "analog",
            {
                "r": 0,
                "width": 30,
                "height": 23,
                "offset": (0, 0),
                "label_style": "block",
            },
        ),
        ("GPIO26", "mu-port", cfg1),
        ("A0/DAC0", "default", cfg_end),
    ],
    [
        ("D15", "digital", cfg_digital_short),
        ("A1", "analog", cfg_analog_short),
        ("GPIO27", "mu-port", cfg1),
        ("A1", "default", cfg_end),
    ],
    [
        ("D16", "digital", cfg_digital_short),
        ("A2", "analog", cfg_analog_short),
        ("GPIO28", "mu-port", cfg1),
        ("A2", "default", cfg_end),
    ],
    [
        ("D17", "digital", cfg_digital_short),
        ("A3", "analog", cfg_analog_short),
        ("GPIO29", "mu-port", cfg1),
        ("A3", "default", cfg_end),
    ],
    [
        ("D18", "digital", cfg_digital_short),
        ("A4", "analog", cfg_analog_short),
        ("GPIO12", "mu-port", cfg1),
        ("A4", "default", cfg_end),
    ],
    [
        ("D19", "digital", cfg_digital_short),
        ("A5", "analog", cfg_analog_short),
        ("GPIO13", "mu-port", cfg1),
        ("A5", "default", cfg_end),
    ],
    [
        ("D20", "digital", cfg_digital_short),
        ("A6", "analog", cfg_analog_short),
        (
            "A6",
            "default show-leader",
            {
                "r": 0,
                "width": 80,
                "height": 23,
                "offset": (84, 0),
                "label_style": "end",
            },
        ),
    ],
    [
        ("D21", "digital", cfg_digital_short),
        ("A7", "analog", cfg_analog_short),
        (
            "A7",
            "default show-leader",
            {
                "r": 0,
                "width": 80,
                "height": 23,
                "offset": (84, 0),
                "label_style": "end",
            },
        ),
    ],
    [("+5V", "pwr", cfg2)],
    [("RESET", "other", cfg0), ("QSPI_CSn", "default", cfg_end)],
    [("GND", "gnd", cfg2)],
    [("VIN", "pwr", cfg2)],
]


#########################################################
#
# LED labels
#
#########################################################

led_pitch = pitch_generator((200, 80), (-112, -28))
leds = [
    [
        (
            "Power",
            "led",
            {
                "r": 13,
                "style": "smooth_bend",
                "width": 120,
                "height": 23,
                "offset": next(led_pitch),
            },
        )
    ],
    [
        (
            "LED_BUILTIN",
            "led",
            {
                "r": 13,
                "style": "smooth_bend",
                "width": 120,
                "height": 23,
                "offset": next(led_pitch),
            },
        )
    ],
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
    '<tspan class="p">Pinout diagram create with <tspan class="strong italic">pinout</tspan></tspan>',
    '<tspan class="p">A Python package for creating pinout diagrams.</tspan>',
    '<tspan class="p"><a href="https://pinout.readthedocs.io">pinout.readthedocs.io</a></tspan>',
]
para_2 = [
    '<tspan class="p">NOTE: This is not official documentation.</tspan>',
    '<tspan class="p">Diagram aesthetics from Arduino docs.</tspan>',
    '<tspan class="p">Visit <tspan class="strong"><a href="https://www.arduino.cc/">https://www.arduino.cc/</a></tspan> for official docs.</tspan>',
]