import pytest
from pinout.diagram import Diagram
from pinout.components import Component
from pinout import elements as elem


@pytest.mark.parametrize(
    "component, element, answer",
    [
        [
            Component(x=20, y=10, scale=(1, 1)),
            elem.Rect(x=20, y=10, width=10, height=10),
            (40, 20, 50, 30),
        ],
        [
            Component(x=20, y=10, scale=(-1, -1)),
            elem.Rect(x=20, y=10, width=10, height=10),
            (-50, -30, -40, -20),
        ],
        [
            Component(x=20, y=10, scale=(1, 1)),
            elem.Rect(x=-30, y=-20, width=10, height=10),
            (-10, -10, 0, 0),
        ],
        [
            Component(x=20, y=10, scale=(-1, -1)),
            elem.Rect(x=-30, y=-20, width=10, height=10),
            (0, 0, 10, 10),
        ],
        # scaled element (Rect should not alter bounding_coords)
        [
            Component(x=20, y=10, scale=(1, 1)),
            elem.Rect(x=20, y=10, width=10, height=10, scale=(-1, -1)),
            (40, 20, 50, 30),
        ],
    ],
)
def test_component_and_rect_element(component, element, answer):
    diagram = Diagram()
    c01 = diagram.add(component)
    r01 = c01.add(element)

    assert diagram.bounding_coords == answer
