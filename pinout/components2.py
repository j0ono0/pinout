from . import core


class Rect(core.Path):
    def __init__(self, x=0, y=0, width=10, height=10, tag=None, r=0, **kwargs):
        x1 = 0
        y1 = 0
        x2 = width
        y2 = height

        path_def = " ".join(
            (
                f"M {x1 + r} {y1}",
                f"L {x2 - r} {y1}",
                f"A {r} {r} 0 0 1 {x2} {y1 + r}",
                f"L {x2} {y2 - r}",
                f"A {r} {r} 0 0 1 {x2 - r} {y2}",
                f"L {x1 + r} {y2}",
                f"A {r} {r} 0 0 1 {x1} {y2 - r}",
                f"L {x1} {y1 + r}",
                f"A {r} {r} 0 0 1 {x1 + r} {y1}",
                "z",
            )
        )
        super().__init__(
            path_def, x=x, y=y, width=width, height=height, tag=tag, **kwargs
        )


class Label(core.Group):
    def __init__(
        self,
        content,
        x=0,
        y=0,
        width=60,
        height=24,
        tag="",
        r=0,
        leader_len=0,
        **kwargs,
    ):
        taglist = tag.split(" ")
        taglist.append("label")
        tag = " ".join(taglist)
        super().__init__(x=x, y=y, tag=tag, **kwargs)

        kwargs["scale"] = (1, 1)
        label_body = self.add(
            core.Rect(
                r=r,
                x=leader_len,
                y=-height / 2,
                width=width - leader_len,
                height=height,
                tag="label__body",
                **kwargs,
            )
        )
        if leader_len > 0:
            path_def = f"M 0 0 l {leader_len} 0"
            self.add(
                core.Path(
                    path_definition=path_def,
                    x=0,
                    y=0,
                    width=leader_len,
                    height=0,
                    tag="label__leaderline",
                    **kwargs,
                )
            )

        kwargs["scale"] = self.scale
        x = label_body.width / 2 + leader_len
        self.add(core.Text(content, x=x, tag="label__text", **kwargs))


class LabelRow(core.Group):
    def __init__(self, labels, **kwargs):
        scale = kwargs.pop("scale", (1, 1))
        super().__init__(**kwargs)
        for content, tag, config in labels:
            self.add(Label(content, tag=tag, scale=scale, **config))

    def add(self, label):
        if type(label) is Label:
            label.x = self.width * label.scale.x
            self.children.append(label)
            return label
        # Only allow Labels to be added to a LabelRow
        raise TypeError(label)


class LabelSet(core.Group):
    def __init__(self, pitch, rows, **kwargs):
        scale = kwargs.pop("scale", (1, 1))
        super().__init__(**kwargs)
        pitch = core.Coords(*pitch)
        for ind, row in enumerate(rows):
            row_x = self.x + pitch.x * ind
            row_y = self.y + pitch.y * ind
            self.add(LabelRow(labels=row, x=row_x, y=row_y, scale=scale))
