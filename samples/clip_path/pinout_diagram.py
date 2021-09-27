##############################################################
#
# Example script demonstrating clipping paths
#
# Export the diagram via commandline:
# >>> py -m pinout.manager -e pinout_diagram diagram.svg
#
##############################################################


from pinout.core import Circle, Group, Image, Rect, ClipPath, Use
from pinout.components.annotation import AnnotationLabel
from pinout.components.layout import Diagram_2Rows, Panel
from pinout.components.legend import Legend
from pinout.components.pinlabel import PinLabelGroup, PinLabel
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline
from pinout import config


##############################################################
#
# Diagram setup
# Create a layout and add an image component
#
# Diagram_2Rows provides 2 panels to add components,
# 'panel_01' and 'panel_02'.
#
##############################################################

diagram = Diagram_2Rows(1200, 675, 500, tag="clip-demo")
diagram.add_stylesheet("styles.css")

# Components added to <defs> do not render but can be referenced
# by other components.
hardware_def = diagram.add_def(Image("hardware_18pin.png"))

# Coordinates and sizes of intended ClipPaths can be measured
# against the reference image and stored here. These coordinates
# are automatically adjusted if the image is transformed.
hardware_def.add_coord("led_loc", 32, 63)
hardware_def.add_coord("led_size", 74, 45)
hardware_def.add_coord("ic_center", 110, 176)


##############################################################
#
# All components have a 'clip' attribute.
# Clip arguments can be an instance of a ClipPath, SvgShape,
# or a list of SvgShapes.
#
##############################################################

# Example of applying a simple clip-path
box01 = diagram.panel_01.add(
    Rect(
        x=0,
        y=0,
        width=1195,
        height=499,
        tag="box01",
        clip=Rect(x=10, y=10, width=589, height=489),
    )
)


##############################################################
#
# Apply clipping to an Image
#
##############################################################

# Grouping components and clipping paths makes positioning easier
group_overlay = diagram.panel_01.add(Group())

# Add a semi-transparent image as a base
group_overlay.add(Image(hardware_def, tag="opacity_40"))

# Create a clip-path
image_clip_path = ClipPath(Rect(x=0, y=230, width=220, height=70))

# Create an image, applying the clip-path to it
overlay_image = group_overlay.add(Image(hardware_def, clip=image_clip_path))

# Now 'group_overlay' is populated its dimensions can be calculated and
# centered over 'box01'.
group_overlay.x = (box01.width - group_overlay.width) / 2
group_overlay.y = (box01.height - group_overlay.height) / 2


##############################################################
#
# Apply clipping to a Group
#
# Aligning the visible section of a clipped component
# at at (0,0) origin can make for more intuative
# layout calculations.
#
##############################################################

# Create a group
led_detail = diagram.panel_01.add(Group())

# Create an image, adding it to 'led_detail'
led_image = led_detail.add(Image(hardware_def))

# Access relevant coordinates form 'led_image'.
led_x, led_y = led_image.coord("led_loc")
led_w, led_h = led_image.coord("led_size", True)

# Realign 'led_image' so the clipped section's top-left
# aligns with its parent's origin.
led_image.x = -led_x
led_image.y = -led_y

# Add a clip-path to 'led_detail'.
led_detail.clip = Rect(
    width=led_w,
    height=led_h,
)

# Locating 'led_detail' is now more intuative as
# its (x,y) location matches with the visible portion
# of its children

led_detail.x = 837
led_detail.y = 150

##############################################################
#
# Succinct version of previous example
#
##############################################################

circle_group = diagram.panel_01.add(
    Group(
        x=874,
        y=300,
        clip=Circle(cx=0, cy=0, r=68),
        children=[
            Image(
                hardware_def,
                x=-hardware_def.coord("ic_center").x,
                y=-hardware_def.coord("ic_center").y,
            )
        ],
    )
)

##############################################################
#
# Additional non ClipPath diagram components
#
##############################################################
diagram.panel_02.add(
    TextBlock(
        """<tspan class="h1">Pinout: ClipPath examples</tspan>
        pinout provides an easy method to create pinout diagrams 
        for electronic hardware.
        
        <tspan class="strong">pinout.readthedocs.io</tspan>""",
        x=20,
        y=30,
    )
)
