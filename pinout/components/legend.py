from pinout import core


class Swatch(core.Rect):

    width = 20
    height = 20
    r = 0

    def __init__(self, **kwargs):
        kwargs["tag"] = ("swatch__body " + kwargs.pop("tag", "")).strip()
        kwargs["r"] = kwargs.get("r", Swatch.r)
        kwargs["width"] = kwargs.get("width", Swatch.width)
        kwargs["height"] = kwargs.get("height", Swatch.height)
        super().__init__(**kwargs)


class LegendEntry(core.Group):
    def __init__(
        self, content, swatch=None, width=160, height=30, inset=(3, 3, 3, 3), **kwargs
    ):
        kwargs["tag"] = ("legend-entry " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)

        inset = core.BoundingCoords(*inset)

        # Entry background
        self.add(
            core.Rect(r=0, x=0, y=0, width=width, height=height, tag="legend-entry__bg")
        )

        if swatch is not None:
            swatch_inset = (height - swatch.height) / 2
            swatch.x += inset.x1
            swatch.y += swatch_inset
            self.add(swatch)
        else:
            swatch_size = height - (inset.y1 + inset.y2)
            swatch = self.add(
                core.Rect(
                    r=0,
                    x=inset.x1,
                    y=inset.y1,
                    width=swatch_size,
                    height=swatch_size,
                    tag="swatch__body",
                )
            )

        self.add(
            core.Text(
                content,
                x=swatch.width + inset.x1 + swatch.height / 2,
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

        for entry_class, entry_kwargs in entries:
            swatch_class, swatch_kwargs = entry_kwargs.pop("swatch", (Swatch, {}))
            entry_kwargs["swatch"] = swatch_class(**swatch_kwargs)
            entry_kwargs["x"] = entry_kwargs.get("x", x)
            entry_kwargs["y"] = entry_kwargs.get("y", y)

            entry = self.add(entry_class(**entry_kwargs))

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