###########################################
#
# Example script to build a pinout diagram
# Includes examples of all features
#
###########################################

from pinout.core import Diagram, Group, Rect, Image
from pinout.components import pinlabel
from pinout.components import leaderline as lline

import data

# Create a new diagram and add a background
diagram = Diagram(1200, 675, "diagram")
diagram.add(Rect(0, 0, 1200, 675, "diagram__bg"))


# Add a stylesheet
diagram.add_stylesheet("styles.css", True)


# Create some panels to group content together
# and add backgrounds to them
panel_meta = diagram.add(Group(2, 2, "panel--meta"))
panel_meta.add(Rect(0, 0, 1196, 71, "bg"))

panel_main = diagram.add(Group(2, 75, "panel--main"))
panel_main.add(Rect(0, 0, 1196, 598, "bg"))


# Create a group to hold the pinout-diagram components.
graphic = panel_main.add(Group(510, 80))


# Add and embed an image
graphic.add(Image("hardware.png", width=220, height=300, embed=True))


# Add a pinlabels to the right header
graphic.add(
    pinlabel.PinLabelGroup(
        x=204,
        y=106,
        pin_pitch=(0, 30),
        label_start=(60, -12),
        label_pitch=(0, 8),
        labels=data.rhs,
    )
)

# Add a pinlabels to the left header
graphic.add(
    pinlabel.PinLabelGroup(
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
    pinlabel.PinLabelGroup(
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
    pinlabel.PinLabelGroup(
        x=155,
        y=284,
        pin_pitch=(-30, 0),
        label_start=(109, 60),
        label_pitch=(30, 30),
        labels=data.btm_rhs,
        leaderline=lline.Curved(direction="vh"),
    )
)

"""
# Add pinlabels
pinlabel_config = cmpt.Component.config["pinlabel"]
for data in pindata:
    panel_main.add(cmpt.PinLabelSet(**data, config=pinlabel_config))

# Add an annotation sample
panel_main.add(
    cmpt.Annotation(
        "USB-C connector  \nHost/Device functionality",
        x=110,
        y=20,
        config=cmpt.Component.config["annotation"],
    )
)

# Add pinlabel legend panel
panel_legend = diagram.add(cmpt.Panel(x=500, y=0, tag="legend__pinlabels"))

panel_legend.add(
    cmpt.Legend(
        x=-234,
        y=380,
        categories=["analog", "comms", "gpio", "led", "pwm", "pwr"],
        config=cmpt.Component.config["legend"],
    )
)

# Calculate left over space
x = panel_legend.x
y = panel_legend.height + 20  # INVESTIGATE: padding not in dimensions???
w = panel_legend.width + 20
h = panel_main.height - panel_legend.height + 30  ### NOTSURE  WHY THIS IS OUT?

panel_text = diagram.add(
    cmpt.Panel(x=x, y=y, width=w, height=h, tag="experimental_text")
)
panel_text.add(
    elem.TextBlock(
        text_content="*pinout* is a Python application \nthat creates SVG diagrams. Development is active \nand ongoing to convert a promising idea \ninto a useful tool to assist \nwith documentation of electronic hardware.",
        x=0,
        y=0,
        width=w,
        height=h,
        config=cmpt.Component.config["label"],
    )
)
"""
# Export final SVG diagram
diagram.export("pinout_diagram.svg", True)