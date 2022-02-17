from pinout import core, config
from pinout.components.layout import Group


class Swatch(Group):
    """Graphical icon for display in LegendEntry"""

    def __init__(self, width=None, height=None, **kwargs):

        self.merge_config_into_kwargs(kwargs, "legend")

        super().__init__(**kwargs)

        width = width or self.config["swatch"]["width"]
        height = height or self.config["swatch"]["height"]

        # Rect aligned left hand edge, vertically centered around origin.
        shape = self.add(core.Rect(y=-height / 2, width=width, height=height))
        self.add_tag("swatch")
        shape.add_tag("swatch__body")


class LegendEntry(Group):
    """Legend entry comprised of a swatch and single line of text."""

    def __init__(
        self,
        content,
        width=None,
        height=None,
        swatch=None,
        **kwargs,
    ):
        self.merge_config_into_kwargs(kwargs, "legend")

        super().__init__(**kwargs)

        self.add_tag(self.config["tag"])

        width = width or self.config["entry"]["width"]
        height = height or self.config["entry"]["height"]
        swatch = swatch or {}

        if isinstance(swatch, dict):
            swatch = Swatch(**swatch)

        self.add(
            core.SvgShape(
                width=width,
                height=height,
            ),
        )

        swatch.y = height / 2
        swatch.x = (height - swatch.height) / 2
        self.add(swatch)

        self.add(
            core.Text(
                content,
                x=swatch.bounding_coords().x2 + swatch.x,
                y=self.height / 2,
            )
        )


class Legend(Group):
    """Auto generate a legend component"""

    def __init__(
        self,
        data,
        max_height=None,
        **kwargs,
    ):
        self.merge_config_into_kwargs(kwargs, "legend")
        super().__init__(**kwargs)
        self.add_tag(self.config["tag"])

        max_height = max_height or self.config["max_height"]

        entry_x = 0
        entry_y = 0
        for entry in data:

            if type(entry) is tuple:
                content, tag, *args = entry
                attrs = args[0] if len(args) > 0 else {}
                entry = LegendEntry(content, tag=tag, **attrs, scale=self.scale)

            self.add(entry)

            # Position entry in legend
            if max_height and entry_y + entry.height > max_height:
                entry_x = self.width
                entry_y = 0
            entry.x = entry_x
            entry.y = entry_y
            entry_y += entry.height
