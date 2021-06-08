from pinout import core
from pinout import config


class TextBlock(core.Group):
    def __init__(self, content, line_height=None, **kwargs):
        self._scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        self.content = content

        super().__init__(**kwargs)

        # initialise config with default values
        self.update_config(config.textblock)
        # update config with args
        self.update_config({"line_height": line_height})

    def render(self):
        self.add_tag("textblock")
        y = 0

        for text in self.content:
            self.add(core.Text(content=text, y=y, scale=self._scale, **self.config))
            y += self.config["line_height"] * self._scale.y

        return super().render()