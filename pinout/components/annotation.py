import copy
from pinout import core
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline


class Leaderline(lline.Curved):
    pass


class Target(core.Rect):
    pass


class Body(core.Rect):
    pass


class Content(TextBlock):
    pass


class AnnotationLabel(core.Group):
    """Annotation style label."""

    def __init__(
        self,
        content=None,
        body=None,
        leaderline=None,
        target=None,
        **kwargs,
    ):
        self._content = None
        self._body = None
        self._leaderline = None
        self._target = None

        self.merge_config_into_kwargs(kwargs, "annotation")

        super().__init__(**kwargs)

        self.add_tag(self.config["tag"])

        self.leaderline = leaderline
        self.body = body
        self.target = target
        # content relied on body - must come after
        self.content = content

        # Route leaderline once other elements exist
        self._leaderline.route(self.target, self.body)

        self.add(self.leaderline)
        self.add(self.target)
        self.add(self.body)
        self.add(self.content)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        content = copy.deepcopy(content or {})
        config = self.config["content"]
        # Parse content: str > list > dict > TextBlock
        if type(content) is str:
            content = [content]
        if type(content) is list:
            content = {
                "content": content,
                "x": self.body.x + self.body.width / 2,
                "y": (self.body.y + self.body.height / 2)
                - (config["line_height"] * (len(content) - 1) / 2 * self.scale.y),
            }
        if isinstance(content, dict):
            config.update(content)
            content = Content(**config)
        content.add_tag(self.config["content"]["tag"])
        content.scale = self.scale
        self._content = content

    @property
    def leaderline(self):
        return self._leaderline

    @leaderline.setter
    def leaderline(self, leaderline):
        leaderline = copy.deepcopy(leaderline or {})
        if isinstance(leaderline, dict):
            leaderline_config = self.config["leaderline"]
            leaderline_config.update(leaderline)
            leaderline = Leaderline(**leaderline_config)
        leaderline.add_tag(self.config["leaderline"]["tag"])
        self._leaderline = leaderline

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        target = copy.deepcopy(target or {})
        if isinstance(target, dict):
            target_config = self.config["target"]
            target_config.update(target)
            target = Target(**target_config)
        target.add_tag(self.config["target"]["tag"])
        self._target = target

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        body = copy.deepcopy(body or {})
        if isinstance(body, dict):
            body_config = self.config["body"]
            body_config.update(body)
            body = Body(**body_config)
        body.add_tag(self.config["body"]["tag"])
        self._body = body
