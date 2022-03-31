# py -m pinout.manager --export diagram_dimensions.py diagram_dimensions.svg -o

from pinout.components import (
    annotation,
    layout,
    leaderline,
    pinlabel,
    text,
)
from pinout.core import (
    Circle,
    Group,
    Image,
    Path,
    Rect,
    Text,
)

diagram = layout.Diagram(200, 100, units="mm")
diagram.add_stylesheet("diagram_dimensions_styles.css", embed=False)
diagram.add_stylesheet("diagram_dimensions_custom_styles.css", embed=False)

diagram.add(Rect(x=60, y=0, width=40, height=20, tag="blue"))

diagram.add(layout.Panel(20, 20, inset=(5, 5, 5, 5)))

diagram.add(Circle(cx=30, cy=10, r=10, tag="red"))
diagram.add(Path(x=40, path_definition="M 0 0 l 20 0 l 0 20"))
diagram.add(Text("0987654321", x=60, y="12pt", tag="white"))
diagram.add(
    text.TextBlock(
        "The quick brown \nfox jumps over \nthe lazy dog.",
        x=60,
        y="24pt",
        tag="white",
    )
)

img = diagram.add(Image("200x200.png", x=60, y=20, width=40, height=40))
img.add_coord("centre", 100, 100)


pinlabel_group = diagram.add(Group(x=100, tag="grp_pinlabels"))
pinlabel_group.add(
    pinlabel.PinLabel(
        "gpio01",
        x=10,
        y=10,
        tag="gpio",
        body={"x": 10, "y": 5},
    )
)
pinlabel_group.add(
    pinlabel.PinLabel(
        "gpio02",
        x=10,
        y=20,
        tag="gpio",
        leaderline={"direction": "vh"},
        body={"x": 10, "y": 5},
    )
)
pinlabel_group.add(
    pinlabel.PinLabel(
        "gpio04",
        x=10,
        y=30,
        tag="gpio",
        leaderline=leaderline.Straight(),
        body={"x": 10, "y": 5},
    )
)

pinlabel_group.add(
    pinlabel.PinLabel(
        "gpio03",
        x=10,
        y=40,
        tag="gpio",
        leaderline=leaderline.Angled(),
        body={"x": 10, "y": 5},
    )
)

ax, ay = img.coord("centre")
print(ax, ay)
diagram.add(
    annotation.AnnotationLabel(
        content="This is an \nannotation", x=10, y=10, body={"x": 10, "y": 30}
    )
)
