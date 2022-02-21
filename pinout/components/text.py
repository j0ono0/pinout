from pinout import core


class TextBlock(core.Group):
    """Multiline text component."""

    def __init__(self, content, line_height=None, **kwargs):
        # initialise module attrs
        self._scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        self._content = None

        self.merge_config_into_kwargs(kwargs, "textblock")

        super().__init__(**kwargs)

        self.line_height = line_height or self.config["line_height"]
        self.content = content

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
        y = 0
        for text in self.content:
            self.add(
                core.Text(content=text, x=0, y=y, scale=self._scale, **self.config)
            )
            y += self.line_height * self._scale.y

        return super().render()
