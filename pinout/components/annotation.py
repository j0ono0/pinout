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
    def __init__(self, content, width, height, **kwargs):
        self.content = content
        self._scale = core.Coords(*kwargs.pop("scale", (1, 1)))
        super().__init__(**kwargs)

        self.update_config(config.annotation["text"])

        # Add a 'spacer' (non-rendering) SvgShape so component
        # reports correct size before Body.render() called.
        self.add(core.SvgShape(width=width, height=height))

    def render(self):
        # Assemble at render as attributes may have
        # changed since instatiation.
        self.add(core.Rect(0, 0, self.width, self.height))

        if self._scale.x < 0:
            self.config["x"] = self.width - self.config["x"]
        if self._scale.y < 0:
            self.config["y"] = self.height - self.config["y"]

        self.add(
            type.TextBlock(
                self.content,
                scale=self._scale,
                **self.config,
            )
        )

        return super().render()


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
            self.config[name].update(obj)
            obj = Cls(content=self.content, scale=scale, **self.config[name])

        return self.add(obj)