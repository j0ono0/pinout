import os
from collections import namedtuple
from pathlib import Path

from . import file_manager, style_tools
from .components import Component, StyleSheet, Image, Legend, PinLabelSet
from .templates import svg


class Diagram(Component):
    """Components are collated and the final diagram is exported with this class. A typical diagram will include an image, pins with labels, and a stylesheet."""

    def add_stylesheet(self, path, embed=False):
        self.add(StyleSheet(path))

    def add_image(self, path, *args, embed=False, **kwargs):
        self.add(Image(path, *args, **kwargs))

    def add_legend(self, *args, **kwargs):
        l = Legend(*args, **kwargs)
        self.add(Legend(*args, **kwargs))

    def add_pinlabelset(self, offset, labels, pitch=(1, 1), *args, **kwargs):
        self.add(PinLabelSet(offset, labels, pitch, *args, **kwargs))

    def generate_stylesheet(self, path, overwrite):
        default_css = style_tools.default_css(self)
        cssname = path.name[: -len(path.suffix)]
        csspath = Path(path.parent, "{}.css".format(cssname))
        # File name may change if overwrite is False
        actual_csspath = file_manager.export_file(default_css, csspath, overwrite)

        self.children.insert(0, StyleSheet(actual_csspath.name))

    def export(self, path, overwrite=False):
        """Output the diagram in SVG format. If no stylesheet(s) are included one will be generated and exported automatically. See style_tools.default_css() for more details.

        :param svgname: Name of svg file to be created, including export path.
        :type svgname: str
        :param overwrite: When set to False, this function aborts if the file already exists avoiding accidental overwriting. Defaults to False.
        :type overwrite: bool, optional
        """

        # Create export location and unique filename if required
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not overwrite:
            path = file_manager.unique_filepath(path)
        path.touch(exist_ok=True)

        output = ""

        # Generate default styles if none supplied
        stylesheets = [s for s in self.children if isinstance(s, StyleSheet)]
        if not stylesheets:
            self.generate_stylesheet(path, overwrite)

        # Render all components
        for c in self.children:
            output += c.render()

        # Render final SVG file
        path.write_text(
            svg.render(
                x=0,
                y=0,
                width=self.width,
                height=self.height,
                viewbox=self.bounding_rect,
                tags=self.tags,
                content=output,
            )
        )
        print(f"'{path}' exported successfully.")
