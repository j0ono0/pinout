from pinout import core


class TextBlock(core.Group):
    def __init__(self, content, line_height, **kwargs):
        scale = kwargs.pop("scale", (1, 1))
        scale = core.Coords(*scale)

        super().__init__(**kwargs)
        self.add_tag("textblock")
        self.line_height = line_height

        height = len(content) * line_height
        y = 0 if scale.y > 0 else height

        for text in content:
            self.add(core.Text(content=text, y=y, scale=scale))
            y += self.line_height * scale.y
