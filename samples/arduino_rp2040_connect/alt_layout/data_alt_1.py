# Experimental helper function to calculate locations of label rows
# This only gets used for the LED labels
def pitch_generator(start, pitch):
    x = start[0]
    y = start[1]
    while True:
        yield (x, y)
        x += pitch[0]
        y += pitch[1]


# Define common dimensions
lbl_h = 26
lbl_w_xl = 120
lbl_w_lg = 100
lbl_w_md = 60
lbl_w_sm = 40

rhs_pitch = pitch_generator((60, -56), (0, 6))
lhs_pitch = pitch_generator((60, -56), (0, 6))
offset_x_lg = (104, 0)
offset_x_sm = (2, 0)

# Common label configuration settings
cfg0 = {
    "width": lbl_w_lg,
    "height": lbl_h,
    "offset": next(rhs_pitch),
    "label_style": "start",
}
cfg1 = {
    "width": lbl_w_lg,
    "height": lbl_h,
    "offset": offset_x_sm,
    "label_style": "box",
}
cfg2 = {"r": lbl_h / 2, "width": lbl_w_lg, "height": lbl_h, "offset": next(lhs_pitch)}

cfg_end = {
    "width": lbl_w_lg,
    "height": lbl_h,
    "offset": offset_x_sm,
    "label_style": "end",
}

cfg_digital_short = {
    "width": lbl_w_md,
    "height": lbl_h,
    "offset": offset_x_lg,
    "label_style": "start",
}
cfg_analog_short = {
    "width": lbl_w_sm,
    "height": lbl_h,
    "label_style": "block",
}


#########################################################
#
# Header: Right-hand-side
#
#########################################################

header_rhs = [
    [
        (
            "D12",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO4", "mu-port", cfg1),
        ("CIPO", "default", cfg_end),
    ],
    [
        (
            "D11",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO7", "mu-port", cfg1),
        ("CIPI", "default", cfg_end),
    ],
    [
        (
            "D10",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO5", "mu-port", cfg_end),
    ],
    [
        (
            "D9",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO21", "mu-port", cfg_end),
    ],
    [
        (
            "D8",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO20", "mu-port", cfg_end),
    ],
    [
        (
            "D7",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO19", "mu-port", cfg_end),
    ],
    [
        (
            "D6",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO18", "mu-port", cfg_end),
    ],
    [
        (
            "D5",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO17", "mu-port", cfg_end),
    ],
    [
        (
            "D4",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO16", "mu-port", cfg_end),
    ],
    [
        (
            "D3",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO15", "mu-port", cfg_end),
    ],
    [
        (
            "D2",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO25", "mu-port", cfg_end),
    ],
    [
        (
            "GND",
            "gnd",
            {
                "r": lbl_h / 2,
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
            },
        )
    ],
    [
        (
            "RESET",
            "other",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("RESET", "mu-port", cfg_end),
    ],
    [
        (
            "RX",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO1", "mu-port", cfg_end),
    ],
    [
        (
            "TX",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(rhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO0", "mu-port", cfg_end),
    ],
]


#########################################################
#
# Header: Left-hand-side
#
#########################################################

header_lhs = [
    [
        (
            "D13",
            "digital",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("GPIO6", "mu-port", cfg1),
        ("SCK", "default", cfg_end),
    ],
    [
        (
            "+3V3",
            "pwr",
            {
                "r": lbl_h / 2,
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(lhs_pitch),
            },
        )
    ],
    [
        (
            "AREF",
            "other",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("PA03", "mu-port", cfg_end),
    ],
    [
        (
            "D14",
            "digital",
            {
                "width": lbl_w_md,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        (
            "A0",
            "analog",
            {
                "width": lbl_w_sm,
                "height": lbl_h,
                "offset": (0, 0),
                "label_style": "block",
            },
        ),
        ("GPIO26", "mu-port", cfg1),
        ("A0/DAC0", "default", cfg_end),
    ],
    [
        (
            "D15",
            "digital",
            {
                "width": lbl_w_md,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("A1", "analog", cfg_analog_short),
        ("GPIO27", "mu-port", cfg1),
        ("A1", "default", cfg_end),
    ],
    [
        (
            "D16",
            "digital",
            {
                "width": lbl_w_md,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("A2", "analog", cfg_analog_short),
        ("GPIO28", "mu-port", cfg1),
        ("A2", "default", cfg_end),
    ],
    [
        (
            "D17",
            "digital",
            {
                "width": lbl_w_md,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("A3", "analog", cfg_analog_short),
        ("GPIO29", "mu-port", cfg1),
        ("A3", "default", cfg_end),
    ],
    [
        (
            "D18",
            "digital",
            {
                "width": lbl_w_md,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("A4", "analog", cfg_analog_short),
        ("GPIO12", "mu-port", cfg1),
        ("A4", "default", cfg_end),
    ],
    [
        (
            "D19",
            "digital",
            {
                "width": lbl_w_md,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("A5", "analog", cfg_analog_short),
        ("GPIO13", "mu-port", cfg1),
        ("A5", "default", cfg_end),
    ],
    [
        (
            "D20",
            "digital",
            {
                "width": lbl_w_md,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("A6", "analog", cfg_analog_short),
        (
            "A6",
            "default show-leader",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": offset_x_lg,
                "label_style": "end",
            },
        ),
    ],
    [
        (
            "D21",
            "digital",
            {
                "width": lbl_w_md,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("A7", "analog", cfg_analog_short),
        (
            "A7",
            "default show-leader",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": offset_x_lg,
                "label_style": "end",
            },
        ),
    ],
    [
        (
            "+5V",
            "pwr",
            {
                "r": lbl_h / 2,
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(lhs_pitch),
            },
        )
    ],
    [
        (
            "RESET",
            "other",
            {
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(lhs_pitch),
                "label_style": "start",
            },
        ),
        ("QSPI_CSn", "default", cfg_end),
    ],
    [
        (
            "GND",
            "gnd",
            {
                "r": lbl_h / 2,
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(lhs_pitch),
            },
        )
    ],
    [
        (
            "VIN",
            "pwr",
            {
                "r": lbl_h / 2,
                "width": lbl_w_lg,
                "height": lbl_h,
                "offset": next(lhs_pitch),
            },
        )
    ],
]


#########################################################
#
# LED labels
#
#########################################################

led_pitch = pitch_generator((200, 85), (-112, -30))
leds = [
    [
        (
            "Power",
            "led",
            {
                "r": lbl_h / 2,
                "style": "smooth_bend",
                "width": lbl_w_xl,
                "height": lbl_h,
                "offset": next(led_pitch),
            },
        )
    ],
    [
        (
            "LED_BUILTIN",
            "led",
            {
                "r": lbl_h / 2,
                "style": "smooth_bend",
                "width": lbl_w_xl,
                "height": lbl_h,
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
    '<tspan class="p">Pinout diagram create with <tspan class="italic">pinout (v0.0.10)</tspan></tspan>',
    '<tspan class="p">A Python package for creating pinout diagrams.</tspan>',
    '<tspan class="p"><tspan class="strong"><a href="https://pinout.readthedocs.io">pinout.readthedocs.io</a></tspan></tspan>',
]
para_2 = [
    '<tspan class="p">NOTE: This is not official documentation.</tspan>',
    '<tspan class="p">Diagram aesthetics from Arduino docs.</tspan>',
    '<tspan class="p"><tspan class="strong"><a href="https://www.arduino.cc/">https://www.arduino.cc/</a></tspan></tspan>',
]