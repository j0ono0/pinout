import copy
from pinout.core import SvgShape, Group, Rect, Text, BoundingCoords, Coords
from pinout.components import leaderline as lline
from pinout import config


def pitch_generator(start, pitch):
    x = start[0]
    y = start[1]
    while True:
        yield (x, y)
        x += pitch[0]
        y += pitch[1]


class Body(SvgShape):
    """Graphical shape that makes up the body of a pinlabel."""

    def __init__(self, x, y, width, height, corner_radius=0, **kwargs):
        self.corner_radius = corner_radius
        super().__init__(x=x, y=y, width=width, height=height, **kwargs)

    def bounding_coords(self):
        # PinLabelBody origin is vertically centered
        return BoundingCoords(
            self.x,
            self.y - (self.height / 2),
            self.x + self.width,
            self.y + (self.height / 2),
        )

    def render(self):
        body = Rect(
            x=self.x,
            y=self.y - (self.height / 2),
            width=self.width,
            height=self.height,
            corner_radius=self.corner_radius,
        )
        body.add_tag(config.pinlabel["body"]["tag"])
        return body.render()


class Leaderline(lline.Curved):
    """Graphical line joining the label origin coordinates to the label body."""

    pass


class Base(Group):
    """Label component designed specifically for labelling pins."""

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
        self._leaderline = None
        self._body = None
        super().__init__(x, y, tag=tag, **kwargs)
        self.update_config(config.pinlabel)

        self.body = body
        self.leaderline = leaderline

        # Add leaderline and body reference into children
        self.add(self._body)

        # Add leaderline at render as it is replaced by pinlabelGroup!!!
        # Add SvgShape so pin label reports correct dimensions.
        self.add(SvgShape(x=self.leaderline.x, y=self.leaderline.x))

        self.add_tag(config.pinlabel["tag"])

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        # ensure instance data is unique
        body = copy.deepcopy(body or self.config["body"])
        # Convert dict into body object
        if isinstance(body, dict):
            body_config = self.config["body"]
            body_config.update(body)
            body = Body(**body_config)
            # Add body config tag if not there
        body.add_tag(self.config["body"]["tag"])
        self._body = body

    @property
    def leaderline(self):
        return self._leaderline

    @leaderline.setter
    def leaderline(self, leaderline):
        # ensure instance data is unique
        leaderline = copy.deepcopy(leaderline or self.config["leaderline"])
        # Convert dict into leaderline object
        if isinstance(leaderline, dict):
            leaderline_config = self.config["leaderline"]
            leaderline_config.update(leaderline)
            leaderline = Leaderline(**leaderline_config)
        # Add leaderline config tag if not there
        leaderline.add_tag(self.config["leaderline"]["tag"])
        self._leaderline = leaderline

    def render(self):
        # Add text content
        x = self.body.width / 2 + self.body.x
        y = self.body.y
        self.add(
            Text(
                self.content,
                x=x,
                y=y,
                tag=config.pinlabel["text"]["tag"],
                scale=self.scale,
            )
        )
        # Route leaderline
        self.leaderline.route(Rect(), self._body)
        self.add(self.leaderline)
        return super().render()


class PinLabel(Base):
    pass


class PinLabelGroup(Group):
    """Convenience class to place multiple rows of pin-labels on a pin-header."""

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
        scale = Coords(*kwargs.pop("scale", (1, 1)))
        super().__init__(x=x, y=y, **kwargs)

        # Setup generators for row locations
        pin_coords = pitch_generator((0, 0), pin_pitch)
        label_coords = pitch_generator(label_start, label_pitch)

        for row in labels:
            row_group = self.add(Group())
            for label in row:

                # If data is supplied convert to Label
                if type(label) is tuple:
                    content, tag, *args = label
                    attrs = args[0] if len(args) > 0 else {}

                    # Set leaderline and body in attrs if supplied in either:
                    # 1. data
                    # 2. PinlabelGroup
                    attrs["leaderline"] = attrs.get("leaderline", None) or leaderline
                    attrs["body"] = attrs.get("body", None) or body

                    label = PinLabel(
                        content=content,
                        scale=scale,
                        **attrs,
                    )

                # -- label now exists -- #
                label.add_tag(tag)

                # Label follows another label in the row
                try:
                    prev_label = row_group.children[-1]
                    label.x = prev_label.x + prev_label.width * scale.x
                    label.y = prev_label.y + prev_label.body.y * scale.y
                    label.leaderline = lline.Straight(direction="hh")
                # Start of a new row
                except IndexError:
                    label.x, label.y = next(pin_coords)
                    x, y = next(label_coords)

                    label.body.x += x - label.x * scale.x
                    label.body.y += y - label.y * scale.y

                row_group.add(label)
