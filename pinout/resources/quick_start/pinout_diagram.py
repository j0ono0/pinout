###########################################
#
# Example script to build a
# pinout diagram. Includes basic
# features and convenience classes.
#
###########################################

from pinout.core import Group, Image
from pinout.components.layout import Diagram, Panel
from pinout.components.pinlabel import PinLabelGroup, PinLabel
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline
from pinout.components.legend import Legend


# Import data for the diagram
import data

# Create a new diagram
diagram = Diagram(1024, 576, "diagram")

# Add a stylesheet
diagram.add_stylesheet("styles.css", embed=True)

# Create a layout
content = diagram.add(
    Panel(
        width=1024,
        height=576,
        inset=(2, 2, 2, 2),
    )
)
panel_main = content.add(
    Panel(
        width=content.inset_width,
        height=440,
        inset=(2, 2, 2, 2),
        tag="panel--main",
    )
)
panel_info = content.add(
    Panel(
        x=0,
        y=panel_main.height,
        width=panel_main.width,
        height=content.inset_height - panel_main.height,
        inset=(2, 2, 2, 2),
        tag="panel--info",
    )
)

# Create a group to hold the pinout-diagram components.
graphic = panel_main.add(Group(400, 42))


# Add and embed an image
hardware = graphic.add(Image("hardware.png", embed=True))

# Measure and record key location with the hardware Image instance
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

# Create a title and a text-block
title_block = panel_info.add(
    TextBlock(
        data.title,
        x=20,
        y=30,
        line_height=18,
        tag="panel title_block",
    )
)
panel_info.add(
    TextBlock(
        data.description,
        x=20,
        y=60,
        width=title_block.width,
        height=panel_info.height - title_block.height,
        line_height=18,
        tag="panel text_block",
    )
)

# Create a legend
legend = panel_info.add(
    Legend(
        data.legend,
        x=340,
        y=8,
        max_height=132,
    )
)

# Export the diagram via commandline:
# >>> py -m pinout.manager --export pinout_diagram diagram.svg