from pinout.diagram import Diagram
from pinout.components import Component
from pinout import elements as elem


def component_coords():
    diagram = Diagram()
    c1 = diagram.add(Component())

    r1 = c1.add(elem.Rect(x=-50, y=-50, width=10, height=10))
    r2 = c1.add(elem.Rect(x=40, y=-50, width=10, height=10))
    r3 = c1.add(elem.Rect(x=-50, y=40, width=10, height=10))
    r4 = c1.add(elem.Rect(x=40, y=40, width=10, height=10))

    return c1.bounding_coords


def test_component_coords():
    assert component_coords() == (-50, -50, 50, 50)
