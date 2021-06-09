from pinout import core, config


class Swatch(core.Group):
    def __init__(self, width=None, height=None, **kwargs):
        super().__init__(**kwargs)
        self.update_config(config.legend["entry"]["swatch"])
        width = width or self.config["width"]
        height = height or self.config["height"]

        # Rect aligned left hand edge, vertically centered around origin.
        shape = self.add(core.Rect(y=-height / 2, width=width, height=height))
        self.add_tag("swatch")
        shape.add_tag("swatch__body")


class LegendEntry(core.Group):
    def __init__(
        self,
        content,
        width=None,
        height=None,
        swatch=None,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.update_config(config.legend["entry"])
        self.add_tag(self.config["tag"])

        width = width or self.config["width"]
        height = height or self.config["height"]
        swatch = swatch or {}

        if isinstance(swatch, dict):
            swatch = Swatch(**swatch)

        self.add(
            core.Rect(
                width=width,
                height=height,
                tag=f"{self.config['tag']}__bg",
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
                tag=f"{self.config['tag']}__text",
            )
        )


class Legend(core.Group):
    def __init__(
        self,
        data,
        max_height=None,
        inset=None,
        **kwargs,
    ):

        super().__init__(**kwargs)
        self.update_config(config.legend)
        self.add_tag(self.config["tag"])

        inset = inset or self.config["inset"]
        inset = core.BoundingCoords(*inset)
        max_height = max_height or self.config["max_height"]

        x = inset.x1
        y = inset.y1

        for entry in data:

            if type(entry) is tuple:
                content, tag, *args = entry
                attrs = args[0] if len(args) > 0 else {}
                entry = LegendEntry(content, tag=tag, **attrs, scale=self.scale)

            self.add(entry)

            # Position entry in legend
            if max_height and y + entry.height + inset.y2 > max_height:
                x = self.width
                y = inset.y1
            entry.x = x
            entry.y = y
            y += entry.height

        # Add a background Rect and offset origin
        self.children.insert(
            0,
            core.Rect(
                width=self.width + inset.x1 + inset.x2,
                height=self.height + inset.y1 + inset.y2,
                tag="legend__bg",
            ),
        )
