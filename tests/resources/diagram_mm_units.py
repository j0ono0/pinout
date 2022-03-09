from pinout import core
from pinout.core import Group
from pinout.components.layout import Diagram
from pinout.components.text import TextBlock
from pinout.components import pinlabel
from pinout import config_manager

# Testing millimetre as units
config_manager.add_file("mm_config.py")

print(config_manager.config_modules)

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


diagram.add_stylesheet("mm_styles.css", embed=False)
diagram.add(core.Rect(0, 0, 127, 254, tag="bg_rect"))
diagram.add(core.Rect(0, 0, 63.5, 63.5, tag="top_left_cnr"))


diagram.add(
    core.Image("50mmx50mm.svg", x=63.5, y=0, width=63.5, height=63.5, embed=False)
)

#################################################

grp_1 = diagram.add(Group(1.75, 43.5 - 1.75))
grp_1.add(core.Rect(0, 0, 20, 20, tag="rect_1"))
grp_1.add(core.Circle(30, 10, 10, tag="circle_1"))
grp_1.add(core.Path(path_definition="M 40 0 L 60 20 L 40 20", tag="path_1"))
diagram.add(TextBlock(lowercase_text, line_height="11pt", x=1.75, y=1.75, tag="white"))

#################################################

diagram.add(
    TextBlock(uppercase_alphanum, line_height="35pt", x=1.75, y=63.5, tag="alphanum")
)
grp_pttn = diagram.add(Group(0, 63.5, tag="pttn", clip=core.Rect(0, 0, 127, 63.5)))
for i in range(11):
    for j in range(6):
        x = i * 63.5 / 5
        y = j * 63.5 / 5
        grp_pttn.add(core.Circle(x, y, 5, tag="pttn__dot"))

#################################################

grp_grid = diagram.add(Group(x=0, y=127))

# IMPORTANT: dpi of a source image must be included to calculate coords correctly
img_grid = grp_grid.add(
    core.Image(
        "grid_200x80_mm.png",
        embed=True,
        dpi=300,
        x=0,
        y=0,
        width=127,
        height=80 / 200 * 127,
    )
)


img_grid.add_coord("ref1", 60, 20)
grp_grid.add(core.Circle(*img_grid.coord("ref1"), 3, tag="stroke"))


#################################################


diagram.add(pinlabel.PinLabel("PIN01", 1.75, 127, tag="pin01"))

# From the command line:
# ----------------------

# Export diagram as SVG:
# >>> py -m pinout.manager -e diagram_mm_units.py diagram_mm_units.svg -o
