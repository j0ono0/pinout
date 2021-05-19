import re
import cairo
from collections import namedtuple


Coords = namedtuple("Coords", ("x y"))


class SvgTransformMixin:
    def __init__(
        self,
        matrix=None,
        translate=None,
        scale=(1, 1),
        rotate=None,
        skewx=None,
        skewy=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.matrix = matrix
        self.translate = translate
        self.scale = Coords(*scale)
        self.rotate = rotate
        self.skewx = skewx
        self.skewy = skewy


class SvgPresentationMixin:
    def __init__(
        self,
        fill=(1, 1, 0, 1),
        fill_opacity=1,
        fill_rule=None,
        filter=None,
        mask=None,
        opacity=1,
        stroke=(0, 0, 0, 1),
        stroke_dasharray=None,
        stroke_dashoffset=None,
        stroke_linecap=None,
        stroke_linejoin=None,
        stroke_miterlimit=None,
        stroke_opacity=1,
        stroke_width=0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.fill_rule = fill_rule
        self.filter = filter
        self.mask = mask
        self.opacity = opacity
        self.stroke = stroke
        self.stroke_dasharray = stroke_dasharray
        self.stroke_dashoffset = stroke_dashoffset
        self.stroke_linecap = stroke_linecap
        self.stroke_linejoin = stroke_linejoin
        self.stroke_miterlimit = stroke_miterlimit
        self.stroke_opacity = stroke_opacity
        self.stroke_width = stroke_width


class Layout(SvgPresentationMixin, SvgTransformMixin):
    def __init__(self, x=0, y=0, width=1200, height=675, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = []

    def add(self, instance):
        if isinstance(instance, Layout):
            instance.width = self.width
            instance.height = self.height
        self.children.append(instance)
        return instance

    def bounding_rect(self):
        x1, y1, x2, y2 = self.bounding_coords()
        return (x1, y1, x2 - x1, y2 - y1)

    def bounding_coords(self):
        x1, y1, x2, y2 = self.extents()
        return (x1 + self.x, y1 + self.y, x2 + self.x, y2 + self.y)

    def extents(self):
        coord_arr = list(zip(*[child.bounding_coords() for child in self.children]))
        x1 = min(coord_arr[0])
        y1 = min(coord_arr[1])
        x2 = max(coord_arr[2])
        y2 = max(coord_arr[3])
        return (x1, y1, x2, y2)

    def render(self, ctx):
        for child in self.children:
            ctx.save()
            ctx.scale(*self.scale)
            child.render(ctx)
            ctx.restore()


class Group(Layout):
    def __init__(self, x, y, **kwargs):
        super().__init__(x=x, y=y, **kwargs)

    def render(self, ctx):
        ctx.save()
        ctx.push_group()

        ctx.translate(self.x, self.y)
        super().render(ctx)

        group = ctx.pop_group()
        ctx.set_source(group)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()
        ctx.restore()


class Diagram(Layout):
    def __init__(self, width, height, **kwargs):
        super().__init__(width=width, height=height, **kwargs)

    def render_png(self, path):
        with cairo.ImageSurface(
            cairo.FORMAT_ARGB32, self.width, self.height
        ) as surface:
            ctx = cairo.Context(surface)
            self.render(ctx)
            surface.write_to_png(f"{path}.png")

    def render_svg(self, path):
        with cairo.SVGSurface(f"{path}.svg", self.width, self.height) as surface:
            ctx = cairo.Context(surface)
            self.render(ctx)


class Path(SvgPresentationMixin, SvgTransformMixin):
    def __init__(self, x=0, y=0, d="", **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.d = self.parse_path_definition(d)

    def parse_path_definition(self, d):
        return [i.strip() for i in re.findall(r"[a-zA-Z] [ 0-9]+", d)]

    def move_to(self, ctx, x, y):
        ctx.move_to(x, y)

    def line_to(self, ctx, x, y):
        ctx.line_to(x, y)

    def curve_to(self, ctx, x1, y1, x2, y2, x, y):
        ctx.curve_to(x1, y1, x2, y2, x, y)

    def draw_path(self, ctx):
        fn_map = {
            "M": self.move_to,
            "L": self.line_to,
            "C": self.curve_to,
        }
        for instruction in self.d:
            fn, args = instruction.split(" ", 1)
            # convert args to float
            args = [float(arg) for arg in args.split(" ")]
            fn_map[fn](ctx, *args)

    def bounding_rect(self):
        x1, y1, x2, y2 = self.bounding_coords()
        return (x1, y1, x2 - x1, y2 - y1)

    def bounding_coords(self):
        x1, y1, x2, y2 = self.extents()
        return (x1 + self.x, y1 + self.y, x2 + self.x, y2 + self.y)

    def extents(self):
        with cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1) as surface:
            ctx = cairo.Context(surface)
            self.draw_path(ctx)
            return ctx.path_extents()

    def render_stroke(self, ctx):
        ctx.set_line_width(self.stroke_width)
        ctx.set_source_rgba(*self.stroke)

        self.draw_path(ctx)
        ctx.translate(self.x, self.y)
        ctx.stroke()

    def render(self, ctx):
        ctx.save()
        ctx.scale(*self.scale)
        ctx.translate(self.x, self.y)
        self.render_stroke(ctx)
        ctx.restore()


class Polygon(Path):
    def draw_path(self, ctx):
        super().draw_path(ctx)
        ctx.close_path()

    def render_fill(self, ctx):
        ctx.set_source_rgba(*self.fill)
        self.draw_path(ctx)
        ctx.fill()

    def render_stroke(self, ctx):
        # clip hides stroke outside polygon
        ctx.set_line_width(self.stroke_width * 2)
        ctx.set_source_rgba(*self.stroke)
        self.draw_path(ctx)
        ctx.clip_preserve()
        ctx.stroke()
        ctx.clip()

    def render(self, ctx):
        ctx.save()
        ctx.scale(*self.scale)
        ctx.translate(self.x, self.y)
        self.render_fill(ctx)
        self.render_stroke(ctx)
        ctx.restore()


class Rect(Polygon):
    def __init__(self, x=0, y=0, width=10, height=10, r=0, **kwargs):
        x1 = 0
        y1 = 0
        x2 = width
        y2 = height
        path_def = " ".join(
            (
                f"M {x1 + r} {y1}",
                f"L {x2 - r} {y1}",
                f"C {x2} {y1} {x2} {y1} {x2} {y1 + r}",
                f"L {x2} {y2 - r}",
                f"C {x2} {y2} {x2} {y2} {x2 - r} {y2}",
                f"L {x1 + r} {y2}",
                f"C {x1} {y2} {x1} {y2} {x1} {y2 - r}",
                f"L {x1} {y1 + r}",
                f"C {x1} {y1} {x1} {y1} {x1 + r} {y1}",
            )
        )
        super().__init__(x, y, path_def, **kwargs)
