legend = [
    ("Analog", "analog"),
    ("Communication", "comms"),
    ("Ground", "gnd"),
    ("GPIO", "gpio"),
    ("LED", "led"),
    ("Power", "pwr"),
    ("PWM", "pwm"),
]

# Pinlabels
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

# Text

title = "<tspan class='h1'>pinout</tspan>"

desc = """<tspan class='italic'>pinout</tspan> is a Python application to assist
with documentation of electronic hardware. 
Development is active with a goal to convert 
a promising idea into a useful tool.

More info: <tspan class='strong'>www.readthedocs.pinout</tspan>"""