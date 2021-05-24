from pinout.core import Diagram, Group, Image
from pinout.components import Rect, LabelSet, TextBlock
import data


# Create a new digram
diagram = Diagram(1200, 675, tag="arduino-rp2040-connect")

# Add a stylesheet and some custom patterns
diagram.add_stylesheet("styles.css", False)
diagram.add_defs("patterns.xml")

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
group_notes.add(TextBlock(data.para_2, 17, x=380, y=74))


# Add a hardware image
# Note its coordinates are relative to the group it is within
pinout_graphic.add(
    Image(
        "hardware.png",
        x=-176 / 2,
        y=0,
        width=176,
        height=449,
    )
)

# Common label configuration arguments can be documented together
label_one = {"r": 13, "width": 74, "height": 26}
label_config = {
    "r": 13,
    "style": "smooth_bend",
    "width": 74,
    "height": 26,
    "offset": (6, 0),
}

pinout_graphic.add(
    LabelSet(
        x=86,
        y=58,
        pitch=(0, 24.6),
        # scale=(-1, 1),
        rows=data.header_rhs,
    )
)

pinout_graphic.add(
    LabelSet(
        x=-86,
        y=58,
        pitch=(0, 24.6),
        scale=(-1, 1),
        rows=data.header_lhs,
    )
)
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
