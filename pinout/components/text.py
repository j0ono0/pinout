import re
from pinout import core


class TextBlock(core.Group):
    """Multiline text component."""

    def __init__(self, content, line_height=None, **kwargs):
        # initialise module attrs
        self.merge_config_into_kwargs(kwargs, "textblock")
        self._scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        self._content = None

        # NOTE: line_height may be a string with typographic specific units (ie pt)
        self.line_height = line_height or self.config["line_height"]

        super().__init__(**kwargs)

        self.content = content

    @property
    def line_height(self):
        """Convert line_height unit system to textblock unit system"""
        return self.units_to_userspace(self._line_height)

    @line_height.setter
    def line_height(self, value):
        self._line_height = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        # Convert string to list
        if isinstance(content, str):
            content = [line.strip() for line in content.split("\n")]
        self._content = content

    def render(self):
        for i, text in enumerate(self.content):
            y = self.line_height * i * self._scale.y
            self.add(
                core.Text(content=text, x=0, y=y, scale=self._scale, **self.config)
            )

        return super().render()
