###########################################
#
# Example script to build a
# pinout diagram. Includes basic
# features and convenience classes.
#
###########################################

from pinout.core import Group, Image
from pinout.components.layout import Diagram_2Row
from pinout.components.pinlabel import PinLabelGroup, PinLabel
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline
from pinout.components.legend import Legend


# Import data for the diagram
import data

# Create a new diagram
# The Diagram_2Row class provides 2 panels,
# 'panel_01' and 'panel_02', to insert components into.
diagram = Diagram_2Row(1024, 576, 440, "diagram")

# Add a stylesheet
diagram.add_stylesheet("styles.css", embed=True)

# Create a group to hold the pinout-diagram components.
graphic = diagram.panel_01.add(Group(400, 42))

# Add and embed an image
hardware = graphic.add(Image("hardware.png", embed=True))

# Measure and record key locations with the hardware Image instance
hardware.add_coord("gpio0", 16, 100)
hardware.add_coord("gpio3", 65, 244)
hardware.add_coord("reset", 155, 244)
hardware.add_coord("vcc", 206, 100)
# Other (x,y) pairs can also be stored here
hardware.add_coord("pin_pitch_v", 0, 30)
hardware.add_coord("pin_pitch_h", 30, 0)

# Create a single pin label
graphic.add(
    PinLabel(
        content="RESET",
        x=hardware.coord("reset").x,
        y=hardware.coord("reset").y,
        tag="pwr",
        body={"x": 117, "y": 30},
        leaderline={"direction": "vh"},
    )
)

# Create pinlabels on the right header
graphic.add(
    PinLabelGroup(
        x=hardware.coord("vcc").x,
        y=hardware.coord("vcc").y,
        pin_pitch=hardware.coord("pin_pitch_v", raw=True),
        label_start=(60, 0),
        label_pitch=(0, 30),
        labels=data.right_header,
    )
)

# Create pinlabels on the left header
graphic.add(
    PinLabelGroup(
        x=hardware.coord("gpio0").x,
        y=hardware.coord("gpio0").y,
        pin_pitch=hardware.coord("pin_pitch_v", raw=True),
        label_start=(60, 0),
        label_pitch=(0, 30),
        scale=(-1, 1),
        labels=data.left_header,
    )
)

# Create pinlabels on the lower header
graphic.add(
    PinLabelGroup(
        x=hardware.coord("gpio3").x,
        y=hardware.coord("gpio3").y,
        scale=(-1, 1),
        pin_pitch=hardware.coord("pin_pitch_h", raw=True),
        label_start=(110, 30),
        label_pitch=(0, 30),
        labels=data.lower_header,
        leaderline=lline.Curved(direction="vh"),
    )
)

# Create a title and description text-blocks
title_block = diagram.panel_02.add(
    TextBlock(
        data.title,
        x=20,
        y=30,
        line_height=18,
        tag="panel title_block",
    )
)
diagram.panel_02.add(
    TextBlock(
        data.description,
        x=20,
        y=60,
        width=title_block.width,
        height=diagram.panel_02.height - title_block.height,
        line_height=18,
        tag="panel text_block",
    )
)

# Create a legend
legend = diagram.panel_02.add(
    Legend(
        data.legend,
        x=340,
        y=8,
        max_height=132,
    )
)

# Export the diagram via commandline:
# >>> py -m pinout.manager --export pinout_diagram diagram.svg
