import os
from pathlib import Path
from collections import namedtuple
from .templates import svg
from . import style_tools
from . import file_manager
from .components import (
    Component,
    StyleSheet,
    Label,
)


class Diagram(Component):
    """Components are collated and the final diagram is exported with this class. A typical diagram will include an image, pins with labels, and a stylesheet."""

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
            default_css = style_tools.default_css(self)
            cssname = path.name[: -len(path.suffix)]
            csspath = Path(path.parent, "{}.css".format(cssname))
            # File name may change if overwrite is False
            actual_csspath = file_manager.export_file(default_css, csspath, overwrite)

            self.children.insert(0, StyleSheet(actual_csspath.name))

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
