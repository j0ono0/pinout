import copy
import types
from pathlib import Path
from . import file_manager
from . import elements as elem
from .components import Component, Legend, PinLabelSet, Annotation, BoundingCoords
from .templates import svg


class Diagram(Component):
    """The base class that makes up a *pinout* diagram."""

    def __init__(self, *args, **kwargs):

        # Load default config
        Component.config = file_manager.load_config()
        self.config = copy.deepcopy(Component.config["diagram"])

        # Patch config with user suppled config.
        config = kwargs.get("config", {})
        self.patch_config(self.config, config)

        kwargs["config"] = self.config

        super().__init__(*args, **kwargs)

    def add_config(self, path=None):
        """Add a configuration file to the diagram."""
        self.patch_config(Component.config, file_manager.load_config(path))

    def add_panel(self, padding=None, *args, **kwargs):
        """ Add a panel component to the diagram. Returns Panel instance."""
        config = copy.deepcopy(Component.config["panel"])
        kwargs["config"] = self.patch_config(config, kwargs.get("config", {}))
        return self.add(Panel(padding, *args, **kwargs))

    def add_image(self, path, *args, embed=False, **kwargs):
        """Associate a PNG, JPG or SVG formatted image to the diagram."""
        self.add(elem.Image(path, *args, embed=embed, **kwargs))

    def add_legend(self, *args, categories=None, **kwargs):
        """Add a pinlabel legend to the diagram."""
        config = copy.deepcopy(Component.config["legend"])
        kwargs["config"] = self.patch_config(config, kwargs.get("config", {}))
        self.add(Legend(categories, *args, **kwargs))

    def add_pinlabelset(self, *args, **kwargs):
        """Add a pinlabels to a 'header' of pins in the diagram."""
        config = copy.deepcopy(Component.config["pinlabel"])
        kwargs["config"] = self.patch_config(config, kwargs.get("config", {}))
        self.add(PinLabelSet(*args, **kwargs))

    def add_annotation(self, text_content, *args, **kwargs):
        """Add an annotation to the diagram."""
        config = copy.deepcopy(Component.config["annotation"])
        kwargs["config"] = self.patch_config(config, kwargs.get("config", {}))
        self.add(Annotation(text_content, *args, **kwargs))

    def render(self):

        output = ""
        for child in self.children:
            output += child.render()

        return svg.render(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            viewbox=self.bounding_rect,
            content=output,
            **self.config,
        )

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

        # Render final SVG file
        path.write_text(self.render())
        print(f"'{path}' exported successfully.")
