# Some custom components
# These are experimental: Trialling what might be useful components
# If they go really well might look into rolling them into the official package.


from pinout import core


class Panel(Group):
    def __init__(self, width, height, inset, **kwargs):
        self.inset = core.BoundingCoords(*inset)
        super().__init__(**kwargs)

        # add a non-rendering shape so component
        # reports user set coordinates and dimensions
        self.add(
            core.SvgShape(
                x=-self.inset.x1,
                y=-self.inset.y1,
                width=width,
                height=height,
            )
        )

        # Add a panel background filling the inset area
        self.children.insert(
            0,
            core.Rect(
                width=width - (self.inset.x1 + self.inset.x2),
                height=height - (self.inset.y1 + self.inset.y2),
                tag="panel__bg",
            ),
        )

        self.x += self.inset.x1
        self.y += self.inset.y1

    # Calculate inner dimensions for easier
    # alignment of other components
    @property
    def inset_width(self):
        return self.width - (self.inset.x1 + self.inset.x2)

    @property
    def inset_height(self):
        return self.height - (self.inset.y1 + self.inset.y2)
