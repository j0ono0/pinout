from pinout import core
from pinout.components import type


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


class LeaderLineCurved(core.Path):
    def __init__(self, target, body, style=None, **kwargs):
        kwargs["tag"] = ("annotation__leaderline " + kwargs.pop("tag", "")).strip()

        t_coords = target.bounding_coords()
        b_coords = body.bounding_coords()

        start_v = core.Coords(target.x + (t_coords.x2 - t_coords.x1) / 2, t_coords.y2)
        start_h = core.Coords(t_coords.x2, target.y + (t_coords.y2 - t_coords.y1) / 2)
        end_v = core.Coords(body.x + (b_coords.x2 - b_coords.x1) / 2, b_coords.y1)
        end_h = core.Coords(b_coords.x1, body.y + (b_coords.y2 - b_coords.y1) / 2)

        r = min(body.x, body.y) / 3
        len = (b_coords.x1 - t_coords.x2) / 8
        ctl_h = (b_coords.x1 - t_coords.x2) / 2
        ctl_v = (b_coords.y1 - t_coords.y2) / 2

        if style == "vh":
            # start vertical, end horizontal
            path_def = " ".join(
                [
                    f"M {start_v.x} {start_v.y}",
                    f"L {start_v.x} {end_h.y - r}",
                    f"A {r} {r} 0 0 0 {start_v.x + r} {end_h.y}",
                    f"L {end_h.x} {end_h.y}",
                ]
            )
        elif style == "hv":
            # start horizontal, end vertical
            path_def = " ".join(
                [
                    f"M {start_h.x} {start_h.y}",
                    f"L {end_v.x - r} {start_h.y}",
                    f"A {r} {r} 0 0 1 {end_v.x} {start_h.y + r}",
                    f"L {end_v.x} {end_v.y}",
                ]
            )
        elif style == "hh":
            # start horizontal, end horizontal
            path_def = " ".join(
                [
                    f"M {start_h.x} {start_h.y}",
                    f"L {start_h.x + len} {start_h.y}",
                    f"C {start_h.x + ctl_h} {start_h.y} {end_h.x - ctl_h} {end_h.y} {end_h.x - len} {end_h.y}",
                    f"L {end_h.x} {end_h.y}",
                ]
            )
        elif style == "vv":
            # start vertical, end vertical
            path_def = " ".join(
                [
                    f"M {start_v.x} {start_v.y}",
                    f"L {start_v.x} {start_v.y + len}",
                    f"C {start_v.x} {start_v.y + ctl_v} {end_v.x} {end_v.y - ctl_v} {end_v.x} {end_v.y - len}",
                    f"L {end_v.x} {end_v.y}",
                ]
            )
        else:
            path_def = ""

        super().__init__(path_definition=path_def, **kwargs)


class LeaderLineAngled(core.Path):
    def __init__(self, target, body, style=None, **kwargs):
        kwargs["tag"] = ("annotation__leaderline " + kwargs.pop("tag", "")).strip()

        t_coords = target.bounding_coords()
        b_coords = body.bounding_coords()

        start_v = core.Coords(target.x + (t_coords.x2 - t_coords.x1) / 2, t_coords.y2)
        start_h = core.Coords(t_coords.x2, target.y + (t_coords.y2 - t_coords.y1) / 2)
        end_v = core.Coords(body.x + (b_coords.x2 - b_coords.x1) / 2, b_coords.y1)
        end_h = core.Coords(b_coords.x1, body.y + (b_coords.y2 - b_coords.y1) / 2)

        if style == "vh":
            # start vertical, end horizontal
            path_def = " ".join(
                [
                    f"M {start_v.x} {start_v.y}",
                    f"L {start_v.x} {end_h.y}",
                    f"L {end_h.x} {end_h.y}",
                ]
            )
        elif style == "hv":
            # start horizontal, end vertical
            path_def = " ".join(
                [
                    f"M {start_h.x} {start_h.y}",
                    f"L {end_v.x} {start_h.y}",
                    f"L {end_v.x} {end_v.y}",
                ]
            )
        elif style == "hh":
            # start horizontal, end horizontal
            path_def = " ".join(
                [
                    f"M {start_h.x} {start_h.y}",
                    f"L {start_h.x + (end_h.x - start_h.x)/4} {start_h.y}",
                    f"L {start_h.x + (end_h.x - start_h.x)/4} {end_h.y}",
                    f"L {end_h.x} {end_h.y}",
                ]
            )
        elif style == "vv":
            # start vertical, end vertical
            path_def = " ".join(
                [
                    f"M {start_v.x} {start_v.y}",
                    f"L {start_v.x} {start_v.y + (end_v.y - start_v.y)/4}",
                    f"L {end_v.x} {start_v.y + (end_v.y - start_v.y)/4}",
                    f"L {end_v.x} {end_v.y}",
                ]
            )
        else:
            path_def = ""

        super().__init__(path_definition=path_def, **kwargs)


class LeaderLine(core.Path):
    def __init__(self, target, body, style=None, **kwargs):
        kwargs["tag"] = ("annotation__leaderline " + kwargs.pop("tag", "")).strip()

        t_coords = target.bounding_coords()
        b_coords = body.bounding_coords()

        start_v = core.Coords(target.x + (t_coords.x2 - t_coords.x1) / 2, t_coords.y2)
        start_h = core.Coords(t_coords.x2, target.y + (t_coords.y2 - t_coords.y1) / 2)
        end_v = core.Coords(body.x + (b_coords.x2 - b_coords.x1) / 2, b_coords.y1)
        end_h = core.Coords(b_coords.x1, body.y + (b_coords.y2 - b_coords.y1) / 2)

        if style == "vh":
            # start vertical, end horizontal
            path_def = " ".join(
                [
                    f"M {start_v.x} {start_v.y}",
                    f"L {end_h.x} {end_h.y}",
                ]
            )
        elif style == "hv":
            # start horizontal, end vertical
            path_def = " ".join(
                [
                    f"M {start_h.x} {start_h.y}",
                    f"L {end_v.x} {end_v.y}",
                ]
            )
        elif style == "hh":
            # start horizontal, end horizontal
            path_def = " ".join(
                [
                    f"M {start_h.x} {start_h.y}",
                    f"L {end_h.x} {end_h.y}",
                ]
            )
        elif style == "vv":
            # start vertical, end vertical
            path_def = " ".join(
                [
                    f"M {start_v.x} {start_v.y}",
                    f"L {end_v.x} {end_v.y}",
                ]
            )
        else:
            path_def = ""

        super().__init__(path_definition=path_def, **kwargs)


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
            "r": 0,
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
            "r": 0,
            "x": offset.x,
            "y": offset.y,
            "width": 200,
            "height": len(content) * line_height + text_offset.x,
        }
        try:
            cls, config_overrides = body
            config.update(config_overrides)
        except TypeError:
            cls = Body
        body = cls(**config)

        ##########################
        # Leaderline
        config = {
            "target": target,
            "body": body,
            "style": "vv",
        }
        try:
            cls, config_overrides = leaderline
            config.update(config_overrides)
        except TypeError:
            cls = LeaderLine
        leaderline = cls(**config)

        self.add(leaderline)
        self.add(target)
        self.add(body)

        if scale.x > 0:
            x = body.x + text_offset.x
        else:
            x = body.x + body.width - text_offset.x
        y = body.y + text_offset.y + line_height / 2 + text_offset.x / 2

        self.add(
            type.TextBlock(
                content, line_height, x=x, y=y, width=body.width, scale=scale
            )
        )
