import copy
import os
from pathlib import Path
from . import file_manager
from . import elements as elem
from .components import Component, Legend, PinLabelSet, Annotation
from .templates import svg


class Panel(Component):
    def __init__(self, padding=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if padding is None:
            padding = self.config.get("padding", [0, 0, 0, 0])
        self.padding = elem.Padding(*padding)

    @property
    def bounding_coords(self):
        coords = super().bounding_coords
        # Add padding to dimensions
        return elem.BoundingCoords(
            coords.x_min,
            coords.y_min,
            coords.x_max + self.padding.right + self.padding.left,
            coords.y_max + self.padding.bottom + self.padding.top,
        )

    def render(self):
        rect_config = self.config["rect"]
        rect_config["width"] = self.width
        rect_config["height"] = self.height
        rect = self.children.insert(
            0,
            elem.Rect(
                x=-self.padding.left,
                y=-self.padding.top,
                width=self.width,
                height=self.height,
                config=self.config["rect"],
            ),
        )
        # Offset children to top-left padding coords
        self.x += self.padding.left
        self.y += self.padding.top
        return super().render()

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


class Diagram(Panel):
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

        # Update diagram config
        self.config["rect"]["height"] = self.height
        self.config["rect"]["width"] = self.width

        # Render final SVG file
        path.write_text(
            svg.render(
                x=0,
                y=0,
                width=self.width,
                height=self.height,
                viewbox=self.bounding_rect,
                content=output,
                **self.config,
            )
        )
        print(f"'{path}' exported successfully.")
