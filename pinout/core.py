import uuid
from . import file_manager, templates
from .mixins import (
    TransformMixin,
    Coords,
    BoundingCoords,
    BoundingRect,
)
import pathlib


class Layout(TransformMixin):
    def __init__(self, x=0, y=0, tag=None, **kwargs):
        super().__init__(**kwargs)
        self.tag = tag
        self.x = x
        self.y = y
        self.children = []

    def add(self, instance):
        self.children.append(instance)
        return instance

    def bounding_rect(self):
        x1, y1, x2, y2 = self.bounding_coords()
        return BoundingRect(x1, y1, x2 - x1, y2 - y1)

    def bounding_coords(self):
        """Coordinates of the components's bounding rectangle.

        :return: (x1, y1, x2, y2)
        :rtype: BoundingCoords (namedtuple)
        """
        # Collect untransformed bounding coords
        x = []
        y = []
        for child in [
            instance
            for instance in self.children
            if hasattr(type(instance), "bounding_coords")
        ]:
            coords = child.bounding_coords()
            x.append(self.x + coords.x1 * self.scale.x)
            y.append(self.y + coords.y1 * self.scale.y)
            x.append(self.x + coords.x2 * self.scale.x)
            y.append(self.y + coords.y2 * self.scale.y)
        x.sort()
        y.sort()
        try:
            return BoundingCoords(x[0], y[0], x[-1], y[-1])
        except IndexError:
            # There are no children
            return BoundingCoords(0, 0, 0, 0)

    def render_children(self):
        output = ""
        for child in self.children:
            output += child.render()
        return output


class StyleSheet:
    def __init__(self, path, embed=False):
        self.path = path
        self.embed = embed

    def render(self):
        tplt = templates.get("style.svg")
        if not self.embed:
            return tplt.render(stylesheet=self)
        else:
            data = file_manager.load_data(self.path)
            return tplt.render(data=data)


class Diagram(Layout):
    def __init__(self, width, height, tag=None, **kwargs):
        super().__init__(tag=tag, **kwargs)
        self.width = width
        self.height = height
        self.defs = []

    def add_stylesheet(self, path, embed=True):
        self.children.insert(0, StyleSheet(path, embed))

    def add_defs(self, path):
        self.defs.append(file_manager.load_data(path))

    def render(self):
        tplt = templates.get("svg.svg")
        return tplt.render(svg=self)

    def export(self, path, overwrite=False):
        """Output the diagram in SVG format.

        :param path: File location and name
        :type path: string
        :param overwrite: Overwrite existing file of same path, defaults to False
        :type overwrite: bool, optional
        """
        # Create export location and unique filename if required
        path = pathlib.Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not overwrite:
            path = file_manager.unique_filepath(path)
        path.touch(exist_ok=True)

        # Render final SVG file
        path.write_text(self.render())
        print(f"'{path}' exported successfully.")


class Group(Layout):
    def __init__(self, x=0, y=0, tag=None, **kwargs):
        super().__init__(x=x, y=y, tag=tag, **kwargs)

    @property
    def width(self):
        return self.bounding_rect().w

    @property
    def height(self):
        return self.bounding_rect().h

    def render(self):
        tplt = templates.get("group.svg")
        return tplt.render(group=self)


class SvgShape(TransformMixin):
    def __init__(self, x=0, y=0, width=0, height=0, tag=None, **kwargs):
        super().__init__(**kwargs)
        self.tag = tag
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def bounding_rect(self):
        x1, y1, x2, y2 = self.bounding_coords()
        return BoundingRect(x1, y1, x2 - x1, y2 - y1)

    def bounding_coords(self):
        x = [self.x, (self.x * self.scale.x + self.width) * self.scale.x]
        y = [self.y, (self.y * self.scale.y + self.height) * self.scale.y]
        return BoundingCoords(min(x), min(y), max(x), max(y))


class Path(SvgShape):
    def __init__(self, path_definition="", **kwargs):
        super().__init__(**kwargs)
        self.d = path_definition

    def render(self):
        tplt = templates.get("path.svg")
        return tplt.render(path=self)


class Rect(SvgShape):
    def __init__(self, r, **kwargs):
        super().__init__(**kwargs)
        self.r = r
        self.uuid = uuid.uuid4()

    def render(self):
        tplt = templates.get("rect.svg")
        return tplt.render(rect=self)


class Text(SvgShape):
    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.content = content

    def render(self):
        tplt = templates.get("text.svg")
        return tplt.render(text=self)