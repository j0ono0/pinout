# User defined components

from pinout.components.pinlabel import PinLabelBody
from pinout import core


class LabelIn(PinLabelBody):
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