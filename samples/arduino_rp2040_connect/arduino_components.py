# Customised components for Arduino pinout diagram
from pinout import core
from pinout.components import LabelBase


class FirstLabel(LabelBase):
    def __init__(self, content, **kwargs):
        # Extract kwargs that are used locally
        height = kwargs.pop("height")
        width = kwargs.pop("width")
        super().__init__(**kwargs)

        # Leaderline
        # note: beizer curve used to display feature!
        # Simpler straight line path_def could be used
        if self.offset.x != 0 or self.offset.y != 0:
            len = self.offset.x / 5
            ctl_x = self.offset.x / 2
            path_def = f"M 0 0 L {len} 0 C {ctl_x} 0 {ctl_x} {self.offset.y} {self.offset.x - len} {self.offset.y} L {self.offset.x} {self.offset.y}"

            self.add(
                core.Path(
                    path_definition=path_def,
                    width=self.offset.x,
                    height=self.offset.y,
                    tag="label__leaderline",
                )
            )

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

        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(core.Text(content, x=x, y=y, tag="label__text", scale=self.scale))


class LabelLast(LabelBase):
    def __init__(self, content, **kwargs):
        height = kwargs.pop("height")
        width = kwargs.pop("width")
        super().__init__(**kwargs)

        if self.offset != (0, 0):
            # Straight line
            path_def = f"M 0 0 l {self.offset.x} {self.offset.y}"
            self.add(
                core.Path(
                    path_definition=path_def,
                    x=0,
                    y=0,
                    width=self.offset.x,
                    height=self.offset.y,
                    tag="label__leaderline",
                )
            )

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

        # Label text
        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(core.Text(content, x=x, y=y, tag="label__text", scale=self.scale))


class Label(LabelBase):
    def __init__(self, content, **kwargs):
        height = kwargs.pop("height")
        width = kwargs.pop("width")
        style = kwargs.pop("style", "")
        # 'r' is used for the label body radius (leaderline corner curve radius is 'hard coded'.)
        r = kwargs.pop("r", 0)
        super().__init__(**kwargs)

        # Add a leaderline if label is offset from origin
        if self.offset != (0, 0):
            if style == "cnr":
                # Single bend
                llr = min(*self.offset) / 3
                path_def = f"M 0 0 L 0 {self.offset.y - llr} A {llr} {llr} 0 0 0 {llr} {self.offset.y} L {self.offset.x} {self.offset.y}"
            else:
                # Beizer curve (default)
                len = self.offset.x / 5
                ctl_x = self.offset.x / 2
                path_def = f"M 0 0 L {len} 0 C {ctl_x} 0 {ctl_x} {self.offset.y} {self.offset.x - len} {self.offset.y} L {self.offset.x} {self.offset.y}"

            self.add(
                core.Path(
                    path_definition=path_def,
                    x=0,
                    y=0,
                    width=self.offset.x,
                    height=self.offset.y,
                    tag="label__leaderline",
                )
            )

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

        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(core.Text(content, x=x, y=y, tag="label__text", scale=self.scale))
