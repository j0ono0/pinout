from pinout.core import Diagram, Group, Image, Raw
from pinout import components as cmp
from pinout.components import Rect, LabelSet, TextBlock


# Import data from another script
import data

# Create a new digram
diagram = Diagram(1200, 675, tag="arduino-rp2040-connect")


# Add a stylesheet and some custom patterns
diagram.add_stylesheet("styles.css", True)

# Load some svg markup to be used as patterns
# The Raw class allows arbitary code to be inserted
# into the diagram.
with open("patterns.xml") as f:
    patterns = f.read()
diagram.add_def(Raw(patterns))

# Construct a layout and add some backgrounds
group_main = diagram.add(Group(0, 0, tag="panel panel--main"))
group_main.add(Rect(0, 0, 1200, 555, tag="panel__bg"))

# Keeping elements in a group allows for easier measuring and moving
# Create a group for the main pinout graphic
pinout_graphic = group_main.add(Group(600, 80, tag="pinout-graphic"))

group_notes = diagram.add(Group(0, 550, tag="panel panel--notes"))
group_notes.add(Rect(0, 0, 1200, 120, tag="panel__bg"))
group_notes.add(TextBlock(data.title_1, 22, x=50, y=30))
group_notes.add(TextBlock(data.para_1, 17, x=50, y=74))
group_notes.add(TextBlock(data.para_2, 17, x=800, y=74))


# Add a hardware image
# Note its coordinates are relative to the group it is within
pinout_graphic.add(
    Image(
        "hardware.png",
        x=-176 / 2,
        y=0,
        width=176,
        height=449,
        embed=True,
    )
)
# Right hand side pin header
pinout_graphic.add(
    LabelSet(x=86, y=58, pitch=(0, 24.6), scale=(1, 1), rows=data.header_rhs)
)


# Left hand side pin header
pinout_graphic.add(
    LabelSet(
        x=-86,
        y=58,
        pitch=(0, 24.6),
        scale=(-1, 1),
        rows=data.header_lhs,
    )
)

# LED labels
pinout_graphic.add(
    LabelSet(
        x=-56,
        y=28,
        pitch=(112, 0),
        scale=(1, -1),
        rows=data.leds,
    )
)

diagram.export("pinout_arduino_nano_rp2040_connect.svg", True)
