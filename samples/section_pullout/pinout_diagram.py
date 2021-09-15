###########################################
#
# Example script to build a pinout diagram
# featuring a detail 'pull-out'.
#
# Export the diagram via commandline:
# >>> py -m pinout.manager --export pinout_diagram diagram.svg
#
###########################################

from pinout.core import Group, Image, Rect
from pinout.components.annotation import AnnotationLabel
from pinout.components.layout import Diagram, Panel, ClipPath
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline
from pinout.components.legend import Legend


# Import data for the diagram
import data


##############################################################
#
# Create a diagram and layout
#
##############################################################

diagram = Diagram(1024, 576, "diagram")

# Add stylesheet
diagram.add_stylesheet("styles.css")

# Add hardware image
hardware_img = diagram.add_def(Image("hardware_18pin.png"))

# Create layout
content = diagram.add(
    Panel(
        width=1024,
        height=576,
        inset=(2, 2, 2, 2),
    )
)
panel_main = content.add(
    Panel(
        x=0,
        y=0,
        width=content.inset_width // 3,
        height=440,
        inset=(2, 2, 2, 2),
        tag="panel--main",
    )
)
panel_detail = content.add(
    Panel(
        x=panel_main.width,
        y=0,
        width=content.inset_width - panel_main.width,
        height=440,
        inset=(2, 2, 2, 2),
        tag="panel--detail",
    )
)
panel_info = content.add(
    Panel(
        x=0,
        y=panel_main.height,
        width=content.inset_width,
        height=content.inset_height - panel_main.height,
        inset=(2, 2, 2, 2),
        tag="panel--info",
    )
)


##############################################################
#
# Measuring key coordinates on hardware image
#
##############################################################

hardware_img.add_coord("pin5", 65, 253)
hardware_img.add_coord("pin9", 65, 284)
hardware_img.add_coord("annotation", 110, 268)
hardware_img.add_coord("pin_pitch_v", 0, 30)

hardware_img.add_coord("origin", 0, 0)
hardware_img.add_coord("size", hardware_img.width, hardware_img.height)

##############################################################
#
# Construct pinout graphic with annotation label
#
##############################################################

# Create a group to hold pinout components.
graphic_main = panel_main.add(
    Group(
        x=panel_main.width // 2,
        y=20,
    )
)
hardware = graphic_main.add(Image(hardware_img, x=-110))

graphic_main.add(
    AnnotationLabel(
        x=hardware.coord("annotation").x,
        y=hardware.coord("annotation").y,
        content="Section A",
        body={"x": 20, "y": 60, "width": 120},
        target={"x": -120, "y": -40, "width": 240, "height": 80},
        scale=(-1, 1),
    )
)


##############################################################
#
# Construct a 'pull-out' graphic with pin-labels
#
##############################################################

# Create a title and text for the diagram section
panel_detail.add(TextBlock(content=data.section_a_text, x=20, y=40))


# Create a group to hold components for a second graphic
graphic_detail = Group(x=0, y=0, tag="graphic-detail")

hardware_sm = graphic_detail.add(Image(hardware_img, width=110, rotate=90))
tx, ty = hardware_sm.coord("origin")
tw, th = hardware_sm.coord("size", True)

hardware_sm.clip = ClipPath(Rect(x=tx - th, y=0, width=50, height=110))


# Add pin-labels to the x2 rows of pin headers
graphic_detail.add(
    PinLabelGroup(
        x=hardware_sm.coord("pin5").x,
        y=hardware_sm.coord("pin5").y,
        pin_pitch=hardware_sm.coord("pin_pitch_v", True),
        label_start=(60, 0),
        label_pitch=(0, 30),
        scale=(1, 1),
        labels=data.lower_header_in,
    )
)
graphic_detail.add(
    PinLabelGroup(
        x=hardware_sm.coord("pin9").x,
        y=hardware_sm.coord("pin9").y,
        scale=(-1, 1),
        pin_pitch=hardware_sm.coord("pin_pitch_v", True),
        label_start=(60, 0),
        label_pitch=(0, 30),
        labels=data.lower_header_out,
    )
)


# With content added the width of 'graphic_detail' can be calculated
# and the component aligned in it's panel

graphic_detail.x = (
    panel_detail.inset_width - graphic_detail.width
) / 2 - graphic_detail.bounding_rect().x

graphic_detail.y = (panel_detail.inset_height - graphic_detail.height) / 2


# Add graphic_detail *after* calculating position
panel_detail.add(graphic_detail)

##############################################################
#
# Add content to the title bar
#
##############################################################

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
        x=640,
        y=8,
        max_height=132,
    )
)
