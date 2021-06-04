import warnings
from pinout import core
from pinout.components import leaderline as lline


class Base(core.Group):
    def __init__(self, **kwargs):
        self.offset = core.Coords(*kwargs.pop("offset", (1, 1)))
        kwargs["tag"] = ("label " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)


class Label(Base):
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
        offset=(18, 0),
        clip=False,
        leaderline=None,
        **kwargs,
    ):
        self.content = content
        scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        super().__init__(x=x, y=y, tag=tag, scale=scale, offset=offset, **kwargs)

        if self.offset.x < 0:
            msg = f"""
                {self}:
                Negative value in Label.offset.x has unexpected results!
                Use Label.scale=(-1, 1) to 'flip' a label horizontally instead.
                """
            warnings.warn(msg)

        ##########################
        # Clipping mask
        clip_id = None
        if clip:
            clip_path = self.add_def(core.ClipPath())
            clip_id = clip_path.uuid
            clip_path.add(
                core.Rect(
                    r=r,
                    x=self.offset.x,
                    y=self.offset.y - (height / 2),
                    width=width,
                    height=height,
                    tag="label__body-clip",
                    **kwargs,
                )
            )

        ##########################
        # Label body
        self.label_body = self.add(
            core.Rect(
                r=r,
                x=self.offset.x,
                y=self.offset.y - (height / 2),
                width=width,
                height=height,
                tag="label__body",
                clip_id=clip_id,
                **kwargs,
            )
        )

        ##########################
        # Leaderline
        leaderline = leaderline or lline.Curved(direction="hh")
        leaderline.route(core.Rect(r=0, x=0, y=0, width=0, height=0), self.label_body)

        self.add(leaderline)

    def render(self):
        # Apply text just before render as scale may change

        x = self.label_body.width / 2 + self.offset.x
        y = self.offset.y
        self.add(core.Text(self.content, x=x, y=y, tag="label__text", scale=self.scale))

        return super().render()


class Row(core.Group):
    def __init__(self, labels, **kwargs):
        kwargs["tag"] = ("labelrow " + kwargs.pop("tag", "")).strip()
        scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        super().__init__(**kwargs)

        for label in labels:
            if type(label) is tuple:
                label = Label(*label)
            elif type(label) is dict:
                label = Label(**label)

            # pass scale to label instance
            label.scale = scale

            # Align each label to the end of the previous label.
            label.x = self.width * scale.x
            try:
                prev_label = self.children[-1]
                label.y = prev_label.y + prev_label.offset.y * scale.y
            except IndexError:
                # No children yet
                label.y = 0
            self.add(label)

            # self.add(cls(content, x=x, y=y, tag=tag, scale=scale, **config))

    def add(self, label):
        if issubclass(type(label), Base):
            self.children.append(label)
            return label
        # Only allow Labels to be added to a label Row
        raise TypeError(label)


class Header(core.Group):
    def __init__(self, pitch, rows, **kwargs):
        scale = kwargs.pop("scale", (1, 1))
        super().__init__(**kwargs)
        pitch = core.Coords(*pitch)
        for ind, row in enumerate(rows):
            row_x = pitch.x * ind
            row_y = pitch.y * ind
            self.add(Row(labels=row, x=row_x, y=row_y, scale=scale))


class PinLabelGroup(core.Group):
    def __init__(self, labels, **kwargs):
        scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        super().__init__(**kwargs)
        for row in labels:
            row_group = self.add(core.Group(tag="label__row"))
            for label in row:

                # If data supplied convert to Label
                if type(label) is tuple:
                    label = Label(*label)
                elif type(label) is dict:
                    label = Label(**label)

                # Align labels in row
                try:
                    prev_label = row_group.children[-1]
                    label.y = prev_label.y + prev_label.offset.y * label.scale.y
                    label.x = prev_label.x + prev_label.width * label.scale.x
                except IndexError:
                    # No children yet
                    pass
                row_group.add(label)
