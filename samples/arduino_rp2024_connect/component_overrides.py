# Customised components for Arduino pinout diagram
# NOTE: there is probably a better way to integrate this!
from pinout import core


class Label(core.Group):
    def __init__(
        self,
        content,
        x=0,
        y=0,
        width=60,
        height=24,
        tag="",
        style="curve",
        label_style=None,
        r=0,
        offset=(0, 0),
        **kwargs,
    ):
        self.offset = core.Coords(*offset)

        taglist = tag.split(" ")
        taglist.append("label")
        tag = " ".join(taglist)
        super().__init__(x=x, y=y, tag=tag, **kwargs)

        scale = kwargs.pop("scale", core.Coords(1, 1))
        # kwargs["scale"] = (1, 1)

        rx = height / 2

        if self.offset.x != 0 or self.offset.y != 0:
            if style == "straight":
                # Straight line
                path_def = f"M 0 0 l {self.offset.x} {self.offset.y}"
            elif style == "angle_bend":
                # Single bend
                path_def = f"M 0 0 l 0 {self.offset.y} l {self.offset.x} 0"
            elif style == "smooth_bend":
                # Single bend
                rx = min(*self.offset)
                # TODO: determine 'r' in a non-arbitary way
                rx = rx / 3
                path_def = f"M 0 0 L 0 {self.offset.y - rx} A {rx} {rx} 0 0 0 {rx} {self.offset.y} L {self.offset.x} {self.offset.y}"
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
                    **kwargs,
                )
            )
        # Label body
        if label_style == "start":
            path_def = " ".join(
                [
                    f"M {rx} 0",
                    f"L {width} 0",
                    f"L {width} {height}",
                    f"L {rx} {height}",
                    f"A {rx} {rx} 0 0 1 {rx} 0",
                    "Z",
                ]
            )

            clip = self.add(
                core.ClipPath(
                    path_definition=path_def,
                    x=0,
                    y=0,
                    width=width,
                    height=height,
                    **kwargs,
                )
            )

            label_body = self.add(
                core.Path(
                    path_definition=path_def,
                    x=self.offset.x,
                    y=self.offset.y - (height / 2),
                    width=width,
                    height=height,
                    tag="label__body",
                    clip_id=clip.uuid,
                    **kwargs,
                )
            )

        elif label_style == "end":
            path_def = " ".join(
                [
                    f"M 0 0",
                    f"L {width - rx} 0",
                    f"a {rx} {rx} 0 0 1 0 {height}",
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
                    **kwargs,
                )
            )
        else:
            label_body = self.add(
                core.Rect(
                    r=r,
                    x=self.offset.x,
                    y=self.offset.y - (height / 2),
                    width=width,
                    height=height,
                    tag="block label__body",
                    **kwargs,
                )
            )

        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(
            core.Text(content, x=x, y=y, tag="label__text", scale=self.scale, **kwargs)
        )
