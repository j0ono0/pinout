###########################################
#
# Example script to build a
# pinout diagram. Includes basic
# features and convenience classes.
#
###########################################

from pinout.core import Diagram, Group, Rect, Image
from pinout.components.pinlabel import PinLabelGroup, Label
from pinout.components.type import TextBlock
from pinout.components import leaderline as lline
from pinout.components.legend import Legend

# Import data for the diagram
import data

# Create a new diagram and add a background
diagram = Diagram(1024, 574, "diagram")
diagram.add(Rect(0, 0, 1024, 576, "diagram__bg"))

# Add a stylesheet
diagram.add_stylesheet("styles.css", True)

# Create a layout for diagram
panel_main = diagram.add(Group(2, 2, "panel panel--main"))
panel_main.add(Rect(0, 0, 1020, 438, "panel__bg"))

info_panel = diagram.add(Group(x=2, y=442, tag="panel panel--info"))
info_panel.add(Rect(0, 0, 1020, 132, tag="panel__bg"))

# Create a group to hold the pinout-diagram components.
graphic = panel_main.add(Group(400, 42))

# Add and embed an image
graphic.add(Image("hardware.png", width=220, height=260, embed=True))

# Create a single pin label
graphic.add(
    Label(
        content="RESET",
        x=155,
        y=244,
        tag="pwr",
        body={"x": 117, "y": 30},
        leaderline={"direction": "vh"},
    )
)

# Create pinlabels on the right header
graphic.add(
    PinLabelGroup(
        x=206,
        y=100,
        pin_pitch=(0, 30),
        label_start=(60, 0),
        label_pitch=(0, 0),
        labels=data.right_header,
    )
)

# Create pinlabels on the left header
graphic.add(
    PinLabelGroup(
        x=16,
        y=100,
        pin_pitch=(0, 30),
        label_start=(60, 0),
        label_pitch=(0, 0),
        scale=(-1, 1),
        labels=data.left_header,
    )
)

# Create pinlabels on the lower header
graphic.add(
    PinLabelGroup(
        x=65,
        y=244,
        scale=(-1, 1),
        pin_pitch=(30, 0),
        label_start=(110, 30),
        label_pitch=(30, 30),
        labels=data.lower_header,
        leaderline=lline.Curved(direction="vh"),
    )
)

# Create a title and a text-block
title_block = info_panel.add(
    TextBlock(
        data.title,
        x=0,
        y=0,
        width=338,
        height=42,
        offset=(20, 33),
        line_height=18,
        tag="panel title_block",
    )
)
info_panel.add(
    TextBlock(
        data.description.split("\n"),
        x=0,
        y=title_block.y + title_block.height,
        width=title_block.width,
        height=info_panel.height - title_block.height,
        offset=(20, 18),
        line_height=18,
        tag="panel text_block",
    )
)

# Create a legend
legend = info_panel.add(
    Legend(
        data.legend,
        x=338,
        y=0,
        max_height=132,
    )
)

# Export final SVG diagram
diagram.export("quick_start_pinout_diagram.svg", True)