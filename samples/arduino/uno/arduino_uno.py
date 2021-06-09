from pinout.core import Diagram, Group, Image, Raw, Rect
from pinout.components import pinlabel, legend, leaderline
from pinout.components.type import TextBlock


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
diagram.add(Rect(x=0, y=0, width=1200, height=675, tag="diagram__bg"))
group_main = diagram.add(Group(2, 2, tag="panel panel--main"))
group_main.add(Rect(x=0, y=0, width=1196, height=548, tag="panel__bg"))

# Keeping elements in a group allows for easier measuring and moving
# Create a group for the main pinout graphic
pinout_graphic = group_main.add(Group(600, 10, tag="pinout-graphic"))

group_notes = diagram.add(Group(2, 552, tag="panel panel--notes"))
group_notes.add(Rect(x=0, y=0, width=1196, height=121, tag="panel__bg"))
group_notes.add(
    legend.Legend(data.legend, max_height=112, x=10, y=5, inset=(0, 0, 0, 0))
)
group_notes.add(TextBlock(data.title_1, 22, x=580, y=30))
group_notes.add(TextBlock(data.para_1, 17, x=580, y=74))
group_notes.add(TextBlock(data.para_2, 17, x=900, y=74))

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
    pinlabel.PinLabelGroup(
        x=147,
        y=153,
        pin_pitch=(0, 15.35),
        label_start=(90, -80),
        label_pitch=(0, 8),
        labels=data.header_rhs_a,
    )
)
pinout_graphic.add(
    pinlabel.PinLabelGroup(
        x=147,
        y=316,
        pin_pitch=(0, 15.35),
        label_start=(90, 8),
        label_pitch=(0, 8),
        labels=data.header_rhs_b,
    )
)

# Left hand side pin header
pinout_graphic.add(
    pinlabel.PinLabelGroup(
        x=-147,
        y=208,
        pin_pitch=(0, 15.35),
        label_start=(90, -64),
        label_pitch=(0, 8),
        scale=(-1, 1),
        labels=data.header_lhs_a,
    )
)
pinout_graphic.add(
    pinlabel.PinLabelGroup(
        x=-147,
        y=347,
        pin_pitch=(0, 15.35),
        label_start=(90, 8),
        label_pitch=(0, 8),
        scale=(-1, 1),
        labels=data.header_lhs_b,
    )
)


# LEDs RX & TX
pinout_graphic.add(
    pinlabel.PinLabelGroup(
        x=46,
        y=206,
        pin_pitch=(17, 0),
        label_start=(279, 120),
        label_pitch=(17, 23),
        scale=(-1, -1),
        labels=data.leds_a,
        leaderline=leaderline.Curved(direction="vh"),
    )
)

# LEDs pwr
pinout_graphic.add(
    pinlabel.PinLabelGroup(
        x=62,
        y=392,
        pin_pitch=(39, -185),
        label_start=(38, 90),
        label_pitch=(39, 208),
        scale=(-1, 1),
        labels=data.leds_b,
        leaderline=leaderline.Curved(direction="vh"),
    )
)

diagram.export("pinout_arduino_uno_rev3.svg", True)
