from pinout import config
from pinout.components import integrated_circuits as ic
from pinout.components.legend import Legend
from pinout.components.layout import Diagram, Group, Panel
from pinout.components.text import TextBlock

legend_data = [
    ("Port", "port"),
    ("Analog", "adc"),
    ("Analog Comparator", "comparator"),
    ("Ground", "gnd"),
    ("Interrupt", "interrupt"),
    ("Timer-counter", "timer-counter"),
    ("Communications", "comms"),
    ("Oscillator", "oscillator"),
    ("Power", "pwr"),
]

attiny85 = [
    [
        ("PB5", "port"),
        ("dW", "port"),
        ("ADC0", "adc"),
        ("RESET", "gnd"),
        ("PCINT5", "interrupt"),
    ],
    [
        ("PB3", "port"),
        ("ADC3", "adc"),
        ("OC1B", "timer-counter"),
        ("CLKI", "comms"),
        ("XTAL1", "oscillator"),
        ("PCINT3", "interrupt"),
    ],
    [
        ("PB4", "port"),
        ("ADC2", "adc"),
        ("OC1B", "timer-counter"),
        ("CLKO", "port"),
        ("XTAL2", "oscillator"),
        ("PCINT4", "interrupt"),
    ],
    [
        ("GND", "gnd"),
    ],
    [
        ("PB0", "port"),
        ("MOSI", "comms"),
        ("DI", "comms"),
        ("SDA", "comms"),
        ("AIN0", "comparator"),
        ("OC0A", "timer-counter"),
        ("OC1A", "timer-counter"),
        ("AREF", "pwr"),
        ("PCINT0", "interrupt"),
    ],
    [
        ("PB1", "port"),
        ("MISO", "comms"),
        ("DO", "comms"),
        ("AIN1", "comparator"),
        ("OC0B", "timer-counter"),
        ("OC1A", "timer-counter"),
        ("PCINT1", "interrupt"),
    ],
    [
        ("PB2", "port"),
        ("SCK", "comms"),
        ("USCK", "comms"),
        ("SCL", "comms"),
        ("ADC1", "adc"),
        ("T0", "timer-counter"),
        ("INT0", "interrupt"),
        ("PCINT2", "interrupt"),
    ],
    [
        ("VCC", "pwr"),
    ],
]

attiny85_QFN = (
    attiny85[0:2]
    + [[("DNC", "dnc")]] * 2
    + attiny85[2:3]
    + [[("DNC", "dnc")]] * 2
    + attiny85[3:4]
    + [[("DNC", "dnc")]] * 2
    + attiny85[4:6]
    + [[("DNC", "dnc")]]
    + attiny85[6:]
    + [[("DNC", "dnc")]] * 5
)

# Modify default config
config.pinlabel["body"]["width"] = 50
config.ic_qfp["inset"] = (3, 3, 3, 3)
config.panel["inset"] = (1.5, 1.5, 1.5, 1.5)
config.legend["entry"]["width"] = 200
config.legend["entry"]["inset"] = 0

# Add pin numbers in a list comprehension
attiny85_numbered = [
    [(f"{i+1}", "pin_id", {"body": {"width": 20, "height": 15}})] + row
    for i, row in enumerate(attiny85)
]


diagram = Diagram(1200, 675)
diagram.add_stylesheet("attiny_styles.css")
content = diagram.add(Panel(width=1200, height=675))
dip_panel = content.add(Panel(x=0, y=0, width=content.inset_width, height=200))
qfn_panel = content.add(Panel(x=0, y=200, width=content.inset_width, height=360))
title_panel = content.add(
    Panel(
        x=0,
        y=qfn_panel.bounding_coords().y2,
        width=content.inset_width,
        height=content.inset_height - qfn_panel.bounding_coords().y2,
        tag="panel__title",
    )
)

dip_panel.add(
    TextBlock("<tspan class='panel__title'>PDIP / SOIC / TSSOP</tspan>", x=10, y=30)
)
dip_graphic = dip_panel.add(Group(450, 50))
dip_graphic.add(
    ic.labelled_dip(labels=attiny85_numbered, width=110, height=120, label_start_x=50)
)

qfn_numbered = [
    [(f"{i+1}", "pin_id", {"body": {"width": 20, "height": 15}})] + row
    for i, row in enumerate(attiny85_QFN)
]
qfn_panel.add(TextBlock("<tspan class='panel__title'>QFN / MLF</tspan>", x=10, y=30))
qfn_graphic = qfn_panel.add(Group(500, 110))
qfn_graphic.add(ic.labelled_qfn(labels=qfn_numbered, length=100, label_start=(50, 10)))


title_panel.add(
    TextBlock(
        [
            "<tspan class='diagram__title'>Pinout ATtiny25/45/85</tspan>",
            "Created with <tspan class='italic'>pinout</tspan> Python package.",
            "pinout.readthedocs.io",
        ],
        x=10,
        y=30,
    )
)
title_panel.add(
    Legend(
        legend_data,
        max_height=96,
        x=title_panel.width - 614,
        y=14,
    )
)
