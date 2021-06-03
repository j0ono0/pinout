from pinout import core


class Swatch(core.Group):

    width = 20
    height = 20
    r = 0

    def __init__(self, width=None, height=None, r=None, **kwargs):
        r = r or Swatch.r
        width = width or Swatch.width
        height = height or Swatch.height
        super().__init__(**kwargs)

        # Rect aligned left hand edge, vertically centered around origin.
        shape = self.add(core.Rect(r=r, y=-height / 2, width=width, height=height))
        self.add_tag("swatch")
        shape.add_tag("swatch__body")


class LegendEntry(core.Group):
    def __init__(self, content, tag=None, width=160, height=30, swatch=None, **kwargs):
        swatch = swatch or Swatch()
        kwargs["tag"] = tag
        super().__init__(**kwargs)
        self.add_tag("legend-entry")

        self.add(
            core.Rect(
                r=0,
                width=width,
                height=height,
                tag="legend-entry__bg",
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
                tag="legend-entry__text",
            )
        )


class Legend(core.Group):
    def __init__(self, entries, max_height=104, inset=(4, 4, 4, 4), **kwargs):
        super().__init__(**kwargs)
        inset = core.BoundingCoords(*inset)
        self.add_tag("legend")

        x = 0
        y = 0

        for entry in entries:
            # Convert tuple or dict into default LegendEntry
            if type(entry) is tuple:
                entry = LegendEntry(*entry)
            elif type(entry) is dict:
                entry = LegendEntry(**entry)
            entry.x = x
            entry.y = y

            self.add(entry)

            y += entry.height
            if y >= max_height:
                x = self.width
                y = 0

        # Add a background Rect and offset origin
        self.x += inset.x1
        self.y += inset.y1
        self.children.insert(
            0,
            core.Rect(
                r=0,
                x=-inset.x1,
                y=-inset.y1,
                width=self.width + inset.x1 + inset.x2,
                height=self.height + inset.y1 + inset.y2,
                tag="legend__bg",
            ),
        )
