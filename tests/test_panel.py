import pytest
from pinout.diagram import Diagram
from pinout import components as cmpt
from pinout import elements as elem


def test_panel():

    diagram = Diagram()

    panel_main = diagram.add(
        cmpt.Panel(
            x=0,
            y=0,
            width=220,
            height=120,
            config={
                "padding": [50, 10, 10, 50],
                "fill": [255, 100, 100],
                "fill_opacity": 1,
                "stroke": [204, 204, 204],
                "stroke_width": 0,
                "rx": 0,
            },
        )
    )
    panel_main.add(
        elem.Rect(
            x=0,
            y=0,
            width=100,
            height=100,
            config={
                "fill": [100, 255, 100],
                "fill_opacity": 1,
                "stroke": [204, 204, 204],
                "stroke_width": 0,
                "rx": 0,
            },
        )
    )
    panel_main.add(
        elem.Rect(
            x=100,
            y=0,
            width=100,
            height=100,
            config={
                "fill": [200, 55, 0],
                "fill_opacity": 1,
                "stroke": [204, 204, 204],
                "stroke_width": 0,
                "rx": 0,
            },
        )
    )
    panel_rhs = diagram.add(
        cmpt.Panel(
            x=220,
            y=0,
            # width=100,
            height=120,
            config={
                "padding": [10, 10, 10, 10],
                "fill": [255, 100, 255],
                "fill_opacity": 1,
                "stroke": [204, 204, 204],
                "stroke_width": 0,
                "rx": 0,
            },
        )
    )
    panel_rhs.add(
        elem.Rect(
            x=0,
            y=0,
            width=10,
            height=10,
            config={
                "fill": [100, 255, 100],
                "fill_opacity": 1,
                "stroke": [204, 204, 204],
                "stroke_width": 0,
                "rx": 0,
            },
        )
    )

    diagram.export("test_panel_output.svg", overwrite=True)

    # assert diagram.bounding_rect == (0, 0, 50, 50)
    assert diagram.bounding_rect == (0, 0, 320, 120)
