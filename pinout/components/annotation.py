from pinout import core
from pinout.components import type
from pinout.components import leaderline as lline

from pinout import config


class Base(core.Group):
    def __init__(self, **kwargs):
        self.offset = core.Coords(*kwargs.pop("offset", (1, 1)))
        kwargs["tag"] = ("annotation " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)


class Leaderline(lline.Curved):
    pass


class Target(core.Rect):
    def __init__(self, **kwargs):
        kwargs["tag"] = ("annotation__target " + kwargs.pop("tag", "")).strip()
        super().__init__(**kwargs)


class Body(core.Group):
    def __init__(
        self,
        content,
        x=None,
        y=None,
        width=None,
        height=None,
        corner_radius=None,
        textblock=None,
        **kwargs,
    ):
        scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        super().__init__(**kwargs)

        # Load default config (in case of creation independently)
        self.update_config(config.annotation["body"])

        # Body background shape
        width = width or self.config["width"]
        height = height or self.config["height"]
        corner_radius = corner_radius or self.config["corner_radius"]
        tag = config.annotation["tag"] + "__bg"
        self.add(
            core.Rect(
                x=0,
                y=0,
                width=width,
                height=height,
                corner_radius=corner_radius,
                tag=tag,
            )
        )

        self.x = x or self.config["x"]
        self.y = y or self.config["y"]

        textblock = textblock or {}
        if isinstance(textblock, dict):
            textblock_config = self.config["textblock"]
            textblock_config.update(textblock)

            # Align text block accoring to +/- scale
            if scale.x < 0:
                textblock_config["x"] = self.width - textblock_config["x"]
            if scale.y < 0:
                textblock_config["y"] = self.height - textblock_config["y"]

            textblock = type.TextBlock(content, scale=scale, **textblock_config)
        self.add(textblock)


class AnnotationLabel(Base):
    def __init__(
        self,
        content,
        body=None,
        leaderline=None,
        target=None,
        **kwargs,
    ):
        self.content = content
        body = body or {}
        leaderline = leaderline or {}
        target = target or {}

        super().__init__(**kwargs)
        self.update_config(config.annotation)

        # add annotation sub-components
        leaderline = self.add_component(Leaderline, "leaderline", leaderline)
        target = self.add_component(Target, "target", target)
        body = self.add_component(Body, "body", body, self.scale)

        # Route leaderline once other elements exist
        leaderline.route(target, body)

    def add_component(self, Cls, name, obj, scale=(1, 1)):

        if isinstance(obj, dict):
            # Update config with dict items
            self.config[name].update(obj)
            # Replace dict with class instance
            # Unneeded attr (content) is 'consumed'
            # by kwargs in target and leaderline
            obj = Cls(content=self.content, scale=scale, **self.config[name])

        return self.add(obj)