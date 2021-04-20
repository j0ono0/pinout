import os
from collections import namedtuple
from pathlib import Path

from . import file_manager, style_tools
from .components import Component, StyleSheet, Image, Legend, PinLabelSet
from .templates import svg


class Diagram(Component):
    """The base class that makes up every *pinout* diagram."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = file_manager.load_config()

    def add_stylesheet(self, path, embed=False):
        """Associate a stylesheet to the diagram. Multiple stylesheets can be added. If none are added one is automatically generated.

        :param path: Path to the stylesheet file. *Note*: Where :code:`embed=False` the path is relative to the exported file. Where :code:`embed=True` the path is relative to the current working directory.
        :type path: string
        :param embed: Embed or link the stylesheet in the exported file, defaults to False
        :type embed: bool, optional
        """
        self.add_and_instantiate(StyleSheet, path, embed=embed)

    def add_image(self, path, *args, embed=False, **kwargs):
        """Associate a PNG, JPG or SVG formatted image to the diagram. *IMPORTANT*: Image width and height parameters must be supplied for the image to display! *pinout* does not auto-detect these attributes.

        :param path: Path to the image file. *Note*: Where :code:`embed=False` the path is relative to the exported file. Where :code:`embed=True` the path is relative to the current working directory.
        :type path: string
        :param embed: Embed or link the image in the exported file, defaults to False
        :type embed: bool, optional
        """
        self.add_and_instantiate(Image, path, *args, embed=embed, **kwargs)

    def add_legend(self, *args, **kwargs):
        """Add a legend to the diagram. Content for the legend is provided via a config file::

            # config.yaml

            legend:
                categories: [
                    # [<Title>, <CSS class 'tag'>]
                    ["Analog", "analog"],
                    ["GPIO", "gpio"],
                    ["PWM", "pwm"],
                ]

        See 'add_config' for related information.
        """
        self.add_and_instantiate(Legend, *args, **kwargs)

    def add_pinlabelset(self, *args, **kwargs):
        """Add a PinLabelSet to the diagram. This is the recommended method of adding pin labels to a diagram. See :class:`components.PinLabelSet` for more details."""
        self.add_and_instantiate(PinLabelSet, *args, **kwargs)

    def patch_config(self, cfg, patch):
        """Recursively update configuration dictionary. Accessing this method directly may not be necessary. Use *add_config* in conjunction with a YAML configuration file to modify the default settings.

        :param patch: path to YAML config file
        :type patch: dict
        """
        for key, val in patch.items():
            if type(val) == dict:
                self.patch_config(cfg[key], patch[key])
            else:
                cfg[key] = val

    def add_config(self, path):
        """Add configuration settings to the diagram. Parameters set in this fashion override the existing 'defaults' and referenced by components when parameters are not explicitly assigned.

        A complete set of *pinout* defaults can be duplicated from the command line for reference::

            >>> py -m pinout.file_manager --duplicate config

        :param path: Path to YAML formatted configuration file
        :type path: str
        """
        self.patch_config(self.cfg, file_manager.load_config(path))

    def generate_stylesheet(self, path, overwrite):
        """Generate a stylesheet based on config settings and randomised (within set limits) values. Directly using this function is probably unnecessary. Diagrams with no associated stylesheet automatically call this function on export.

        :param path: export path for stylesheet file
        :type path: string
        :param overwrite: Allow an existing file of the same name to be overwritten
        :type overwrite: bool
        """
        default_css = style_tools.default_css(self)
        cssname = path.name[: -len(path.suffix)]
        csspath = Path(path.parent, "{}.css".format(cssname))
        # File name may change if overwrite is False
        actual_csspath = file_manager.export_file(default_css, csspath, overwrite)

        self.children.insert(0, StyleSheet(actual_csspath.name))

    def export(self, path, overwrite=False):
        """Output the diagram in SVG format. If no stylesheet(s) are included one will be generated and exported automatically. See style_tools.default_css() for more details.

        :param path: Name of svg file to be created, including export path.
        :type path: str
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
