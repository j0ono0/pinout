###########################################
#
# Example script to build a pinout diagram
# Includes examples of all basic features
#
# Export SVG diagram via command-line:
# >>> py -m pinout.manager --export pinout_diagram.py pinout_diagram.svg -o
#
###########################################
from pinout import config
from pinout.core import Group, Image
from pinout.components.layout import Diagram, Panel
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.annotation import AnnotationLabel
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline
from pinout.components.legend import Legend


import data

# Edit some component default config
config.panel["inset"] = (2, 2, 2, 2)

# Create a new diagram, add styles and a base panel
diagram = Diagram(1200, 675, "diagram")
diagram.add_stylesheet("styles_auto.css", True)
diagram.add_stylesheet("styles.css", True)
content = diagram.add(Panel(width=1200, height=675, tag="panel__content"))


# Create panels to from a graphical layout

panel_graphic = content.add(
    Panel(
        width=860,
        height=content.inset_height,
        tag="panel__graphic",
    )
)
panel_title = content.add(
    Panel(
        x=panel_graphic.width,
        y=0,
        width=content.inset_width - panel_graphic.width,
        height=60,
        tag="panel__title",
    )
)
panel_legend = content.add(
    Panel(
        x=panel_graphic.width,
        y=panel_title.bounding_coords().y2,
        width=panel_title.width,
        height=135,
        tag="panel__legend",
    )
)
panel_description = content.add(
    Panel(
        x=panel_graphic.width,
        y=panel_legend.bounding_coords().y2,
        width=panel_title.width,
        height=120,
        tag="panel__description",
    )
)
panel_notes = content.add(
    Panel(
        x=panel_graphic.width,
        y=panel_description.bounding_coords().y2,
        width=panel_title.width,
        height=content.inset_height - panel_description.bounding_coords().y2,
        tag="panel__notes",
    )
)

# Create a group to hold the actual diagram components.
graphic = panel_graphic.add(Group(318, 200))

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
        content={"x": 102, "y": 55, "content": data.annotation_usb},
        x=110,
        y=0,
        scale=(1, -1),
        body={"width": 125},
    )
)

graphic.add(
    AnnotationLabel(
        x=87,
        y=85,
        scale=(1, -1),
        content={"x": 102, "y": 196, "content": data.annotation_led},
        body={"y": 168, "width": 125},
        target={"x": -20, "y": -20, "width": 40, "height": 40, "corner_radius": 20},
    )
)

title_block = panel_title.add(
    TextBlock(
        [data.title],
        x=10,
        y=40,
        line_height=18,
        tag="panel title_block",
    )
)

legend = panel_legend.add(
    Legend(
        data.legend,
        x=10,
        y=5,
        max_height=132,
    )
)

description = panel_description.add(
    TextBlock(
        data.desc,
        x=10,
        y=20,
        line_height=18,
        tag="panel text_block",
    )
)

panel_notes.add(
    TextBlock(
        data.notes,
        x=10,
        y=20,
        line_height=18,
        tag="panel text_block",
    )
)
