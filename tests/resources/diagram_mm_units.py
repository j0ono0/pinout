from pinout import core
from pinout.core import Group, Image
from pinout.components.layout import Diagram
from pinout.components.text import TextBlock

# Testing millimetre as units


diagram = Diagram(
    127,
    127,
    units="mm",
    dpi=96,
    tag="millimetre-dimensions",
)

diagram.add_stylesheet("mm_styles.css", embed=True)
diagram.add(core.Rect(0, 0, 127, 127, tag="bg_rect"))
diagram.add(core.Rect(0, 0, 63.5, 63.5, tag="top_left_cnr"))
diagram.add(core.Text("Testing millimetre units", x=10, y=10))

png = diagram.add(core.Image_PNG("50mmx50mm.png", x=63.5, y=0, width=63.5, height=63.5))


grp_1 = diagram.add(Group(0, 63.5))

grp_1.add(core.Rect(10, 10, 20, 20, tag="rect_1"))
grp_1.add(core.Circle(40, 20, 10, tag="circle_1"))
grp_1.add(core.Path(path_definition="M 50 10 L 70 30 L 50 30", tag="path_1"))

tb = diagram.add(
    TextBlock(
        "THIS IS A TEXTBLOCK\nLINE 0002.\nLine 0003.",
        line_height="12pt",
        x=63.5,
        y=63.5,
    )
)

# From the command line:
# ----------------------

# Export diagram as SVG:
# >>> py -m pinout.manager -e diagram_mm_units.py diagram_mm_units.svg -o
