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
        ("Lc1a", "comms", {"offset": (92, 0)}),
    ],
    [
        ("2", "gpio"),
        ("Lc2a", "analog"),
        ("Lc2b", "led"),
    ],
    [
        ("RESET", "pwr", {"offset": (232, 0)}),
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

aux = [
    [
        ("a", "led"),
        ("AUX_a", "analog"),
    ],
    [
        ("b", "led"),
        ("AUX_b", "pwm"),
        ("PWM", "pwm"),
    ],
]
