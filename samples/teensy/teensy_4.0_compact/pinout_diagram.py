# Teensy 4.0 Pinout
# https://www.pjrc.com/store/teensy40.html

from pinout.core import Diagram, Rect, Group, Image
from pinout import config
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.type import TextBlock
from pinout.components import leaderline as lline

import data

# Override default config settings
config.pinlabel["body"]["x"] = 0
config.pinlabel["body"]["height"] = 28
config.pinlabel["body"]["corner_radius"] = 0

################################################
# EXPERIMENTAL: DATA PREPROCESSOR
# modify data based on its tag name
# to further minimise config in data


def update_config(source, update):
    for k, v in update.items():
        if type(v) is dict:
            source[k] = source.get(k, {})
            update_config(source[k], v)
        else:
            source[k] = v
    return source


def data_preprocessor(data_list):
    for row in data_list:
        for i, label in enumerate(row):
            try:
                data_config = label[2]
            except IndexError:
                data_config = {}

            config = {}
            if label[1] in ["digital", "analog"]:
                config = {"body": {"width": 40}}
            elif label[1] in ["pwm"]:
                config = {"body": {"width": 60}}

            update_config(config, data_config)

            row[i] = (label[0], label[1], config)
        yield row


################################################
# Using SASS here to try out some
# more succinct style documentation.
# It is not required for pinout but
# might suit some workflows.

# build css from scss
import sass

with open("styles.scss", "r") as f:
    styles = sass.compile(string=f.read())

with open("styles.css", "w") as f:
    f.write(styles)

################################################

# Create a new diagram and add a background
# Official Teensy pinout cards are 1.41 ratio (or very close)
# and comfortable to read at approx A6 dimensions 148mm x 105mm
# 10 "units" is equal to 1mm if printed at A6
diagram = Diagram(1128, 800, "diagram")

diagram.add(Rect(0, 0, 1128, 800, "diagram__bg"))

# Add a stylesheet
diagram.add_stylesheet("styles.css", True)

# Create a layout
panel_main = diagram.add(Group(10, 10, "panel panel--main"))
panel_main.add(Rect(0, 0, 1108, 638, "mainpanel__bg"))


# Create a group to hold the actual diagram components.
graphic = panel_main.add(Group(340, 25, scale=(1.1, 1.1)))

# Custom legend
legend = diagram.add(Group(971, 10, "legend"))
legend.add(Rect(0, 0, 147, 780, "legend__bg panel__bg"))

# Title bar
titlebar = diagram.add(Group(10, 650, "titlebar"))
titlebar.add(Rect(0, 0, 961, 140, "titlebar__bg panel__bg"))

# Add and embed an image
graphic.add(
    Image(
        "hardware_teensy_4.0_front.svg",
        x=-8.5,
        y=-7.5,
        width=210,
        height=340,
        embed=True,
    )
)

# Pinlabels: Right header
graphic.add(
    PinLabelGroup(
        x=195,
        y=32,
        pin_pitch=(0, 30),
        label_start=(40, 0),
        label_pitch=(0, 30),
        labels=data_preprocessor(data.header_rhs),
    )
)

# Pinlabels: Left header
graphic.add(
    PinLabelGroup(
        x=15,
        y=32,
        scale=(-1, 1),
        pin_pitch=(0, 30),
        label_start=(40, 0),
        label_pitch=(0, 30),
        labels=data_preprocessor(data.header_lhs),
    )
)

# Pinlabels: End, left side
graphic.add(
    PinLabelGroup(
        x=45,
        y=422,
        scale=(-1, 1),
        pin_pitch=(30, 0),
        label_start=(70, 30),
        label_pitch=(0, 30),
        labels=data.header_end_lhs,
        leaderline=lline.Curved(direction="vh"),
    )
)

# Pinlabels: End, right side
graphic.add(
    PinLabelGroup(
        x=135,
        y=422,
        pin_pitch=(30, 0),
        label_start=(100, 90),
        label_pitch=(0, -30),
        labels=data.header_end_rhs,
        leaderline=lline.Curved(direction="vh"),
    )
)

# Legend entries
gutter = 2
entry_height = 95.75
for ind, (entry, tag) in enumerate(data.legend_content):

    legend.add(
        TextBlock(
            entry.split("\n"),
            x=gutter,
            y=0 + ind * (entry_height + gutter),
            width=145,
            height=entry_height,
            offset=(8, 26),
            line_height=19,
            tag=f"{tag} legend__entry",
        )
    )

titlebar.add(
    TextBlock(
        data.title,
        x=20,
        y=38,
        offset=(0, 0),
        line_height=16,
        tag="h1",
    )
)
titlebar.add(
    TextBlock(
        data.title_2.split("\n"),
        x=20,
        y=48,
        offset=(8, 18),
        line_height=18,
        tag="h2",
    )
)
titlebar.add(
    TextBlock(
        data.instructions.split("\n"),
        x=20,
        y=90,
        offset=(8, 18),
        line_height=18,
        tag="p",
    )
)
titlebar.add(
    TextBlock(
        data.notes.split("\n"),
        x=395,
        y=72,
        offset=(8, 18),
        line_height=18,
        tag="p",
    )
)


# Export final SVG diagram
diagram.export("teensy_4.0_front_pinout_diagram.svg", True)