import base64
import copy
import math
import pathlib
import urllib.request
import PIL
from collections import namedtuple
from pinout import manager, templates


Coords = namedtuple("Coords", ("x y"))
BoundingCoords = namedtuple("BoundingCoords", ("x1 y1 x2 y2"))
BoundingRect = namedtuple("BoundingCoords", ("x y w h"))


class TransformMixin:
    def __init__(
        self,
        matrix=None,
        translate=None,
        scale=(1, 1),
        rotate=0,
        skewx=None,
        skewy=None,
        **kwargs,
    ):
        # kwargs that make it to here are ignored.
        self.matrix = matrix
        self.translate = translate
        self.scale = Coords(*scale)
        self.rotate = rotate
        self.skewx = skewx
        self.skewy = skewy


class Layout(TransformMixin):
    """Base class for components that fundamentally group other components together."""

    def __init__(self, x=0, y=0, tag=None, **kwargs):
        super().__init__(**kwargs)
        self.tag = tag
        self.x = x
        self.y = y
        self.children = []
        self.defs = []
        self.config = kwargs.pop("config", {})

    def add(self, instance):
        self.children.append(instance)
        return instance

    def add_def(self, instance):
        """Add a component to the svg 'def' section

        :param instance: pinout component
        :return: instance added
        :rtype: pinout components
        """
        self.defs.append(instance)
        return instance

    def add_tag(self, tag):
        """Append a tag to the instance

        :param tag: CSS class name(s)
        :type tag: string
        """
        tag_list = (self.tag or "").split(" ")
        if tag not in tag_list:
            tag_list.append(tag)
        self.tag = " ".join(tag_list)

    def update_config(self, vals):
        """update config dict

        :param vals: Values to update
        :type vals: dict
        """
        self.config.update(copy.deepcopy(vals))

    @staticmethod
    def find_children_by_type(component, target_type):
        """Recursively find all children of the component and it's decendents by type.

        :param component: Component instance to start seach from
        :type component: class instance
        :param target_type: class  to match with instances
        :type target_type: class
        :return: All instances of type 'target_type' that are descendents of 'component'
        :rtype: list
        """
        results = []
        try:
            for c in component.children:
                if isinstance(c, target_type):
                    results.append(c)
                results += Layout.find_children_by_type(c, target_type)
        except AttributeError:
            pass
            # No children

        return results

    def bounding_rect(self):
        """Top left coordinates with width and height of a bounding rectangle

        :return: origin coordinates and rectangle dimensions
        :rtype: tuple (x, y, w, h)
        """
        x1, y1, x2, y2 = self.bounding_coords()
        return BoundingRect(x1, y1, x2 - x1, y2 - y1)

    def rotated_coords(self, x, y):
        return Coords(
            x * math.cos(math.radians(-self.rotate))
            + y * math.sin(math.radians(-self.rotate)),
            -x * math.sin(math.radians(-self.rotate))
            + y * math.cos(math.radians(-self.rotate)),
        )

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
            # Transform with rotate
            x1, y1, x2, y2 = x[0], y[0], x[-1], y[-1]
            top_left = self.rotated_coords(x1, y1)
            top_right = self.rotated_coords(x2, y1)
            bottom_left = self.rotated_coords(x1, y2)
            bottom_right = self.rotated_coords(x2, y2)
            zipped = [
                sorted(list(coord))
                for coord in zip(top_left, top_right, bottom_left, bottom_right)
            ]
            return BoundingCoords(
                zipped[0][0], zipped[1][0], zipped[0][-1], zipped[1][-1]
            )
        except IndexError:
            # There are no children
            return BoundingCoords(0, 0, 0, 0)

    def render_defs(self):
        """Render SVG markup from 'defs'

        :return: SVG markup
        :rtype: string
        """
        content = ""
        for d in self.defs:
            content += d.render()
        for child in [
            child for child in self.children if hasattr(child, "render_defs")
        ]:
            content += child.render_defs()
        return content

    def render_children(self):
        """Render SVG markup from 'children'

        :return: SVG markup
        :rtype: string
        """
        content = ""
        for child in self.children:
            try:
                content += child.render()
            except TypeError as e:
                print(child)
                print(child.render())
                print(e)
        return content


class Group(Layout):
    """Group components together"""

    def __init__(self, x=0, y=0, tag=None, **kwargs):
        super().__init__(x=x, y=y, tag=tag, **kwargs)

    @property
    def width(self):
        return self.bounding_rect().w

    @property
    def height(self):
        return self.bounding_rect().h

    def render(self):
        """Render children into a <group> tag.

        :return: SVG markup
        :rtype: string
        """
        tplt = templates.get("group.svg")
        return tplt.render(group=self)


class StyleSheet:
    """Include a cascading stylesheet."""

    def __init__(self, path, embed=False):
        self.path = path
        self.embed = embed

    def render(self):
        tplt = templates.get("style.svg")
        if not self.embed:
            return tplt.render(stylesheet=self)
        else:
            data = manager.load_data(self.path)
            return tplt.render(data=data)


class Raw:
    """Include arbitary code to the document"""

    def __init__(self, content):
        self.content = content

    def render(self):
        return self.content


class SvgShape(TransformMixin):
    """Base class for components that have a graphical representation"""

    def __init__(
        self,
        x=0,
        y=0,
        width=0,
        height=0,
        tag=None,
        **kwargs,
    ):
        self.tag = tag
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clip_id = kwargs.pop("clip_id", None)
        super().__init__(**kwargs)

    def bounding_rect(self):
        x1, y1, x2, y2 = self.bounding_coords()
        return BoundingRect(x1, y1, x2 - x1, y2 - y1)

    def bounding_coords(self):
        x = [self.x, (self.x * self.scale.x + self.width) * self.scale.x]
        y = [self.y, (self.y * self.scale.y + self.height) * self.scale.y]
        return BoundingCoords(min(x), min(y), max(x), max(y))

    def add_tag(self, tag):
        """Append a tag to the instance

        :param tag: CSS class name(s)
        :type tag: string
        """
        tag_list = (self.tag or "").split(" ")
        if tag not in tag_list:
            tag_list.append(tag)
        self.tag = " ".join(tag_list)

    def render(self):
        return ""


class Path(SvgShape):
    """SVG Path object"""

    def __init__(self, path_definition="", **kwargs):
        super().__init__(**kwargs)
        self.d = path_definition

    def render(self):
        """Render a <path> tag.

        :return: SVG markup
        :rtype: string
        """
        tplt = templates.get("path.svg")
        return tplt.render(path=self)


class Rect(SvgShape):
    """SVG <rect> object"""

    def __init__(self, *args, corner_radius=0, **kwargs):
        self.corner_radius = corner_radius
        super().__init__(*args, **kwargs)

    def render(self):
        """Render a <rect> tag.

        :return: SVG markup
        :rtype: string
        """
        tplt = templates.get("rect.svg")
        return tplt.render(rect=self)


class Text(SvgShape):
    """SVG <text> object"""

    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.content = content

    def render(self):
        """Render a <text> tag.

        :return: SVG markup
        :rtype: string
        """
        tplt = templates.get("text.svg")
        return tplt.render(text=self)


class Image(SvgShape):
    """Include a image in the diagram."""

    def __init__(self, path, embed=False, **kwargs):
        self.path = path
        self.svg_data = None
        self.embed = embed
        self.coords = {}

        # Load image dimensions to avoid multiple loads when calculating coords
        im = PIL.Image.open(self.path)
        self.im_size = im.size

        # Use actual image dimensions if none supplied
        kwargs["width"] = kwargs.get("width", self.im_size[0])
        kwargs["height"] = kwargs.get("height", self.im_size[1])

        super().__init__(**kwargs)

    def coord(self, name, raw=False):
        """Coordnates are calculated on the scaled image.
        **IMPORTANT** image is scaled proportionally
        to fit within the supplied width and height"""

        x, y = self.coords[name]

        # Actual image size:
        iw, ih = self.im_size

        # Scale x and y to match user supplied dimensions
        scaler = min(self.width / iw, self.height / ih)

        # Transformed size
        tw, th = iw * scaler, ih * scaler

        # Transformed x and y coords
        tx = x * scaler
        ty = y * scaler

        if not raw:
            # NOTE: svg transforms images proportionally to 'fit' supplied dimensions
            # if 'raw' is False translate the coords
            tx = tx + (self.width - tw) / 2 + self.x
            ty = ty + (self.height - th) / 2 + self.y

        return Coords(tx, ty)

    def add_coord(self, name, x, y):
        """Record coordinates on the **unscaled** image. When returned with Image.coord() the values are scaled to match the image scaling.

        :param name: Name of coordinate
        :type name: string
        :param x: x-axis coordinate
        :type x: int
        :param y: y-axis coordinate
        :type y: int
        """
        self.coords[name] = Coords(x, y)

    def loadData(self):
        """Load image data from URL or local file system."""
        try:
            with open(self.path, "rb") as f:
                return f.read()
        except OSError:
            try:
                with urllib.request.urlopen(self.path) as f:
                    return f.read()
            except urllib.error.HTTPError as e:
                print(e.code)

    def render(self):
        """Render SVG markup either linking or embedding an image."""
        media_type = pathlib.Path(self.path).suffix[1:]
        tplt = templates.get("image.svg")

        if self.embed:
            if media_type == "svg":
                data = self.loadData()
                # Extract JUST the <svg> markup with no <XML> tag
                import xml.etree.ElementTree as ET

                tree = ET.fromstring(data)
                self.svg_data = ET.tostring(tree)
            else:
                encoded_img = base64.b64encode(self.loadData())
                self.path = (
                    f"data:image/{media_type};base64,{encoded_img.decode('utf-8')}"
                )

        return tplt.render(image=self)
