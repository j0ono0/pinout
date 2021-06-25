from pinout import core, config
from pinout.components.layout import Group


class TextBlock(Group):
    def __init__(self, content, line_height=None, width=None, height=None, **kwargs):
        # initialise module attrs
        self._scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        self.content = content
        super().__init__(**kwargs)
        self.update_config(config.textblock)
        self.line_height = line_height or self.config["line_height"]
        self.add_tag(self.config["tag"])

        # Insert an SvgShape so component reports dimensions
        width = width or self.config["width"]
        height = height or self.config["height"]
        if width and height:
            self.add(core.SvgShape(0, 0, width, height))

    def render(self):
        self.add_tag(self.config["tag"])
        y = 0
        for text in self.content:
            self.add(
                core.Text(content=text, x=0, y=y, scale=self._scale, **self.config)
            )
            y += self.line_height * self._scale.y

        return super().render()