from pinout import core


class TextBlock(core.Group):
    def __init__(self, content, line_height, **kwargs):
        scale = kwargs.pop("scale", (1, 1))
        kwargs["tag"] = ("textblock " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)
        self.line_height = line_height
        y = 0
        for text in content:
            self.add(core.Text(content=text, y=y, scale=scale))
            y += self.line_height
