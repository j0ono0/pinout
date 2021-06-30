###########################################
#
# Example script to build a pinout diagram
# Includes examples of all features
#
###########################################

from pinout.core import Diagram, Group, Rect, Image, Text
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.annotation import AnnotationLabel
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline
from pinout.components.legend import Legend

import data

# Create a new diagram and add a background
diagram = Diagram(1200, 675, "diagram")
diagram.add(Rect(0, 0, 1200, 675, "diagram__bg"))


# Add a stylesheet
diagram.add_stylesheet("styles.css", True)


# Create a panels to group content together
panel_main = diagram.add(Group(2, 2, "panel panel--main"))
panel_main.add(Rect(0, 0, 856, 671, "panel__bg"))

# Create a group to hold the pinout-diagram components.
graphic = panel_main.add(Group(318, 200))

# Add and embed an image
graphic.add(Image("hardware.png", width=220, height=300, embed=True))


# Add a pinlabels to the right header
graphic.add(
    PinLabelGroup(
        x=204,
        y=106,
        pin_pitch=(0, 30),
        label_start=(60, 0),
        label_pitch=(0, 30),
        labels=data.rhs,
    )
)

# Add a pinlabels to the left header
graphic.add(
    PinLabelGroup(
        x=16,
        y=106,
        pin_pitch=(0, 30),
        label_start=(60, 0),
        label_pitch=(0, 30),
        scale=(-1, 1),
        labels=data.lhs,
    )
)

# Add a pinlabels to the left header
graphic.add(
    PinLabelGroup(
        x=65,
        y=284,
        pin_pitch=(30, 0),
        label_start=(109, 60),
        label_pitch=(0, 30),
        scale=(-1, 1),
        labels=data.btm_lhs,
        leaderline=lline.Curved(direction="vh"),
    )
)

# Add a pinlabels to the left header
graphic.add(
    PinLabelGroup(
        x=155,
        y=284,
        pin_pitch=(-30, 0),
        label_start=(109, 60),
        label_pitch=(0, 30),
        labels=data.btm_rhs,
        leaderline=lline.Curved(direction="vh"),
    )
)

graphic.add(
    PinLabelGroup(
        x=47,
        y=80,
        scale=(-1, -1),
        pin_pitch=(15, 15),
        label_start=(91, 110),
        label_pitch=(0, 30),
        labels=data.aux,
        leaderline=lline.Curved(direction="vh"),
    )
)


graphic.add(
    AnnotationLabel(
        content=data.annotation_usb,
        x=110,
        y=0,
        scale=(1, -1),
        body={"width": 125},
    )
)

graphic.add(
    AnnotationLabel(
        content=data.annotation_led,
        x=87,
        y=85,
        scale=(1, -1),
        target={"x": -20, "y": -20, "width": 40, "height": 40, "corner_radius": 20},
        body={"y": 168, "width": 125},
    )
)

title_block = diagram.add(
    TextBlock(
        [data.title],
        x=860,
        y=2,
        width=338,
        height=60,
        offset=(10, 40),
        line_height=18,
        tag="panel title_block",
    )
)

legend = diagram.add(
    Legend(
        data.legend,
        x=860,
        y=title_block.y + title_block.height + 2,
        max_height=132,
    )
)

description = diagram.add(
    TextBlock(
        data.desc.split("\n"),
        x=860,
        y=legend.y + legend.height + 2,
        width=338,
        height=100,
        offset=(10, 18),
        line_height=18,
        tag="panel text_block",
    )
)

diagram.add(
    TextBlock(
        data.notes.split("\n"),
        x=860,
        y=description.y + description.height + 2,
        width=338,
        height=diagram.height - (description.bounding_coords().y2) - 4,
        offset=(10, 18),
        line_height=18,
        tag="panel text_block",
    )
)

# Export final SVG diagram
diagram.export("pinout_diagram.svg", True)