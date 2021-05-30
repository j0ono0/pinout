import base64
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
        self.defs = []

    def add(self, instance):
        if issubclass(type(instance), (SvgShape, Layout)):
            self.children.append(instance)
        return instance

    def add_def(self, instance):
        self.defs.append(instance)
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

    def render_defs(self):
        content = ""
        for d in self.defs:
            content += d.render()
        for child in [
            child for child in self.children if hasattr(child, "render_defs")
        ]:
            content += child.render_defs()
        return content

    def render_children(self):
        content = ""
        for child in self.children:
            content += child.render()
        return content


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


class Raw:
    def __init__(self, content):
        self.content = content

    def render(self):
        return self.content


class Diagram(Layout):
    def __init__(self, width, height, tag=None, **kwargs):
        super().__init__(tag=tag, **kwargs)
        self.width = width
        self.height = height

    def add_stylesheet(self, path, embed=True):
        self.children.insert(0, StyleSheet(path, embed))

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
    def __init__(
        self,
        x=0,
        y=0,
        width=0,
        height=0,
        tag=None,
        **kwargs,
    ):
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


class Image(SvgShape):
    def __init__(self, path, embed=False, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.embed = embed

    def render(self):
        """Render SVG markup either linking or embedding an image.

        :return: SVG markup
        :rtype: string
        """
        media_type = pathlib.Path(self.path).suffix[1:]
        path = pathlib.Path(self.path)
        tplt = templates.get("image.svg")
        if self.embed:
            if media_type == "svg":
                with path.open() as f:
                    svg_data = f.read()
                # Extract JUST the <svg> markup with no <XML> tag
                import xml.etree.ElementTree as ET

                tree = ET.fromstring(svg_data)
                just_svg_tag = ET.tostring(tree)
                return tplt.render(data=just_svg_tag)
            else:
                encoded_img = base64.b64encode(open(self.path, "rb").read())
                path = f"data:image/{media_type};base64,{encoded_img.decode('utf-8')}"

        return tplt.render(image=self)


########
# misc helper functions


def separate_sign(coords):
    sign = [coord // abs(coord) if coord != 0 else 1 for coord in coords]
    coords = [abs(coord) for coord in coords]
    return (tuple(coords), tuple(sign))