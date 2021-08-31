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
        x = panel_main.width,
        y = 0,
        width = content.inset_width - panel_main.width,
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


##############################################################
#
# Construct pinout graphic with annotation label
#
##############################################################

# Create a group to hold pinout components.
graphic_main = panel_main.add(
    Group(
        x= panel_main.width // 2, 
        y=20,
    )
)
hardware = graphic_main.add(Image(hardware_img, x=-110))

graphic_main.add(
    AnnotationLabel(
        x=hardware.coord("annotation").x,
        y=hardware.coord("annotation").y,
        content="Section A",
        body={"x":20, "y":60, "width":120},
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
panel_detail.add(TextBlock(
    content=data.section_a_text,
    x=20,
    y=40
))

# Create a clip-path to mask the hardware image
clip_01 = diagram.add_def(ClipPath())
clip_01.add(Rect(x=0, y=230, width=220, height=80))

# Create a group to hold components for a second graphic
graphic_detail = panel_detail.add(
    Group(
        x=panel_detail.inset_width // 2 - clip_01.height // 2, 
        y=panel_detail.inset_height // 2
    )
)

# Create an Image, referencing the existing one, and mask it with the clip-path
hardware_detail = graphic_detail.add(Image(hardware_img, x=300, y=-80, rotate=90))
hardware_detail.clip_id = clip_01.id

# Add pin-labels to the x2 rows of pin headers
graphic_detail.add(
    PinLabelGroup(
        x=hardware_detail.coord("pin5").x,
        y=hardware_detail.coord("pin5").y,
        pin_pitch=hardware_detail.coord("pin_pitch_v", True),
        label_start=(60, 0),
        label_pitch=(0, 30),
        scale=(1, 1),
        labels=data.lower_header_in,
    )
)
graphic_detail.add(
    PinLabelGroup(
        x=hardware_detail.coord("pin9").x,
        y=hardware_detail.coord("pin9").y,
        scale=(-1, 1),
        pin_pitch=hardware_detail.coord("pin_pitch_v", True),
        label_start=(60, 0),
        label_pitch=(0, 30),
        labels=data.lower_header_out,
        leaderline=lline.Curved(direction="vh"),
    )
)

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
