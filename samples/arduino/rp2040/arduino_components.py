# Customised components for Arduino pinout diagram
from pinout import core
from pinout.components.pinlabel import PinLabelBody


# PinBodyStart and PinBody include an inset shape
INSET = 2


class PlbStart(PinLabelBody):
    def render(self):

        output = core.Group()

        # Label body
        radius = self.height / 2
        path_def = " ".join(
            [
                f"M {radius} 0",
                f"l {self.width - radius} 0",
                f"l 0 {self.height}",
                f"l {-(self.width - radius)} 0",
                f"a {-radius} {-radius} 0 0 1 0 {-self.height}",
                "z",
            ]
        )
        output.add(
            core.Path(
                path_definition=path_def,
                x=self.x,
                y=self.y - (self.height / 2),
                width=self.width,
                height=self.height,
                tag="label__body",
            )
        )

        # SVG does not support stroke alignment.
        # To achive an 'inner stroke' effect another
        # component has been added with the desired inset.

        h = self.height - INSET
        w = self.width - INSET
        radius = h / 2
        path_def = " ".join(
            [
                f"M {radius + INSET/2} {INSET/2}",
                f"l {w - radius} 0",
                f"l 0 {h}",
                f"l {-(w - radius)} 0",
                f"a {-radius} {-radius} 0 0 1 0 {-h}",
                "z",
            ]
        )
        output.add(
            core.Path(
                path_definition=path_def,
                x=self.x,
                y=self.y - (self.height / 2),
                width=self.width,
                height=self.height,
                tag="label__bodyinner",
            )
        )
        return output.render()


class PlbEnd(PinLabelBody):
    def render(self):

        output = core.Group()

        radius = self.height / 2
        path_def = " ".join(
            [
                f"M 0 0",
                f"L {self.width - radius} 0",
                f"a {radius} {radius} 0 0 1 0 {self.height}",
                f"L 0 {self.height}",
                "Z",
            ]
        )
        output.add(
            core.Path(
                path_definition=path_def,
                x=self.x,
                y=self.y - (self.height / 2),
                width=self.width,
                height=self.height,
                tag="label__body",
            )
        )

        return output.render()


class Plb(PinLabelBody):
    # this class differs from the default version as it include an
    # # 'inner rect' for custom styling
    def render(self):

        output = core.Group()

        output.add(
            core.Rect(
                x=self.x,
                y=self.y - (self.height / 2),
                width=self.width,
                height=self.height,
                corner_radius=self.corner_radius,
                tag="block label__body",
            )
        )

        # Add an inner body for 'inner-stroke' styling
        output.add(
            core.Rect(
                x=self.x + INSET / 2,
                y=self.y - (self.height / 2) + INSET / 2,
                width=self.width - INSET,
                height=self.height - INSET,
                corner_radius=self.corner_radius,
                tag="block label__bodyinner",
            )
        )
        return output.render()
