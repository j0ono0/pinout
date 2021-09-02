import uuid
from pinout import templates, config
from pinout.core import Layout, StyleSheet, Group, SvgShape, Rect, BoundingCoords


class Diagram(Layout):
    """Basis of a pinout diagram"""

    def __init__(self, width, height, tag=None, **kwargs):
        self.width = width
        self.height = height
        super().__init__(tag=tag, **kwargs)
        self.add(SvgShape(width=width, height=height))

    def add_stylesheet(self, path, embed=True):
        """Add a stylesheet to the diagram"""
        self.children.insert(0, StyleSheet(path, embed))

    def render(self):
        """Render children into an <svg> tag."""
        tplt = templates.get("svg.svg")
        return tplt.render(svg=self)


class ClipPath(Group):
    """Define a clip-path component"""

    def __init__(self, x=0, y=0, tag=None, **kwargs):
        super().__init__(x=x, y=y, tag=tag, **kwargs)

    def render(self):
        """Render children into a <clipPath> tag."""
        tplt = templates.get("clippath.svg")
        return tplt.render(path=self)


class Panel(Group):
    def __init__(self, width, height, inset=None, **kwargs):
        """Assist with content grouping and positioning"""
        kwargs["config"] = kwargs.get("config", config.panel["inset"])
        super().__init__(**kwargs)
        inset = inset or self.config["inset"]
        self.inset = BoundingCoords(*inset)
        self.add_tag(config.panel["tag"])

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

        self.children.insert(
            0,
            Rect(
                width=self.width - (self.inset.x1 + self.inset.x2),
                height=self.height - (self.inset.y1 + self.inset.y2),
                tag=config.panel["inner"]["tag"],
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
                tag=config.panel["outer"]["tag"],
            ),
        )

        return super().render()


class Diagram_2Column(Diagram):
    def __init__(self, width, height, gutter, tag, **kwargs):
        self.gutter = gutter
        kwargs["config"] = kwargs.get("config", config.diagram_presets)
        super().__init__(width, height, tag, **kwargs)

        self.panel_00 = self.add(
            Panel(
                x=0,
                y=0,
                width=width,
                height=height,
                tag="panel panel_content",
            )
        )
        self.panel_01 = self.panel_00.add(
            Panel(
                x=0,
                y=0,
                width=self.gutter,
                height=self.panel_00.inset_height,
                tag="panel panel_01",
            )
        )
        self.panel_02 = self.panel_00.add(
            Panel(
                x=self.gutter,
                y=0,
                width=self.panel_00.inset_width - self.gutter,
                height=self.panel_00.inset_height,
                tag="panel panel_02",
            )
        )


class Diagram_2Row(Diagram):
    def __init__(self, width, height, gutter, tag, **kwargs):
        self.gutter = gutter
        kwargs["config"] = kwargs.get("config", config.diagram_presets)
        super().__init__(width, height, tag, **kwargs)

        self.panel_00 = self.add(
            Panel(
                x=0,
                y=0,
                width=width,
                height=height,
                tag="panel panel_content",
                config=self.config["panel"],
            )
        )
        self.panel_01 = self.panel_00.add(
            Panel(
                x=0,
                y=0,
                width=self.panel_00.inset_width,
                height=self.gutter,
                tag="panel_01",
                config=self.config["panel"],
            )
        )
        self.panel_02 = self.panel_00.add(
            Panel(
                x=0,
                y=self.gutter,
                width=self.panel_00.inset_width,
                height=self.panel_00.inset_height - self.gutter,
                tag="panel_02",
                config=self.config["panel"],
            )
        )
