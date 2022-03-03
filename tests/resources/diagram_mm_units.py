from pinout import core
from pinout.core import Group, Image
from pinout.components.layout import Diagram
from pinout.components.text import TextBlock
from pinout.components import pinlabel

# Testing millimetre as units

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

diagram = Diagram(
    127,
    254,
    units="mm",
    dpi=96,
    tag="millimetre-dimensions",
)

diagram.add_stylesheet("mm_styles.css", embed=True)
diagram.add(core.Rect(0, 0, 127, 254, tag="bg_rect"))
diagram.add(core.Rect(0, 0, 63.5, 63.5, tag="top_left_cnr"))

diagram.add(core.ImageBitmap("50mmx50mm.png", x=63.5, y=0, width=63.5, height=63.5))

diagram.add(core.ImageSVG("50mmx50mm.svg", x=0, y=127))

grp_1 = diagram.add(Group(1.75, 43.5 - 1.75))

grp_1.add(core.Rect(0, 0, 20, 20, tag="rect_1"))
grp_1.add(core.Circle(30, 10, 10, tag="circle_1"))
grp_1.add(core.Path(path_definition="M 40 0 L 60 20 L 40 20", tag="path_1"))


diagram.add(TextBlock(lowercase_text, line_height="11pt", x=1.75, y=1.75, tag="white"))
tb = diagram.add(
    TextBlock(uppercase_alphanum, line_height="35pt", x=1.75, y=63.5, tag="alphanum")
)
grp_pttn = diagram.add(Group(0, 63.5, tag="pttn", clip=core.Rect(0, 0, 127, 63.5)))
for i in range(11):
    for j in range(6):
        x = i * 63.5 / 5
        y = j * 63.5 / 5
        grp_pttn.add(core.Circle(x, y, 5, tag="pttn__dot"))


# diagram.add(pinlabel.PinLabel("PIN01", 1.75, 127, tag="pin01"))

# From the command line:
# ----------------------

# Export diagram as SVG:
# >>> py -m pinout.manager -e diagram_mm_units.py diagram_mm_units.svg -o
