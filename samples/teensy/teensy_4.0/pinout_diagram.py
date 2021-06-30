# Teensy 4.0 Pinout
# https://www.pjrc.com/store/teensy40.html

from pinout.core import Diagram, Rect, Group, Image

from pinout.components.pinlabel import PinLabelGroup
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline

import data

# Create a new diagram and add a background
diagram = Diagram(1280, 720, "diagram")
diagram.add(Rect(0, 0, 1280, 720, "diagram__bg"))

# Add a stylesheet
diagram.add_stylesheet("styles.css", True)

# Create a layout
panel_main = diagram.add(Group(2, 2, "panel panel--main"))
panel_main.add(Rect(0, 0, 1276, 576, "panel__bg"))


# Create a group to hold the actual diagram components.
graphic = panel_main.add(Group(420, 25))

# Custom legend
legend = diagram.add(Group(1132, 0, "legend"))
legend.add(Rect(0, 0, 148, 720, "legend__bg panel__bg"))

# Title bar
titlebar = diagram.add(Group(2, 580, "titlebar"))
titlebar.add(Rect(0, 0, 1130, 138, "titlebar__bg panel__bg"))

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
        label_start=(60, 0),
        label_pitch=(0, 30),
        labels=data.header_rhs,
    )
)

# Pinlabels: Left header
graphic.add(
    PinLabelGroup(
        x=15,
        y=32,
        scale=(-1, 1),
        pin_pitch=(0, 30),
        label_start=(60, 0),
        label_pitch=(0, 30),
        labels=data.header_lhs,
    )
)

# Pinlabels: End, left side
graphic.add(
    PinLabelGroup(
        x=45,
        y=422,
        scale=(-1, 1),
        pin_pitch=(30, 0),
        label_start=(90, 30),
        label_pitch=(0, 30),
        labels=data.header_end_lhs,
        leaderline=lline.Curved(direction="vh"),
        body={"width": 166},
    )
)

# Pinlabels: End, right side
graphic.add(
    PinLabelGroup(
        x=135,
        y=422,
        pin_pitch=(30, 0),
        label_start=(120, 90),
        label_pitch=(0, -30),
        labels=data.header_end_rhs,
        leaderline=lline.Curved(direction="vh"),
        body={"width": 166},
    )
)

# Legend entries
entry_height = 87.5
for ind, (entry, tag) in enumerate(data.legend_content):

    legend.add(
        TextBlock(
            entry.split("\n"),
            x=4,
            y=2 + ind * (entry_height + 2),
            width=140,
            height=entry_height,
            offset=(10, 20),
            line_height=18,
            tag=f"{tag} legend__entry",
        )
    )

titlebar.add(
    TextBlock(
        data.title,
        x=20,
        y=38,
        offset=(0, 0),
        line_height=18,
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