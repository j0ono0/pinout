from pinout import core


class Swatch(core.Group):
    def __init__(self, width=22, height=22, **kwargs):
        kwargs["tag"] = ("swatch " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)
        self.add(
            core.Rect(
                r=height / 2, x=0, y=0, width=width, height=height, tag="swatch__body"
            )
        )


class LegendEntry(core.Group):
    def __init__(
        self, content, swatch=None, width=None, height=None, inset=None, **kwargs
    ):
        kwargs["tag"] = ("legend-entry " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)
        # Entry background
        self.add(
            core.Rect(r=0, x=0, y=0, width=width, height=height, tag="legend-entry__bg")
        )

        if swatch is not None:
            swatch_inset = (height - swatch.height) / 2
            swatch.x += swatch_inset
            swatch.y += swatch_inset
            self.add(swatch)
        else:
            swatch_size = height - inset * 2
            swatch = self.add(
                core.Rect(
                    r=0,
                    x=inset,
                    y=inset,
                    width=swatch_size,
                    height=swatch_size,
                    tag="swatch__body",
                )
            )

        self.add(
            core.Text(
                content,
                x=swatch.width + swatch.height / 2,
                y=self.height / 2,
                tag="legend-entry__text",
            )
        )


class Legend(core.Group):
    def __init__(self, entries, max_height=104, inset=(4, 4, 4, 4), **kwargs):
        kwargs["tag"] = ("legend " + kwargs.pop("tag", "")).strip()
        self.inset = core.BoundingCoords(*inset)
        super().__init__(**kwargs)
        x = 0
        y = 0
        for text, tag, *args in entries:
            try:
                kwargs = args[0]
            except IndexError:
                kwargs = {}

            # TODO: Locate default args in a config file/class...?
            entry = self.add(
                LegendEntry(
                    text,
                    tag=tag,
                    width=kwargs.pop("width", 160),
                    height=kwargs.pop("height", 26),
                    inset=kwargs.pop("inset", 3),
                    swatch=kwargs.pop("swatch", None),
                    x=x,
                    y=y,
                )
            )
            y += entry.height
            if y >= max_height:
                x = self.width
                y = 0

    def render(self):
        # Add a background Rect
        self.children.insert(
            0,
            core.Rect(
                r=0,
                x=-self.inset.x1,
                y=-self.inset.y1,
                width=self.width + self.inset.x1 + self.inset.x2,
                height=self.height + self.inset.y1 + self.inset.y2,
                tag="legend__bg",
            ),
        )
        self.x += self.inset.x1
        self.y += self.inset.y1

        return super().render()