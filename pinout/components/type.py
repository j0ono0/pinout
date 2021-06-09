from pinout import core
from pinout import config


class TextBlock(core.Group):
    def __init__(
        self, content, line_height=None, width=None, height=None, offset=None, **kwargs
    ):
        # initialise module attrs
        self._scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        self.content = content
        super().__init__(**kwargs)
        self.update_config(config.textblock)
        offset = offset or self.config["offset"]
        self.offset = core.Coords(*offset)
        self.line_height = line_height or self.config["line_height"]
        self.add_tag(self.config["tag"])

        # Insert a background if width and height exist
        width = width or self.config["width"]
        height = height or self.config["height"]
        bg_tag = f"{self.config['tag']}__bg"
        if width and height:
            self.add(core.Rect(0, 0, width, height, tag=bg_tag))

    def render(self):
        self.add_tag("textblock")
        x = self.offset.x
        y = self.offset.y

        for text in self.content:
            self.add(
                core.Text(content=text, x=x, y=y, scale=self._scale, **self.config)
            )
            y += self.line_height * self._scale.y

        return super().render()