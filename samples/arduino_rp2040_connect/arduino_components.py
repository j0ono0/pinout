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
        bx = height / 2
        path_def = " ".join(
            [
                f"M {bx} 0",
                f"L {width} 0",
                f"L {width} {height}",
                f"L {bx} {height}",
                f"A {bx} {bx} 0 0 1 {bx} 0",
                "Z",
            ]
        )
        # Clip-path is used to display stroke as an inner-stroke.
        # This ensures labels align correctly regardless of stroke existance or width
        # Consequently the CSS stroke-width should be double intended width
        clip = self.add_defs(
            core.ClipPath(
                path_definition=path_def,
                # x=self.offset.x,
                # y=self.offset.y - (height / 2),
                # width=width,
                # height=height,
            )
        )

        # Add the label body shape
        label_body = self.add(
            core.Path(
                path_definition=path_def,
                x=self.offset.x,
                y=self.offset.y - (height / 2),
                width=width,
                height=height,
                tag="label__body",
                clip_id=clip.uuid,
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
        clip = self.add(core.ClipPath(path_definition=path_def))
        label_body = self.add(
            core.Path(
                path_definition=path_def,
                x=self.offset.x,
                y=self.offset.y - (height / 2),
                width=width,
                height=height,
                tag="label__body",
                clip_id=clip.uuid,
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
        # core.Rect has a clip-path added automatically, no requirement to include one here.
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

        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(core.Text(content, x=x, y=y, tag="label__text", scale=self.scale))
