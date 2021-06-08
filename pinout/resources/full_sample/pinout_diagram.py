###########################################
#
# Example script to build a pinout diagram
# Includes examples of all features
#
###########################################

from pinout.core import Diagram, Group, Rect, Image, Text
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.annotation import AnnotationLabel
from pinout.components.type import TextBlock
from pinout.components import leaderline as lline
from pinout.components.legend import Legend

import data

# Create a new diagram and add a background
diagram = Diagram(1200, 675, "diagram")
diagram.add(Rect(0, 0, 1200, 675, "diagram__bg"))


# Add a stylesheet
diagram.add_stylesheet("styles.css", True)


# Create some panels to group content together
# and add backgrounds to them
panel_main = diagram.add(Group(2, 2, "panel--main"))
panel_main.add(Rect(0, 0, 856, 671, "bg"))

panel_meta = diagram.add(Group(860, 2, "panel--meta"))
panel_meta.add(Rect(0, 0, 338, 671, "bg"))


# Create a group to hold the pinout-diagram components.
graphic = panel_main.add(Group(325, 200))

# Add and embed an image
graphic.add(Image("hardware.png", width=220, height=300, embed=True))


# Add a pinlabels to the right header
graphic.add(
    PinLabelGroup(
        x=204,
        y=106,
        pin_pitch=(0, 30),
        label_start=(60, 0),
        label_pitch=(0, 0),
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
        label_pitch=(0, 0),
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
        label_pitch=(30, 30),
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
        label_pitch=(30, 30),
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
        label_pitch=(15, 45),
        labels=data.aux,
        leaderline=lline.Curved(direction="vh"),
    )
)


graphic.add(
    AnnotationLabel(
        ["USB-C connector", "Host/device functionality"],
        x=110,
        y=0,
        scale=(1, -1),
    )
)

graphic.add(
    AnnotationLabel(
        ["Onboard", "LED"],
        x=86.5,
        y=85,
        scale=(1, -1),
        target={"x": -20, "y": -20, "width": 40, "height": 40},
        body={"y": 168, "width": 125},
    )
)

panel_meta.add(Text(data.title, x=10, y=40))
panel_meta.add(
    TextBlock(
        data.desc.split("\n"),
        x=10,
        y=220,
        line_height=18,
    )
)

panel_meta.add(Legend(data.legend, x=0, y=60, max_height=112))

# Export final SVG diagram
diagram.export("pinout_diagram.svg", True)