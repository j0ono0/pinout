import copy
import os
from collections import namedtuple
from pathlib import Path
from . import file_manager
from .elements import Image
from .components import Component, Legend, PinLabelSet, Annotation
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

    def add_image(self, path, *args, embed=False, **kwargs):
        """Associate a PNG, JPG or SVG formatted image to the diagram."""
        self.add(Image, path, *args, embed=embed, **kwargs)

    def add_legend(self, *args, categories=None, **kwargs):
        """Add a pinlabel legend to the diagram."""
        config = copy.deepcopy(self.conf["legend"])
        kwargs["config"] = self.patch_config(config, kwargs.get("legend", {}))
        self.add(Legend, categories, *args, **kwargs)

    def add_pinlabelset(self, *args, **kwargs):
        """Add a pinlabels to a 'header' of pins in the diagram."""
        config = copy.deepcopy(self.conf["pinlabel"])
        kwargs["config"] = self.patch_config(config, kwargs.get("config", {}))
        self.add(PinLabelSet, *args, **kwargs)

    def add_annotation(self, *args, **kwargs):
        """Add an annotation to the diagram."""
        config = copy.deepcopy(self.conf["annotation"])
        kwargs["config"] = self.patch_config(config, kwargs.get("config", {}))
        self.add(Annotation, *args, **kwargs)

    def export(self, path, overwrite=False):
        """Output the diagram in SVG format.

        :param path: File location and name
        :type path: string
        :param overwrite: Overwrite existing file of same path, defaults to False
        :type overwrite: bool, optional
        """
        # Create export location and unique filename if required
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not overwrite:
            path = file_manager.unique_filepath(path)
        path.touch(exist_ok=True)

        output = ""

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
