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
        if isinstance(self._line_height, str):
            # Convert line_height to TextBlock unit system
            # It is eventually converted to px in the template using the textblock unit system
            # re splits at start and end of matched group hence x3 vars
            _, val, units = re.split(r"(^[\d\.]+)", self._line_height)
            px_val = self.units_to_px(float(val), units)
        return self.px_to_units(px_val, self.units)

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
            print(f"y:{y}, line_height: {self.line_height}, i:{i}")
            self.add(
                core.Text(content=text, x=0, y=y, scale=self._scale, **self.config)
            )

        return super().render()
