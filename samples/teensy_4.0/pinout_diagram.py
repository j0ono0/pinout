# Teensy 4.0 Pinout
# https://www.pjrc.com/store/teensy40.html


# Export final SVG diagram from command-line
# py -m pinout.manager -e pinout_diagram.py teensy_4.0_front_pinout_diagram.svg

# NOTE: this sample requires the python package libsass.
# install via pip:
# >>> pip install libsass

from pinout.core import Group, Image
from pinout import config
from pinout.components.layout import Diagram, Panel
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline


import teensy_4_data as data

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

diagram = Diagram(1128, 800, "diagram")

# Add a stylesheet
diagram.add_stylesheet("styles.css", True)

# Create a layout
diagram_inner = diagram.add(
    Panel(
        x=0,
        y=0,
        width=1128,
        height=800,
        inset=(10, 10, 10, 10),
    )
)

panel_main = diagram_inner.add(
    Panel(
        x=0,
        y=0,
        width=960,
        height=640,
        inset=(1, 1, 1, 1),
        tag="mainpanel",
    )
)

# Create a group to hold the actual diagram components.
graphic = panel_main.add(Group(340, 25, scale=(1.1, 1.1)))

# Custom legend
legend = diagram_inner.add(
    Panel(
        x=panel_main.bounding_coords().x2,
        y=0,
        width=diagram_inner.inset_width - panel_main.width,
        height=diagram_inner.inset_height,
        inset=(1, 1, 1, 1),
        tag="legend",
    )
)

# Title bar
titlebar = diagram_inner.add(
    Panel(
        x=0,
        y=panel_main.height,
        width=panel_main.width,
        height=diagram_inner.inset_height - panel_main.height,
        inset=(1, 1, 1, 1),
        tag="titlebar",
    )
)

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
        tag="pingroup",
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
        tag="pingroup",
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
        tag="pingroup",
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
        tag="pingroup",
    )
)

# Legend entries
entry_count = len(data.legend_content)
entry_height = legend.inset_height / entry_count
for index, (entry_text, tag) in enumerate(data.legend_content):
    legend_entry = legend.add(
        Panel(
            x=0,
            y=entry_height * index,
            width=legend.inset_width,
            height=entry_height,
            inset=(1, 1, 1, 1),
            tag=f"{tag} legend__entry",
        )
    )
    legend_entry.add(
        TextBlock(
            entry_text,
            x=10,
            y=22,
            line_height=19,
        )
    )

titlebar.add(
    TextBlock(
        data.title,
        x=20,
        y=38,
        line_height=16,
        tag="h1",
    )
)
titlebar.add(
    TextBlock(
        data.title_2,
        x=20,
        y=60,
        line_height=18,
        tag="h2",
    )
)
titlebar.add(
    TextBlock(
        data.instructions,
        x=20,
        y=100,
        line_height=18,
        tag="p",
    )
)
titlebar.add(
    TextBlock(
        data.notes,
        x=395,
        y=60,
        line_height=18,
        tag="p",
    )
)
