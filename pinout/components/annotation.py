from pinout import core
from pinout.components import type
from pinout.components import leaderline as lline


class Base(core.Group):
    def __init__(self, **kwargs):
        self.offset = core.Coords(*kwargs.pop("offset", (1, 1)))
        kwargs["tag"] = ("annotation " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)


class Target(core.Rect):
    def __init__(self, **kwargs):
        kwargs["tag"] = ("annotation__target " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)


class Body(core.Rect):
    def __init__(self, **kwargs):
        kwargs["tag"] = ("annotation__body " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)


class Label(Base):
    def __init__(
        self,
        content,
        line_height=22,
        offset=(0, 0),
        text_offset=None,
        body=None,
        leaderline=None,
        target=None,
        **kwargs,
    ):
        self.content = content
        super().__init__(**kwargs)
        offset = core.Coords(*offset)
        text_offset = core.Coords(*text_offset)
        scale = core.Coords(*kwargs.get("scale", core.Coords(1, 1)))

        ##########################
        # Target
        config = {
            "x": -5,
            "y": -5,
            "width": 10,
            "height": 10,
        }
        try:
            cls, config_overrides = target
            config.update(config_overrides)
        except TypeError:
            cls = Target
        target = cls(**config)

        ##########################
        # Body
        config = {
            "x": offset.x,
            "y": offset.y,
            "width": 200,
            "height": len(content) * line_height + text_offset.x * 2,
        }
        try:
            cls, config_overrides = body
            config.update(config_overrides)
        except TypeError:
            cls = Body
        body = cls(**config)

        ##########################
        # Leaderline
        leaderline = leaderline or lline.Curved(direction="vv")
        leaderline.route(target, body)

        self.add(leaderline)
        self.add(target)
        self.add(body)

        ##########################
        # Text content
        if scale.x > 0:
            x = body.x + text_offset.x
        else:
            x = body.x + body.width - text_offset.x
        y = body.y + text_offset.y * self.scale.y + line_height / 2 + text_offset.x / 2

        self.add(
            type.TextBlock(
                content, line_height, x=x, y=y, width=body.width, scale=scale
            )
        )
