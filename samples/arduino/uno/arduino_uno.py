from pinout.core import Diagram, Group, Image, Raw
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
diagram.add(Rect(0, 0, 1200, 675, tag="diagram__bg"))
group_main = diagram.add(Group(2, 2, tag="panel panel--main"))
group_main.add(Rect(0, 0, 1196, 548, tag="panel__bg"))

# Keeping elements in a group allows for easier measuring and moving
# Create a group for the main pinout graphic
pinout_graphic = group_main.add(Group(600, 10, tag="pinout-graphic"))

group_notes = diagram.add(Group(2, 552, tag="panel panel--notes"))
group_notes.add(Rect(0, 0, 1196, 121, tag="panel__bg"))
group_notes.add(TextBlock(data.title_1, 22, x=50, y=30))
group_notes.add(TextBlock(data.para_1, 17, x=50, y=74))
group_notes.add(TextBlock(data.para_2, 17, x=800, y=74))

# Add a hardware image
# Note its coordinates are relative to the group it is within
pinout_graphic.add(
    Image(
        "hardware.png",
        x=-326 / 2,
        y=0,
        width=326,
        height=455,
        embed=True,
    )
)
# Right hand side pin headers
pinout_graphic.add(
    LabelSet(x=147, y=153, pitch=(0, 15.35), scale=(1, 1), rows=data.header_rhs_a)
)
pinout_graphic.add(
    LabelSet(x=147, y=316, pitch=(0, 15.35), scale=(1, 1), rows=data.header_rhs_b)
)

# Left hand side pin header
pinout_graphic.add(
    LabelSet(x=-147, y=208, pitch=(0, 15.35), scale=(-1, 1), rows=data.header_lhs_a)
)
pinout_graphic.add(
    LabelSet(x=-147, y=347, pitch=(0, 15.35), scale=(-1, 1), rows=data.header_lhs_b)
)

# LEDs RX & TX
pinout_graphic.add(
    LabelSet(x=46, y=206, pitch=(17, 0), scale=(-1, -1), rows=data.leds_a)
)

# LEDs pwr
pinout_graphic.add(
    LabelSet(x=62, y=392, pitch=(39, -185), scale=(-1, 1), rows=data.leds_b)
)

diagram.export("pinout_arduino_nano_rp2040_connect.svg", True)
