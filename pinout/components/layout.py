import re
from pinout import templates, config_manager
from pinout.core import (
    Layout,
    StyleSheet,
    SvgShape,
    Rect,
    BoundingCoords,
)


class Diagram(Layout):
    """Basis of a pinout diagram"""

    def __init__(self, width, height, units=None, **kwargs):
        self._width = None
        self._height = None
        self.merge_config_into_kwargs(kwargs, "diagram")
        super().__init__(**kwargs)

        # assign units after kwargs config set
        self.units = units

        # Units need to be set before px dimensions calculated
        self.width = self.units_to_px(width)
        self.height = self.units_to_px(height)

        # Add default config to match units
        if self.units == "mm":
            config_manager.add_config_from_package("resources/config/mm_config.json")

        # Setup component
        # Add a non-rendering shape to ensure diagram content is not scaled up on export
        self.add(SvgShape(width=self.width, height=self.height, units="px"))

    @property
    def units(self):
        return config_manager.get("diagram.units")

    @units.setter
    def units(self, val):
        config_manager.set({"diagram": {"units": val}})

    """
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
    """

    def add_config(self, src):
        if isinstance(src, dict):
            config_manager.set(src)
        else:
            config_manager.add_json(src)

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

        self.merge_config_into_kwargs(kwargs, "panel")
        super().__init__(**kwargs)

        self.width = width
        self.height = height

        inset = inset or self.config["inset"]
        self.inset = BoundingCoords(*inset)

        # Offset component to align children with inner dimensions
        self.x += self.units_to_px(self.inset.x1)
        self.y += self.units_to_px(self.inset.y1)

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
    def __init__(self, width, height, gutter, **kwargs):
        super().__init__(width, height, **kwargs)
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
    def __init__(self, width, height, gutter, **kwargs):
        super().__init__(width, height, **kwargs)
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
