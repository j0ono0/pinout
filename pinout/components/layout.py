import re
from pinout import config as conf_mod
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

    def __init__(self, width, height, tag=None, units="px", dpi=96, **kwargs):
        self.dpi = dpi
        self.units = units
        self._width = None
        self._height = None
        self.width = width
        self.height = height
        super().__init__(tag=tag, **kwargs)

        self.add(SvgShape(width=width, height=height))

        # merge kwarg and default configs
        kwarg_cfg = kwargs.get("config", {})
        default_cfg = config_manager.get("diagram")
        self.config = self.update_data_dict(default_cfg, kwarg_cfg)

        # Add tag to component
        self.add_tag(self.config["tag"])

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = self.units_to_px(val)

    @property
    def height(self):
        return self._height

    @property
    def width_in_units(self):
        conversion = {
            "px": self.width,
            "in": self.width / self.dpi,
            "cm": self.width * 2.54 / self.dpi,
            "mm": self.width * 25.4 / self.dpi,
        }
        return conversion[self.units]

    @property
    def height_in_units(self):
        conversion = {
            "px": self.height,
            "in": self.height / self.dpi,
            "cm": self.height * 2.54 / self.dpi,
            "mm": self.height * 25.4 / self.dpi,
        }
        return conversion[self.units]

    @height.setter
    def height(self, val):
        self._height = self.units_to_px(val)

    def units_to_px(self, measurement):
        length = measurement
        units = self.units
        if isinstance(measurement, str):
            tokens = [token for token in re.split(r"(\d+)", measurement, 1) if token]
            length = float(tokens[0])
            units = tokens[1]
            if units not in ["px", "in", "mm", "cm"]:
                raise ValueError(
                    f"units \"{units}\" is not supported. Valid units of measure are 'px', 'in', 'mm' and 'cm'."
                )
        conversion = {
            "px": length,
            "in": length * self.dpi,
            "cm": length / 2.54 * self.dpi,
            "mm": length / 25.4 * self.dpi,
        }
        return conversion[units]

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

        kwargs["config"] = kwargs.get("config", conf_mod.panel)

        super().__init__(**kwargs)

        inset = inset or self.config["inset"]
        self.inset = BoundingCoords(*inset)
        self.add_tag(conf_mod.panel["tag"])

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
                tag=conf_mod.panel["inner"]["tag"],
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
                tag=conf_mod.panel["outer"]["tag"],
            ),
        )

        tplt = templates.get("group.svg")
        return tplt.render(group=self)


class Diagram_2Columns(Diagram):
    def __init__(self, width, height, gutter, tag, **kwargs):
        super().__init__(width, height, tag, **kwargs)
        self.gutter = gutter

        # Add/override config
        self.config = conf_mod.diagram_presets
        self.update_config(kwargs.get("config", {}))

        self.panel_00 = self.add(
            Panel(
                x=0,
                y=0,
                width=width,
                height=height,
                tag=self.config["panel_00"]["tag"],
                config=self.config["panel_00"],
            )
        )
        self.panel_01 = self.panel_00.add(
            Panel(
                x=0,
                y=0,
                width=self.gutter,
                height=self.panel_00.inset_height,
                tag=self.config["panel_01"]["tag"],
                config=self.config["panel_01"],
            )
        )
        self.panel_02 = self.panel_00.add(
            Panel(
                x=self.gutter,
                y=0,
                width=self.panel_00.inset_width - self.gutter,
                height=self.panel_00.inset_height,
                tag=self.config["panel_02"]["tag"],
                config=self.config["panel_02"],
            )
        )


class Diagram_2Rows(Diagram):
    def __init__(self, width, height, gutter, tag, **kwargs):
        super().__init__(width, height, tag, **kwargs)
        self.gutter = self.units_to_px(gutter)

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
