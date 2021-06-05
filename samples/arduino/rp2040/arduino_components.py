# Customised components for Arduino pinout diagram
from pinout import core
from pinout.components.pinlabel import Base
from pinout.components import leaderline as lline


class FirstLabel(Base):
    def __init__(self, content, tag, **kwargs):
        # Extract kwargs that are used locally
        height = kwargs.pop("height")
        width = kwargs.pop("width")
        leaderline = kwargs.pop("leaderline", lline.Curved("hh"))
        super().__init__(tag=tag, **kwargs)

        # Label body
        br = height / 2
        path_def = " ".join(
            [
                f"M {br} 0",
                f"l {width - br} 0",
                f"l 0 {height}",
                f"l {-(width - br)} 0",
                f"a {-br} {-br} 0 0 1 0 {-height}",
                "z",
            ]
        )

        # Add the label body
        label_body = self.add(
            core.Path(
                path_definition=path_def,
                x=self.offset.x,
                y=self.offset.y - (height / 2),
                width=width,
                height=height,
                tag="label__body",
            )
        )

        # SVG does not support stroke alignment.
        # To achive an 'inner stroke' effect another
        # component has been added with the desired inset.
        #
        # !NOTE: clip-path has not been used here due to a bug
        # causing the path to display incorrectly in InkScape!

        inset = 2
        h = height - inset
        w = width - inset
        br = h / 2
        path_def = " ".join(
            [
                f"M {br + inset/2} {inset/2}",
                f"l {w - br} 0",
                f"l 0 {h}",
                f"l {-(w - br)} 0",
                f"a {-br} {-br} 0 0 1 0 {-h}",
                "z",
            ]
        )
        self.add(
            core.Path(
                path_definition=path_def,
                x=self.offset.x,
                y=self.offset.y - (height / 2),
                width=width,
                height=height,
                tag="label__bodyinner",
            )
        )

        self.add(leaderline)
        leaderline.route(core.Rect(0), label_body)

        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(core.Text(content, x=x, y=y, tag="label__text", scale=self.scale))


class LabelLast(Base):
    def __init__(self, content, tag, **kwargs):
        height = kwargs.pop("height")
        width = kwargs.pop("width")
        leaderline = kwargs.pop("leaderline", lline.Curved("hh"))
        super().__init__(tag=tag, **kwargs)

        # Label body
        bx = height / 2
        path_def = " ".join(
            [
                f"M 0 0",
                f"L {width - bx} 0",
                f"a {bx} {bx} 0 0 1 0 {height}",
                f"L 0 {height}",
                "Z",
            ]
        )
        label_body = self.add(
            core.Path(
                path_definition=path_def,
                x=self.offset.x,
                y=self.offset.y - (height / 2),
                width=width,
                height=height,
                tag="label__body",
            )
        )

        if self.offset != (0, 0):
            self.add(leaderline)
            leaderline.route(core.Rect(0), label_body)

        # Label text
        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(core.Text(content, x=x, y=y, tag="label__text", scale=self.scale))


class Label(Base):
    def __init__(self, content, tag, **kwargs):
        height = kwargs.pop("height")
        width = kwargs.pop("width")
        leaderline = kwargs.pop("leaderline", lline.Curved("hh"))
        # 'r' is used for the label body radius (leaderline corner curve radius is 'hard coded'.)
        r = kwargs.pop("r", 0)
        super().__init__(tag=tag, **kwargs)

        # Label body
        label_body = self.add(
            core.Rect(
                r=r,
                x=self.offset.x,
                y=self.offset.y - (height / 2),
                width=width,
                height=height,
                tag="block label__body",
            )
        )

        # Add an inner body for 'inner-stroke' styling
        inset = 2
        self.add(
            core.Rect(
                r=r,
                x=self.offset.x + inset / 2,
                y=self.offset.y - (height / 2) + inset / 2,
                width=width - inset,
                height=height - inset,
                tag="block label__bodyinner",
            )
        )

        if self.offset != (0, 0):
            self.add(leaderline)
            leaderline.route(core.Rect(0), label_body)

        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(core.Text(content, x=x, y=y, tag="label__text", scale=self.scale))
