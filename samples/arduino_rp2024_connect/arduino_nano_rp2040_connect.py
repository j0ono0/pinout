from pinout.core import Diagram, Group, Image
from pinout.components import Rect, LabelSet


# Pin and label locations are predictible and the calculations can be automated
# This generator will help keep class args neat when adding pin-labels
# This helper function may get rolled into the core as some point
def pitch_generator(start, pitch):
    x = start[0]
    y = start[1]
    while True:
        yield (x, y)
        x += pitch[0]
        y += pitch[1]


# Create a new digram
diagram = Diagram(1200, 675, tag="arduino-rp2040-connect")
diagram.add_stylesheet("styles_arduino_nano_rp2040_connect.css")

# Construct a layout and add some backgrounds
group_main = diagram.add(Group(0, 0, tag="panel panel--main"))
group_main.add(Rect(0, 0, 1200, 600, tag="panel__bg"))

# Keeping elements in a group allows for easier measuring and moving
# Create a group for the main pinout graphic
pinout_graphic = group_main.add(Group(600, 80, tag="pinout-graphic"))

group_notes = diagram.add(Group(0, 600, tag="panel panel--notes"))
group_notes.add(Rect(0, 0, 1200, 75, tag="panel__bg"))


# Add a hardware image
# Note its coordinates are relative to the group it is within
pinout_graphic.add(
    Image(
        "hardware_arduino_nano_rp2040_connect.png",
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

# setup some automation for pinrow positioning
pitch = pitch_generator((80, 0), (0, 3))

pinout_graphic.add(
    LabelSet(
        x=86,
        y=58,
        pitch=(0, 24.5),
        # scale=(-1, 1),
        rows=[
            [
                (
                    "GND",
                    "pwr--gnd",
                    {**label_one, "offset": next(pitch)},
                ),
            ],
            [
                (
                    "PWR",
                    "pwr--3v3 ptn__diag--red",
                    {**label_one, "offset": next(pitch)},
                ),
            ],
            [
                (
                    "01",
                    "adc",
                    {**label_one, "offset": next(pitch)},
                ),
                ("02", "dac", label_config),
                ("03", "gpio", label_config),
            ],
            [
                (
                    "04",
                    "dac",
                    {**label_one, "offset": next(pitch)},
                ),
                ("05", "adc", label_config),
                ("06", "gpio", label_config),
            ],
        ],
    )
)

diagram.export("pinout_arduino_nano_rp2040_connect.svg", True)
