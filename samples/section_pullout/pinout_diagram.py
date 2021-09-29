###########################################
#
# Example script to build a pinout diagram
# featuring a detail 'pull-out'.
#
# Export the diagram via commandline:
# >>> py -m pinout.manager --export pinout_diagram.py diagram.svg
#
###########################################

from pinout.core import Group, Image, Rect, ClipPath
from pinout.components.annotation import AnnotationLabel
from pinout.components.layout import Diagram, Panel
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.text import TextBlock
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
# This will be referenced multiple times so
# storing a reference copy in diagram.defs
hardware_img = diagram.add_def(Image("hardware_18pin.png"))

# Create the layout
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

##############################################################
#
# Construct pinout graphic with annotation label
#
##############################################################

# Create a group to hold the annotated image.
group_annotations = panel_main.add(
    Group(
        x=panel_main.width // 2,
        y=20,
    )
)

# Add an image to 'group_annotations'
# It has been offset here for easy center alignment
hardware = group_annotations.add(Image(hardware_img, x=-110))

# Add an annotation to 'group_annotations'
# Its positioning uses transformed coordinates from 'hardware'
# A custom body and target have been supplied to suit requirements.
group_annotations.add(
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
group_detail = panel_detail.add(Group(tag="graphic-detail"))

# Add a rotated instance of 'hardware_img'.
# It has been offset (x=300) so its origin
# is still at the components top-left.
hardware_sm = group_detail.add(
    Image(
        hardware_img,
        x=300,
        rotate=90,
    )
)

# Create and apply a clipping path to 'hardware_sm'
hardware_sm.clip = ClipPath(Rect(x=0, y=0, width=80, height=220))


# Add pin-labels to the x2 rows of pin headers
group_detail.add(
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
group_detail.add(
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


# With content added the width of 'group_detail' can be
# calculated and the component aligned in its panel.
group_detail.x = (
    panel_detail.inset_width - group_detail.width
) / 2 - group_detail.bounding_rect().x

group_detail.y = (panel_detail.inset_height - group_detail.height) / 2


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
