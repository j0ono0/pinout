import copy
import os
from collections import namedtuple
from pathlib import Path

from . import file_manager, style_tools
from .components import Component, StyleSheet, Image, Legend, PinLabelSet, Annotation
from .templates import svg


class Diagram(Component):
    """The base class that makes up a *pinout* diagram."""

    def __init__(self, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load default config and patch with any supplied patch
        Component.conf = file_manager.load_config()

        # Patch conf with user suppled config.
        config = config or {}
        try:
            self.patch_config(self.conf, config)
        except KeyError:
            pass

    def add_config(self, path=None):
        """Add a configuration file to the diagram."""
        self.patch_config(self.conf, file_manager.load_config(path))

    def add_stylesheet(self, path, embed=False):
        """Associate a stylesheet to the diagram."""
        self.add_and_instantiate(StyleSheet, path, embed=embed)

    def add_image(self, path, *args, embed=False, **kwargs):
        """Associate a PNG, JPG or SVG formatted image to the diagram."""
        self.add_and_instantiate(Image, path, *args, embed=embed, **kwargs)

    def add_legend(self, categories, *args, **kwargs):
        """Add a pinlabel legend to the diagram."""
        config = copy.deepcopy(self.conf["legend"])
        kwargs["config"] = self.patch_config(config, kwargs.get("legend", {}))
        self.add_and_instantiate(Legend, categories, *args, **kwargs)

    def add_pinlabelset(self, *args, **kwargs):
        """Add a pinlabels to a 'header' of pins in the diagram."""
        config = copy.deepcopy(self.conf["pinlabel"])
        kwargs["config"] = self.patch_config(config, kwargs.get("config", {}))
        self.add_and_instantiate(PinLabelSet, *args, **kwargs)

    def add_annotation(self, *args, **kwargs):
        config = copy.deepcopy(self.conf["annotation"])
        kwargs["config"] = self.patch_config(config, kwargs.get("config", {}))
        self.add_and_instantiate(Annotation, *args, **kwargs)

    def generate_stylesheet(self, path, overwrite):
        """Generate a stylesheet based on config settings and randomised (within set limits) values."""
        default_css = style_tools.default_css(self)
        cssname = path.name[: -len(path.suffix)]
        csspath = Path(path.parent, "{}.css".format(cssname))
        # File name may change if overwrite is False
        actual_csspath = file_manager.export_file(default_css, csspath, overwrite)

        self.children.insert(0, StyleSheet(actual_csspath.name))

    def export(self, path, overwrite=False):
        """Output the diagram in SVG format."""
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
                tag=self.tag,
                content=output,
            )
        )
        print(f"'{path}' exported successfully.")
