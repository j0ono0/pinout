import pathlib
import uuid
from pinout import templates, file_manager, config, style_tools
from pinout.core import Layout, StyleSheet, Group, SvgShape, Rect, BoundingCoords
from pinout.components.pinlabel import PinLabel


class Diagram(Layout):
    """Basis of a pinout diagram"""

    def __init__(self, width, height, tag=None, **kwargs):
        super().__init__(tag=tag, **kwargs)
        self.width = width
        self.height = height

    def add_stylesheet(self, path, embed=True):
        """Add a stylesheet to the diagram

        :param path: Path to stylesheet file
        :type path: string
        :param embed: embed stylesheet in exported file, defaults to True
        :type embed: bool, optional
        """
        self.children.insert(0, StyleSheet(path, embed))

    def render(self):
        """Render children into an <svg> tag.

        :return: SVG markup
        :rtype: string
        """
        tplt = templates.get("svg.svg")
        return tplt.render(svg=self)

    def create_stylesheet(self, path):
        """Create a stylesheet if none supplied. Does not overwrite any existing file with the predetermined name."""
        """
        if path.is_file():
            print(
                f"A stylesheet at '{path}' already exists! Aborting auto-generation of CSS file."
            )
        else:
        """
        # Extract css class tags from PinLabels
        lbls = self.find_children_by_type(self, PinLabel)
        tags = list(
            set([tag for label in lbls for tag in label.tag.strip().split(" ")])
        )
        if config.pinlabel["tag"] in tags:
            tags.remove(config.pinlabel["tag"])

        css_tplt = templates.get("stylesheet.css")
        css = css_tplt.render(
            css={
                "pinlabel": config.pinlabel,
                "panel": config.panel,
                "legend": config.legend,
                "tags": style_tools.assign_color(tags),
            }
        )
        # Create stylesheet file and link to it
        with open(path, "w") as f:
            f.write(css)
        self.add(StyleSheet(path, embed=True))

    def export(self, path, overwrite=False):
        """Output the diagram in SVG format."""
        # Create export location and unique filename if required
        path = pathlib.Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not overwrite:
            path = file_manager.unique_filepath(path)
        path.touch(exist_ok=True)

        # Create a stylesheet if none exists
        existing_styles = self.find_children_by_type(self, StyleSheet)
        if len(existing_styles) == 0:
            csspath = pathlib.Path(".".join(str(path).split(".")[:-1]) + ".css")
            self.create_stylesheet(csspath)

        # Render final SVG file
        path.write_text(self.render())
        print(f"'{path}' exported successfully.")


class ClipPath(Group):
    """Define a clip-path component"""

    def __init__(self, x=0, y=0, tag=None, **kwargs):
        self.uuid = str(uuid.uuid4())
        super().__init__(x=x, y=y, tag=tag, **kwargs)

    def render(self):
        """Render children into a <clipPath> tag.

        :return: SVG markup
        :rtype: string
        """
        tplt = templates.get("clippath.svg")
        return tplt.render(path=self)


class Panel(Group):
    def __init__(self, width, height, inset=None, **kwargs):
        inset = inset or config.panel["inset"]
        self.inset = BoundingCoords(*inset)
        super().__init__(**kwargs)
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