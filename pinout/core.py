import base64
import collections.abc
import copy
import math
import pathlib
import PIL
from PIL import Image as PILImage
import re
import urllib.request
import uuid
import warnings
import xml.etree.ElementTree as ET
from collections import namedtuple
from pinout import manager, templates, config_manager


Coords = namedtuple("Coords", ("x y"))
BoundingCoords = namedtuple("BoundingCoords", ("x1 y1 x2 y2"))
BoundingRect = namedtuple("BoundingCoords", ("x y w h"))


class IdGenerator:
    def __init__(self):
        self.base = str(uuid.uuid4())
        self.counter = 0

    def __call__(self):
        self.counter += 1
        return f"{self.base}_{self.counter}"


diagram_id = IdGenerator()


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

        super().__init__()


class Component:
    """common functions and attributes shared by all components"""

    def __init__(self, clip=None, config=None, defs=None, tag=None, **kwargs):
        self._clip = None
        self.config = config or {}
        self.defs = defs or []
        self.id = diagram_id()
        self.tag = tag
        super().__init__(**kwargs)

        self.clip = clip

        try:
            # Add config tag(s). These include the default tag
            self.add_tag(self.config["tag"])
        except:
            # No config tag provided
            pass

    @property
    def clip(self):
        return self._clip

    @clip.setter
    def clip(self, obj):
        if obj:
            if isinstance(obj, ClipPath):
                self._clip = obj
            else:
                self._clip = ClipPath(children=obj)

    def add_def(self, instance):
        """Add a component to the svg 'def' section"""
        if instance:
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

    def update_data_dict(self, d, u):
        """Update dict including recursively update dicts that are values. Values are copied.

        :param d: Dict to update, can include dict values
        :type d: dict
        :param u: Values to update
        :type u: dict
        """
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.update_data_dict(d.get(k, {}), v)
            else:
                d[k] = copy.deepcopy(v)
        return d

    def merge_config_into_kwargs(self, kwargs, config_attr):
        kwarg_cfg = kwargs.pop("config", {})
        app_cfg = config_manager.get(config_attr)
        kwargs["config"] = self.update_data_dict(app_cfg, kwarg_cfg)

    def update_config(self, vals, cfg=None):
        cfg = cfg or self.config
        """update config dict

        :param vals: Values to update
        :type vals: dict
        """
        warnings.warn(f"Update_config is to be decomissioned!. cfg ref: {cfg}")
        self.config.update(copy.deepcopy(vals))

    def render_defs(self):
        """Render SVG markup from 'defs'

        :return: SVG markup
        :rtype: string
        """
        content = ""

        # Transfer clippath to defs
        self.add_def(self.clip)

        # Render defs
        for d in self.defs:
            try:
                content += d.render()
            except AttributeError as e:
                print("*", d)
                print(d.render)
                print(d.render())
                print(e)

        # Recursively render children defs
        try:
            for child in [
                child for child in self.children if hasattr(child, "render_defs")
            ]:
                content += child.render_defs()
        except AttributeError:
            pass
            # Object has no children

        return content

    @staticmethod
    def rotate_box_coords(origin, coords, rotate):
        ox, oy = origin
        x1, y1, x2, y2 = coords
        # rotate corners of bounding box
        corners = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
        rx = []
        ry = []
        for (x, y) in corners:
            rx.append(
                ox
                + (x - ox) * math.cos(math.radians(rotate))
                - (y - oy) * math.sin(math.radians(rotate))
            )
            ry.append(
                oy
                + (x - ox) * math.sin(math.radians(rotate))
                + (y - oy) * math.cos(math.radians(rotate))
            )

        return BoundingCoords(min(rx), min(ry), max(rx), max(ry))


class Layout(Component, TransformMixin):
    """Base class fundamentally grouping other components together."""

    def __init__(self, x=0, y=0, children=None, **kwargs):
        self.x = x
        self.y = y
        self.children = children or []

        super().__init__(**kwargs)

    def add(self, instance):
        self.children.append(instance)
        return instance

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

    def bounding_coords(self):
        """Coordinates of the components's bounding rectangle.

        :return: (x1, y1, x2, y2)
        :rtype: BoundingCoords (namedtuple)
        """
        # Collect bounding coords of children
        x = []
        y = []
        if self.clip:
            targets = self.clip.children
        else:
            targets = self.children
        for child in [
            instance
            for instance in targets
            if hasattr(type(instance), "bounding_coords")
        ]:
            coords = child.bounding_coords()
            x.append(self.x + coords.x1 * self.scale.x)
            y.append(self.y + coords.y1 * self.scale.y)
            x.append(self.x + coords.x2 * self.scale.x)
            y.append(self.y + coords.y2 * self.scale.y)

        try:
            x1, y1, x2, y2 = min(x), min(y), max(x), max(y)

            # Clip object has its own rotation
            if self.clip:
                return BoundingCoords(x1, y1, x2, y2)

            # rotate corners of bounding box
            corners = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
            rx = []
            ry = []
            for (x, y) in corners:
                rx.append(
                    self.x
                    + (x - self.x) * math.cos(math.radians(self.rotate))
                    - (y - self.y) * math.sin(math.radians(self.rotate))
                )
                ry.append(
                    self.y
                    + (x - self.x) * math.sin(math.radians(self.rotate))
                    + (y - self.y) * math.cos(math.radians(self.rotate))
                )

            return BoundingCoords(min(rx), min(ry), max(rx), max(ry))

        except ValueError:
            # There are no children
            return BoundingCoords(0, 0, 0, 0)

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
                print(f"An error occurred rendering: {child}")
                print(child.render())
                print(e)
        return content


class Use(Layout):
    """Implement <use> svg tag"""

    def __init__(self, instance, **kwargs):
        self.target_id = instance.id

        super().__init__(**kwargs)

    def render(self):
        # convert kwargs into parameters for <use>
        tplt = templates.get("use.svg")
        return tplt.render(use=self)


class Group(Layout):
    """Group components together"""

    def __init__(self, x=0, y=0, tag=None, **kwargs):

        self.merge_config_into_kwargs(kwargs, "group")
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


class ClipPath(Group):
    """Define a clip-path component"""

    def __init__(self, children=None, **kwargs):
        super().__init__(**kwargs)
        # Accept 'children' as list or single instance.
        children = children or []
        try:
            for child in children:
                self.add(child)
        except TypeError:
            # Children is a single component (not an iterible)
            self.add(children)

    def render(self):
        """Render children into a <clipPath> tag."""
        tplt = templates.get("clippath.svg")
        return tplt.render(path=self)


class StyleSheet:
    """Include a cascading stylesheet."""

    def __init__(self, src, embed=False):
        self._src = None
        self.src = src
        self.embed = embed

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, val):
        self._src = pathlib.Path(val)

    def render(self):
        tplt = templates.get("style.svg")
        if not self.embed:
            return tplt.render(stylesheet=self)
        else:
            data = manager.load_data(self.src)
            return tplt.render(data=data)


class Raw:
    """Include arbitary code to the document"""

    def __init__(self, content):
        self.content = content

    def render(self):
        return self.content


class SvgShape(Component, TransformMixin):
    """Base class for components that have a graphical representation."""

    def __init__(self, x=0, y=0, width=0, height=0, **kwargs):
        self.x = x
        self.y = y
        self._width = width
        self._height = height

        self.merge_config_into_kwargs(kwargs, "svgshape")

        super().__init__(**kwargs)

    @property
    def width(self):
        if self.clip:
            return self.clip.width
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def height(self):
        if self.clip:
            return self.clip.height
        return self._height

    @height.setter
    def height(self, val):
        self._height = val

    def bounding_rect(self):
        """Component's origin coordinates and dimensions"""
        x1, y1, x2, y2 = self.bounding_coords()
        return BoundingRect(x1, y1, x2 - x1, y2 - y1)

    def bounding_coords(self):
        """Coordinates representing a shape's bounding-box."""
        if self.clip:
            return self.clip.bounding_coords()
        else:
            x = [self.x * self.scale.x, (self.x + self.width) * self.scale.x]
            y = [self.y * self.scale.y, (self.y + self.height) * self.scale.y]

            return Component.rotate_box_coords(
                origin=(self.x, self.y),
                coords=(min(x), min(y), max(x), max(y)),
                rotate=self.rotate,
            )

    def render(self):
        return ""


class Path(SvgShape):
    """SVG Path object"""

    def __init__(self, path_definition="", **kwargs):
        self.merge_config_into_kwargs(kwargs, "path")
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
        self.merge_config_into_kwargs(kwargs, "rect")
        super().__init__(*args, **kwargs)

    def render(self):
        """Render a <rect> tag.

        :return: SVG markup
        :rtype: string
        """
        tplt = templates.get("rect.svg")
        return tplt.render(rect=self)


class Circle(SvgShape):
    """SVG <circle> object"""

    def __init__(self, cx, cy, r, **kwargs):
        self.r = r
        kwargs["x"] = cx
        kwargs["y"] = cy
        self.merge_config_into_kwargs(kwargs, "circle")
        super().__init__(**kwargs)

    def render(self):
        """Render a <circle> tag."""

        tplt = templates.get("circle.svg")
        return tplt.render(circle=self)


class Text(SvgShape):
    """SVG <text> object"""

    def __init__(self, content, **kwargs):

        self.merge_config_into_kwargs(kwargs, "text")
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
    """Include an image in the diagram."""

    def __init__(self, src, dpi=72, embed=False, **kwargs):
        self.coords = kwargs.pop("coords", {})
        self._dpi = dpi
        self.embed = embed
        self.im_size = (1, 1)
        self.src = src
        self.svg_data = None

        try:
            # Load image dimensions to avoid multiple loads when calculating coords
            # Allow relative paths outside CWD
            cwd = pathlib.Path.cwd()
            im = PILImage.open(cwd.joinpath(self.src))
            self.im_size = im.size
        except TypeError as e:
            # Image src is assumed to be another Image instance
            self.im_size = self.src.im_size
            self.coords = self.src.coords

        except PIL.UnidentifiedImageError:
            # Image is assumed to be SVG
            self.set_svg_im_size()

        except OSError:
            try:
                # file not at local path, try path as URL
                im = PILImage.open(urllib.request.urlopen(self.src))
                self.im_size = im.size
            except (PIL.UnidentifiedImageError):
                # Image is assumed to be SVG
                # Match arbitary im_size to width and height so no scaling occurs
                pass

        kwargs["width"] = kwargs.get("width", self.im_size[0])
        kwargs["height"] = kwargs.get("height", self.im_size[1])

        self.merge_config_into_kwargs(kwargs, "image")
        super().__init__(**kwargs)

    @property
    def dpi(self):
        return self._dpi

    @dpi.setter
    def dpi(self, val):
        self._dpi = val
        self.set_svg_im_size()

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, val):
        # Ensure src is either a pathlib.Path or Image instance
        if isinstance(val, Image):
            self._src = val
        else:
            self._src = pathlib.Path(val)

    def set_svg_im_size(self):
        # Extract dimensions from SVG attributes
        tree = ET.parse(self.src)
        root = tree.getroot()
        try:
            width = root.attrib["width"]
            height = root.attrib["height"]
        except KeyError:
            # SVG can omit width and height.
            # Use viewBox dimensions instead.
            width, height = root.attrib["viewBox"].split(" ")[-2:]
        # Dimensions may (or may not) include units
        # re splits at start and end of matched group hence x3 vars
        r = re.compile(r"(^[\d\.]+)")
        _, width, width_units = re.split(r, width)
        _, height, height_units = re.split(r, height)
        # Convert to pixel dimensions
        width = self.to_pixels(width, width_units)
        height = self.to_pixels(height, height_units)
        # Set im_size
        self.im_size = (width, height)

    def to_pixels(self, value, units):

        value = float(value)

        if not units or units.strip().lower() == "px":
            return value

        elif units.strip().lower() == "mm":
            return value / 25.4 * self.dpi

        elif units.strip().lower() == "cm":
            return value / 2.54 * self.dpi

        elif units.strip().lower() == "in":
            return value * self.dpi

        elif units.strip().lower() == "pt":
            return value * 72 * self.dpi

        else:
            warnings.warn(
                f'Image dimension "{units}" is not recognised. Leaving unchanged.'
            )
            return value

    def coord(self, name, raw=False):
        """Return scaled coordinatates."""

        x, y = self.coords[name]

        # Actual image size:
        iw, ih = self.im_size

        # Scale x and y to match user supplied dimensions
        # NOTE: use *_width* and *_height* to ensure actual width and not clipped width
        scaler = min(self._width / iw, self._height / ih)

        # Transformed size
        tw, th = iw * scaler, ih * scaler

        # Transform x and y coords
        tx = x * scaler
        ty = y * scaler

        if not raw:
            # if 'raw' is False translate the coords
            # NOTE: SVG transforms images proportionally to 'fit' supplied dimensions

            # Calculate offset to centre fitted image
            tx = tx + (self._width - tw) / 2
            ty = ty + (self._height - th) / 2

            # rotate coords
            rtx = tx * math.cos(math.radians(self.rotate)) - ty * math.sin(
                math.radians(self.rotate)
            )
            rty = tx * math.sin(math.radians(self.rotate)) + ty * math.cos(
                math.radians(self.rotate)
            )
            tx = rtx + self.x
            ty = rty + self.y

        return Coords(tx, ty)

    def add_coord(self, name, x, y):
        """Record coordinates of the **unscaled** image."""
        self.coords[name] = Coords(x, y)

    def loadData(self):
        """Load image data from URL or local file system."""
        try:
            with open(self.src, "rb") as f:
                return f.read()
        except OSError:
            try:
                with urllib.request.urlopen(self.src) as f:
                    return f.read()
            except urllib.error.HTTPError as e:
                print(e.code)

    def render(self):
        """Render SVG markup either linking or embedding an image."""
        if isinstance(self.src, Image):
            # src image is wrapped in <use> tag which has to replicate 'fitting' behaviour of SVG images
            scaler = min(self._width / self.src._width, self._height / self.src._height)
            self.scale = Coords(
                self.scale.x * scaler,
                self.scale.y * scaler,
            )
            actual_width = self.src._width * scaler
            actual_height = self.src._height * scaler

            tx = (self._width - actual_width) / 2
            ty = (self._height - actual_height) / 2

            # Rotate coords
            rtx = tx * math.cos(math.radians(self.rotate)) - ty * math.sin(
                math.radians(self.rotate)
            )
            rty = tx * math.sin(math.radians(self.rotate)) + ty * math.cos(
                math.radians(self.rotate)
            )

            # clip-path must be a separate component when using <use> to
            # avoid applying scale to clip-path.
            output = Group(clip=self.clip)
            # Reference image from defs with <use> tag
            output.add(
                Use(
                    x=self.x + rtx,
                    y=self.y + rty,
                    scale=self.scale,
                    tag=self.tag,
                    instance=self.src,
                    rotate=self.rotate,
                )
            )

            return output.render()

        # Use externally referenced image
        media_type = pathlib.Path(self.src).suffix[1:]
        tplt = templates.get("image.svg")

        if self.embed:
            if media_type == "svg":
                data = self.loadData()
                # Extract JUST the <svg> markup with no <XML> tag
                tree = ET.fromstring(data)
                self.svg_data = ET.tostring(tree)
            else:
                encoded_img = base64.b64encode(self.loadData())
                # IMPORTANT: bypass Image.src setter function
                self._src = (
                    f"data:image/{media_type};base64,{encoded_img.decode('utf-8')}"
                )
        return tplt.render(image=self)
