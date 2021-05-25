from collections import namedtuple
from . import core

LabelAttrs = namedtuple("LabelAttrs", ("content tag config"))
LabelAttrs.__new__.__defaults__ = (None, None, {})


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
        style="curve",
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

        label_body = self.add(
            core.Rect(
                r=r,
                x=self.offset.x,
                y=self.offset.y - (height / 2),
                width=width,
                height=height,
                tag="label__body",
                **kwargs,
            )
        )
        if self.offset.x != 0 or self.offset.y != 0:
            if style == "straight":
                # Straight line
                path_def = f"M 0 0 l {self.offset.x} {self.offset.y}"
            elif style == "angle_bend":
                # Single bend
                path_def = f"M 0 0 l 0 {self.offset.y} l {self.offset.x} 0"
            elif style == "smooth_bend":
                # Single bend
                r = min(*self.offset)
                # TODO: determine 'r' in a non-arbitary way
                r = r / 3
                path_def = f"M 0 0 L 0 {self.offset.y - r} A {r} {r} 0 0 0 {r} {self.offset.y} L {self.offset.x} {self.offset.y}"
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

        x = label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(
            core.Text(content, x=x, y=y, tag="label__text", scale=self.scale, **kwargs)
        )


class LabelRow(core.Group):
    def __init__(self, labels, **kwargs):

        tag = kwargs.pop("tag", "")
        taglist = tag.split(" ")
        taglist.append("labelrow")
        kwargs["tag"] = " ".join(taglist)
        scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        super().__init__(**kwargs)

        for label in labels:
            label = LabelAttrs(*label)

            # Align each label to the end of the previous label.
            x = self.width * scale.x
            y = 0
            try:
                prev_label = self.children[-1]
                y = prev_label.y + prev_label.offset.y * scale.y
            except IndexError:
                pass  # no children yet

            self.add(
                Label(
                    label.content, x=x, y=y, tag=label.tag, scale=scale, **label.config
                )
            )

    def add(self, label):
        if type(label) is Label:
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
            row_x = pitch.x * ind
            row_y = pitch.y * ind
            self.add(LabelRow(labels=row, x=row_x, y=row_y, scale=scale))


class TextBlock(core.Group):
    def __init__(self, content, line_height, **kwargs):
        scale = kwargs.pop("scale", (1, 1))
        tag = kwargs.pop("tag", "")
        taglist = tag.split(" ")
        taglist.insert(0, "textblock")
        kwargs["tag"] = " ".join(taglist)
        super().__init__(**kwargs)
        self.line_height = line_height
        y = 0
        for text in content:
            self.add(core.Text(content=text, y=y, scale=scale))
            y += self.line_height
