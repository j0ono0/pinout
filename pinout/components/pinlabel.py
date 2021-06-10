import warnings
import copy
from pinout import core
from pinout.components import leaderline as lline
from pinout import config


class PinLabelBody(core.SvgShape):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x=x, y=y, width=width, height=height, **kwargs)

    def bounding_coords(self):
        # PinLabelBody origin is vertically centered
        return core.BoundingCoords(
            self.x,
            self.y - (self.height / 2),
            self.x + self.width,
            self.y + (self.height / 2),
        )

    def render(self):
        body = core.Rect(
            x=self.x,
            y=self.y - (self.height / 2),
            width=self.width,
            height=self.height,
        )
        body.add_tag("label__body")
        return body.render()


class Label(core.Group):
    def __init__(
        self,
        content="",
        x=0,
        y=0,
        tag=None,
        body=None,
        leaderline=None,
        **kwargs,
    ):
        self.content = content
        super().__init__(x, y, tag=tag, **kwargs)
        self.update_config(config.pinlabel)

        leaderline = leaderline or self.config["leaderline"]
        if isinstance(leaderline, dict):
            leaderline_config = self.config["leaderline"]
            leaderline_config.update(leaderline)
            leaderline = lline.Curved(**leaderline_config)

        body = body or self.config["body"]
        if isinstance(body, dict):
            body_config = self.config["body"]
            body_config.update(body)
            body = PinLabelBody(**body_config)

        self.leaderline = leaderline
        self.body = body

    def bounding_coords(self):
        return core.BoundingCoords(
            self.x,
            self.y,
            self.x + self.body.bounding_coords().x2,
            self.y + self.body.bounding_coords().y2,
        )

    def render(self):

        self.add(self.leaderline)
        self.add(self.body)

        # Add text content
        x = self.body.width / 2 + self.body.x
        y = self.body.y
        self.add(core.Text(self.content, x=x, y=y, tag="label__text", scale=self.scale))
        # Route leaderline
        self.leaderline.route(core.Rect(), self.body)

        self.add_tag("label")

        return super().render()


class PinLabelGroup(core.Group):
    def __init__(
        self,
        x,
        y,
        pin_pitch,
        label_start,
        label_pitch,
        labels,
        leaderline=None,
        body=None,
        **kwargs,
    ):
        scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        super().__init__(x=x, y=y, **kwargs)

        # Setup generators for row locations
        pin_coords = config.pitch_generator((0, 0), pin_pitch)
        label_coords = config.pitch_generator(label_start, label_pitch)

        for row in labels:
            row_group = self.add(core.Group(tag="label__row"))
            for label in row:

                # If data is supplied convert to Label
                if type(label) is tuple:
                    content, tag, *args = label
                    attrs = args[0] if len(args) > 0 else {}

                    # Set leaderline and body in attrs if supplied in either:
                    # 1. data
                    # 2. PinlabelGroup
                    attrs["leaderline"] = attrs.get("leaderline", leaderline)
                    attrs["body"] = attrs.get("body", body)

                    label = Label(
                        content=content,
                        scale=scale,
                        **attrs,
                    )

                    label.add_tag(tag)

                # -- label now exists -- #

                # Label follows another label in the row
                try:
                    prev_label = row_group.children[-1]
                    label.x = prev_label.x + prev_label.width * scale.x
                    label.y = prev_label.y + prev_label.body.y * scale.y
                    label.leaderline = lline.Straight(direction="hh")

                # Start of a new row
                except IndexError:
                    label.x, label.y = next(pin_coords)
                    label.body.x, label.body.y = next(label_coords)

                row_group.add(label)
