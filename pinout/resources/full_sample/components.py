# User defined components

from pinout import core


class LabelIn(core.SvgShape):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x=x, y=y, width=width, height=height, **kwargs)

    def bounding_coords(self):
        # Report origin as vertically centered
        return core.BoundingCoords(
            self.x,
            self.y - (self.height / 2),
            self.x + self.width,
            self.y + (self.height / 2),
        )

    def render(self):
        skew = 3
        body = core.Path(
            path_definition=" ".join(
                [
                    f"M {self.x + skew} {self.y - self.height/2}",
                    f"l {self.width} 0",
                    f"l {-skew*2} {self.height}",
                    f"{-self.width} 0",
                    "z",
                ]
            )
        )
        body.add_tag("label__body")
        return body.render()