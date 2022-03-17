from pinout import core
from pinout.components import layout
from pinout.core import Group
from pinout.components import integrated_circuits as ic
from pinout.components.annotation import AnnotationLabel
from pinout.components.text import TextBlock
from pinout.components import pinlabel, legend
from pinout import config_manager

# Testing millimetre as units

#################################################

# From the command line:
# ----------------------

# Export diagram as SVG:
# >>> py -m pinout.manager -e diagram_mm_units.py diagram_mm_units.svg -o


config_manager.add_file("mm_config.py")

lowercase_text = """
    The quick brown 
    fox jumps over 
    the lazy dog.
"""
uppercase_text = """
    THE QUICK BROWN FOX 
    JUMPS OVER THE LAZY DOG.
"""
uppercase_alphanum = """
    ABCDEFGHIJKLMN
    OPQRSTUVWXYZ
    1234567890
"""

diagram = layout.Diagram(
    254,
    254,
    units="mm",
    dpi=96,
    tag="millimetre-dimensions",
)


diagram.add_stylesheet("mm_styles.css", embed=False)
diagram.add_stylesheet("mm_dimensions.css", embed=False)

# Diagram background
diagram.add(core.Rect(0, 0, 254, 254, tag="bg_rect"))


#################################################

diagram.add(core.Rect(0, 0, 63.5, 63.5, tag="top_left_cnr"))
diagram.add(TextBlock(lowercase_text, x=1.75, y=1.75, tag="white"))
shapes = diagram.add(Group(1.75, 43.5 - 1.75))
shapes.add(core.Rect(0, 0, 20, 20, tag="rect_1"))
shapes.add(core.Circle(30, 10, 10, tag="circle_1"))
shapes.add(core.Path(path_definition="M 40 0 L 60 20 L 40 20", tag="path_1"))

#################################################

diagram.add(
    core.Image("50mmx50mm.svg", x=63.5, y=0, width=63.5, height=63.5, embed=False)
)

#################################################

grid_grp = diagram.add(Group(x=127, y=0))

# IMPORTANT: dpi of a source image must be included to calculate coords correctly
grid_img = grid_grp.add(
    core.Image(
        "grid_160x80_mm.png",
        embed=True,
        dpi=300,
        x=0,
        y=0,
        width=127,
        height=63.5,
    )
)
grid_img.add_coord("pinlabel_origin", 32, 16)
grid_img.add_coord("pinlabel_body", 48, 16)
grid_img.add_coord("annotation_origin", 16, 16)
grid_img.add_coord("annotation_body", 16 * 4, 16 * 2)

grid_grp.add(core.Circle(*grid_img.coord("pinlabel_origin"), 3, tag="stroke"))

#################################################

diagram.add(
    TextBlock(
        uppercase_alphanum, line_height="35pt", x=1.75, y=63.5 + 1.75, tag="alphanum"
    )
)
grp_pttn = diagram.add(Group(0, 63.5, tag="pttn", clip=core.Rect(0, 0, 127, 63.5)))
for i in range(11):
    for j in range(6):
        x = i * 63.5 / 5
        y = j * 63.5 / 5
        grp_pttn.add(core.Circle(x, y, 5, tag="pttn__dot"))


#################################################

x, y = grid_img.coord("pinlabel_origin")
lbl_x, lbl_y = grid_img.coord("pinlabel_body", raw=True)
grid_grp.add(
    pinlabel.PinLabel(
        "PIN01",
        x,
        y,
        body={"x": lbl_x, "y": lbl_y},
        leaderline={"direction": "vh"},
        tag="gpio",
    )
)

x, y = grid_img.coord("annotation_origin")
lbl_x, lbl_y = grid_img.coord("annotation_body", raw=True)
grid_grp.add(
    AnnotationLabel(
        uppercase_text, x=x, y=y, body={"x": lbl_x, "y": lbl_y, "width": 60}
    )
)

#################################################
# Legend

panel1 = diagram.add(layout.Panel(63.5, 63.5, x=127, y=63.5, inset=(16, 16, 16, 16)))

panel1.add(
    legend.Legend(
        [("One", "one"), ("Two", "two"), ("Pin 1", "pin01")],
        max_height=30,
    )
)

#################################################
# Pinlabel Group

pinlabels_grp = diagram.add(Group(0, 127))
pinlabels_grp.add(
    pinlabel.PinLabelGroup(
        5,
        5,
        (10, 0),
        (50, 50),
        (0, -10),
        [
            [("PWR", "pwr")],
            [("GPIO1", "gpio"), ("PWM", "pwm"), ("Tx", "txrx")],
            [("GPIO2", "gpio"), ("ADC", "adc"), ("Rx", "txrx")],
            [("GND", "gnd")],
        ],
        leaderline={"direction": "vh"},
    )
)

#################################################
# Integrated circuits

ic_grp = diagram.add(Group(10, 190.5))

ic_grp.add(ic.DIP(8, 30, 32, y=4))
ic_grp.add(ic.QFP(16, 40, x=40))
