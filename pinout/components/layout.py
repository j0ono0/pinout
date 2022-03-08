import re
from pinout import templates, config_manager
from pinout.core import (
    Dimensions,
    Layout,
    StyleSheet,
    SvgShape,
    Rect,
    BoundingCoords,
)


class Diagram(Layout):
    """Basis of a pinout diagram"""

    def __init__(self, width, height, **kwargs):
        self._width = None
        self._height = None
        self.width = width
        self.height = height
        self.merge_config_into_kwargs(kwargs, "diagram")

        super().__init__(**kwargs)

        # Setup component
        self.add(SvgShape(width=width, height=height))

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val

    def add_stylesheet(self, path, embed=False):
        """Add a stylesheet to the diagram"""
        self.children.insert(0, StyleSheet(path, embed))

    def render(self):
        """Render children into an <svg> tag."""

        # Warn user if no styles have been added
        stylesheets = self.find_children_by_type(self, StyleSheet)
        if not stylesheets:
            print(
                """
        *********************
        No stylesheet is attached, the diagram may not appear as expected! 
        Generate one automatically with:
        >>> py -m pinout.manager --css <your_script_name> styles.css

        More info at:
        https://pinout.readthedocs.io/en/latest/pages/manager.html#generate-a-cascading-stylesheet
        *********************
                """
            )

        tplt = templates.get("svg.svg")
        return tplt.render(svg=self)


class Panel(Layout):
    def __init__(self, width, height, inset=None, **kwargs):
        """Assist with content grouping and positioning"""

        self.width = width
        self.height = height

        self.merge_config_into_kwargs(kwargs, "panel")

        super().__init__(**kwargs)

        inset = inset or self.config["inset"]
        self.inset = BoundingCoords(*inset)

        # add a non-rendering shape so component
        # reports user set coordinates and dimensions
        self.add(
            SvgShape(
                x=-self.inset.x1,
                y=-self.inset.y1,
                width=width,
                height=height,
            )
        )

        # Offset component to align children with inner dimensions
        self.x += self.inset.x1
        self.y += self.inset.y1

    @property
    def inset_width(self):
        return self.width - (self.inset.x1 + self.inset.x2)

    @property
    def inset_height(self):
        return self.height - (self.inset.y1 + self.inset.y2)

    def render(self):
        """Panel renders children into a <group> tag."""

        self.children.insert(
            0,
            Rect(
                width=self.width - (self.inset.x1 + self.inset.x2),
                height=self.height - (self.inset.y1 + self.inset.y2),
                tag=self.config["inner"]["tag"],
            ),
        )
        # Insert a rect filling the outer component dimensions
        self.children.insert(
            0,
            Rect(
                x=-self.inset.x1,
                y=-self.inset.y1,
                width=self.width,
                height=self.height,
                tag=self.config["outer"]["tag"],
            ),
        )

        tplt = templates.get("group.svg")
        return tplt.render(group=self)


class Diagram_2Columns(Diagram):
    def __init__(self, width, height, gutter, tag, **kwargs):
        super().__init__(width, height, tag, **kwargs)
        self.gutter = gutter

        # Get preset panel config
        panel_cfg = config_manager.get("diagram_presets")

        self.panel_00 = self.add(
            Panel(
                x=0,
                y=0,
                width=self.width,
                height=self.height,
                tag=panel_cfg["panel_00"]["tag"],
                config=panel_cfg["panel_00"],
            )
        )
        self.panel_01 = self.panel_00.add(
            Panel(
                x=0,
                y=0,
                width=self.gutter,
                height=self.panel_00.inset_height,
                tag=panel_cfg["panel_01"]["tag"],
                config=panel_cfg["panel_01"],
            )
        )
        self.panel_02 = self.panel_00.add(
            Panel(
                x=self.gutter,
                y=0,
                width=self.panel_00.inset_width - self.gutter,
                height=self.panel_00.inset_height,
                tag=panel_cfg["panel_02"]["tag"],
                config=panel_cfg["panel_02"],
            )
        )


class Diagram_2Rows(Diagram):
    def __init__(self, width, height, gutter, tag, **kwargs):
        super().__init__(width, height, tag, **kwargs)
        self.gutter = gutter

        # Get preset panel config
        panel_cfg = config_manager.get("diagram_presets")

        self.panel_00 = self.add(
            Panel(
                x=0,
                y=0,
                width=self.width,
                height=self.height,
                tag=panel_cfg["panel_00"]["tag"],
                config=panel_cfg["panel_00"],
            )
        )
        self.panel_01 = self.panel_00.add(
            Panel(
                x=0,
                y=0,
                width=self.panel_00.inset_width,
                height=self.gutter,
                tag=panel_cfg["panel_01"]["tag"],
                config=panel_cfg["panel_01"],
            )
        )
        self.panel_02 = self.panel_00.add(
            Panel(
                x=0,
                y=self.gutter,
                width=self.panel_00.inset_width,
                height=self.panel_00.inset_height - self.gutter,
                tag=panel_cfg["panel_02"]["tag"],
                config=panel_cfg["panel_02"],
            )
        )
