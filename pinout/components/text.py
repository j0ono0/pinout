import re
from pinout import config_manager, core


class TextBlock(core.Group):
    """Multiline text component."""

    def __init__(self, content, line_height=None, **kwargs):
        # initialise module attrs
        self.merge_config_into_kwargs(kwargs, "textblock")
        self._scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        self._content = None
        self.content = content

        super().__init__(**kwargs)

        # Convert line_height to same units as diagram
        # It is converted to px when Text instances are created.
        px_line_height = self.units_to_px(line_height or self.config["line_height"])
        self.line_height = self.px_to_units(
            px_line_height, config_manager.get("diagram.units")
        )

    @property
    def lines(self):
        return len(self._content)

    @property
    def height(self):
        return self.line_height * self.lines

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        # Convert string to list
        if isinstance(content, str):
            content = [line.strip() for line in content.split("\n") if line]
        self._content = content

    def render(self):
        for i, text in enumerate(self.content):
            y = self.line_height * i * self._scale.y
            self.add(
                core.Text(content=text, x=0, y=y, scale=self._scale, **self.config)
            )

        return super().render()
