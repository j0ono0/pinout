from pinout.config import PinConfig
from pinout import config
from pinout.components.pinlabel import Label
from pinout.components import leaderline as lline

rhs = [
    [
        ("Vcc", "pwr--3v3"),
    ],
    [
        ("GND", "gnd"),
    ],
    [
        ("3", "gpio"),
        ("Lc2a", "analog"),
        ("Lc2b", "led"),
    ],
    [
        ("4", "gpio"),
        ("Lc3a", "analog"),
    ],
]

lhs = [
    [
        ("0", "gpio"),
        ("Lb0a", "gpio"),
        ("Lb03", "comms"),
    ],
    [
        ("1", "gpio"),
        # ("Lc1a", "comms"),
        Label("Lc1a", "comms", offset=(60, 0), scale=(-1, 1)),
    ],
    [
        ("2", "gpio"),
        ("Lc2a", "analog", {"offset": (60, 0)}),
        ("Lc2b", "led"),
    ],
    [
        ("RESET", "pwr"),
    ],
]

btm_lhs = [
    [
        ("3", "gpio"),
        ("Lc2a", "analog"),
        ("Lc2b", "led"),
    ],
    [
        ("4", "gpio"),
        ("Lc2a", "pwm"),
        ("Lc2b", "led"),
    ],
]

btm_rhs = [
    [
        ("6", "gpio"),
        ("Lc3a", "analog"),
    ],
    [
        ("5", "gpio"),
        ("Lc2a", "pwm"),
        ("Lc2b", "led"),
    ],
]

aux_1 = [
    ("a", "led"),
    ("AUX_a", "analog"),
]

aux_2 = [
    ("b", "led"),
    ("AUX_b", "pwm"),
    ("PWM", "pwm"),
]
"""


    # Left interior pin
    {
        "x": 47,
        "y": 80,
        "offset": (-107, -100),
        "labels": [
            [("a", "led"), ("AUX_a", "analog")],
        ],
    },
    # Right interior pin
    {
        "x": 62,
        "y": 95,
        "pitch": (30, 0),
        "offset": (-122, -145),
        "labels": [
            [("b", "led"), ("AUX_b", "pwm"), ("PWM", "pwm")],
        ],
    },
]
"""