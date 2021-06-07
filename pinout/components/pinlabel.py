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
        tag=None,
        x=0,
        y=0,
        offset=config.pinlabel_offset,
        body=None,
        leaderline=None,
        **kwargs,
    ):
        super().__init__(x, y, tag=tag, **kwargs)
        self.content = content
        self.offset = core.Coords(*offset)

        self.body = body or PinLabelBody(*offset, **config.pinlabel_body)
        self.leaderline = leaderline or lline.Curved("hh")

        self.add(self.leaderline)
        self.add(self.body)

    def render(self):
        # Update final body position
        self.body.x = self.offset.x
        self.body.y = self.offset.y
        # Add text content
        x = self.body.width / 2 + self.offset.x
        y = self.offset.y
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

        # Setup generator for row locations
        pin_coords = config.pitch_generator((0, 0), pin_pitch)
        label_coords = config.pitch_generator(label_start, label_pitch)

        for row in labels:
            row_group = self.add(core.Group(tag="label__row"))
            for label in row:
                try:
                    # Label follows another label in the row
                    prev_label = row_group.children[-1]
                    x = prev_label.x + prev_label.width * scale.x
                    y = prev_label.y + prev_label.offset.y * scale.y
                    _leaderline = lline.Straight(direction="hh")
                    offset = config.pinlabel_offset

                except IndexError:
                    # Start of a new row
                    x, y = next(pin_coords)
                    offset = next(label_coords)
                    _leaderline = copy.deepcopy(leaderline)

                # If data supplied convert to Label
                if type(label) is tuple:
                    content, tag, *args = label
                    attrs = args[0] if len(args) > 0 else {}
                    # Update label attributes
                    attrs["offset"] = attrs.get("offset", offset)
                    attrs["scale"] = attrs.get("scale", scale)
                    attrs["body"] = attrs.get("body", body)
                    attrs["leaderline"] = attrs.get("leaderline", _leaderline)

                    label = Label(content, tag, **attrs)

                # Align label within row
                label.x = x
                label.y = y

                row_group.add(label)


#######################
# Module config

body = PinLabelBody(x=0, y=0, width=80, height=26)
leaderline = lline.Curved(direction="hh")