import base64
import collections.abc
import copy
import math
from multiprocessing.sharedctypes import Value
import PIL
from PIL import Image as PILImage
import re
import urllib.request
import uuid
import warnings
import xml.etree.ElementTree as ET
import pathlib
from collections import namedtuple
from pinout import manager, templates, config_manager
from pinout import manager_files


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
        self._tag = set()
        super().__init__(**kwargs)

        self.clip = clip

        self.add_tag(tag)
        try:
            # Add config tag(s). These include the default tag
            self.add_tag(self.config["tag"])
        except:
            # No config tag provided
            pass

    @property
    def tag(self):
        # Tags are sorted for consistent ordering on output
        # (required to pass testing)
        return " ".join(sorted([t for t in self._tag]))

    @tag.setter
    def tag(self, tag=None):
        try:
            self._tags = set(tag.split(" "))
        except AttributeError:
            self._tags = set()

    @property
    def clip(self):
        return self._clip

    @clip.setter
    def clip(self, obj):
        if not obj:
            self._clip = None
        elif obj:
            if isinstance(obj, ClipPath):
                self._clip = obj
            else:
                self._clip = ClipPath(children=obj)
        else:
            warnings.warn(f"{obj} is invalid as a clipping path.")

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
        try:
            self._tag.update(tag.split(" "))

        except AttributeError:
            # No tag supplied
            pass

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

    # WARNING: legacy function
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


class Dimensions:
    def __init__(self, x=0, y=0, units=None, **kwargs):
        self.x = self.units_to_px(x, units)
        self.y = self.units_to_px(y, units)

        super().__init__(**kwargs)

    def units_to_px(self, value, units=None, dpi=None):
        dpi = dpi or config_manager.get("diagram.dpi")
        try:
            value, units = [
                token for token in re.split(r"([\d\.-]+)", value, 1) if token
            ]
            value = float(value)
        except TypeError:
            # Value is not at string
            units = units or config_manager.get("diagram.units")

        conversion = {
            "px": value,
            "in": value * dpi,
            "pt": value * dpi / 72,
            "mm": value * dpi / 25.4,
            "cm": value * dpi / 2.54,
        }

        return conversion[units]

    def px_to_units(self, length, units=None, dpi=None):
        units = units or config_manager.get("diagram.units")
        dpi = config_manager.get("diagram.dpi")
        conversion = {
            "px": length,
            "in": length / dpi,
            "pt": length / dpi * 72,
            "mm": length / dpi * 25.4,
            "cm": length / dpi * 2.54,
        }
        return conversion[units]


class Layout(Dimensions, Component, TransformMixin):
    """Base class fundamentally grouping other components together."""

    def __init__(self, children=None, **kwargs):
        self.children = children or []

        super().__init__(**kwargs)

    def add(self, instance):

        # TODO: does clip need adjusting?????
        # if instance.clip:
        #    instance.clip.inherit_dimensions(self)

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
        self.instance = instance
        super().__init__(**kwargs)

    def __getattr__(self, attr):
        # Pass attribute requests onto the instance associated with this 'Use' object
        # This provides some amount of merging with the instance.
        return getattr(self.instance, attr)

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


class SvgShape(Dimensions, Component, TransformMixin):
    """Base class for components that have a graphical representation."""

    def __init__(self, x=0, y=0, width=None, height=None, units=None, **kwargs):
        self.merge_config_into_kwargs(kwargs, "svgshape")
        super().__init__(x=x, y=y, units=units, **kwargs)

        # Width and Height are in user supplied units to this
        # point then converted to px for internal use.
        # Unitless values are processed as same units as diagram
        self._width = self.units_to_px(width, units)
        self._height = self.units_to_px(height, units)

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
        # Default text dimensions to zero if none supplied
        kwargs["width"] = kwargs.get("width", 0)
        kwargs["height"] = kwargs.get("height", 0)
        self.merge_config_into_kwargs(kwargs, "path")
        self._d = None
        super().__init__(**kwargs)

        self.d = path_definition

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, path_definition):
        d_lst = path_definition.split(" ")
        for i, val in enumerate(d_lst):
            try:
                d_lst[i] = str(self.units_to_px(float(val)))

            except ValueError:
                pass  # val is not a number
        self._d = " ".join(d_lst)

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
        self.corner_radius = self.units_to_px(corner_radius)
        self.merge_config_into_kwargs(kwargs, "rect")
        # Default text dimensions to zero if none supplied
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
        self.r = self.units_to_px(r)
        kwargs["x"] = cx
        kwargs["y"] = cy
        self.merge_config_into_kwargs(kwargs, "circle")
        # Default text dimensions to zero if none supplied
        kwargs["width"] = kwargs.get("width", 0)
        kwargs["height"] = kwargs.get("height", 0)
        super().__init__(**kwargs)

    def render(self):
        """Render a <circle> tag."""

        tplt = templates.get("circle.svg")
        return tplt.render(circle=self)


class Text(SvgShape):
    """SVG <text> object"""

    def __init__(self, content, **kwargs):

        self.merge_config_into_kwargs(kwargs, "text")
        # Default text dimensions to zero if none supplied
        kwargs["width"] = kwargs.get("width", 0)
        kwargs["height"] = kwargs.get("height", 0)
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
    def __init__(self, src, embed=False, **kwargs):
        self.merge_config_into_kwargs(kwargs, "image")
        self.coords = kwargs.pop("coords", {})
        self.embed = embed
        self.src = src
        self.im_size = None
        super().__init__(**kwargs)

        self.get_im_size()

    def get_im_size(self):
        if isinstance(self.src, Image):
            self.im_size = self.src.im_size
        else:
            if pathlib.Path(self.src).suffix == ".svg":
                self.get_svg_im_size()
            else:
                self.get_bitmap_im_size()

    def get_bitmap_im_size(self):
        cwd = pathlib.Path.cwd()
        im = PILImage.open(cwd / self.src)
        width, height = im.size
        self.im_size = (self.px_to_units(width), self.px_to_units(height))

    def get_svg_im_size(self):
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

        # Set im_size
        self.im_size = (float(width), float(height))

    @property
    def width(self):
        if self.clip:
            return self.clip.width

        return self._width or self.im_size[0]

    @property
    def height(self):
        if self.clip:
            return self.clip.height

        return self._height or self.im_size[1]

    def coord(self, name, raw=False):
        """Return scaled coordinatates."""

        try:
            x, y = self.coords[name]
        except KeyError:
            x, y = self.src.coord(name)

        # Actual image size:
        iw, ih = self.im_size

        # Scale x and y to match user supplied dimensions
        # NOTE: use *_width* and *_height* to ensure actual width and not clipped width
        width = self._width or self.im_size[0]
        height = self._height or self.im_size[1]
        scaler = min(width / iw, height / ih)

        # Transformed size
        tw, th = iw * scaler, ih * scaler

        # Transform x and y coords
        tx = x * scaler
        ty = y * scaler

        if not raw:
            # if 'raw' is False translate the coords
            # NOTE: SVG transforms images proportionally to 'fit' supplied dimensions

            # Calculate offset to centre fitted image
            tx = tx + (width - tw) / 2
            ty = ty + (height - th) / 2

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

    def render_image_def(self):
        # src image is wrapped in <use> tag which has
        # to replicate 'fitting' behaviour of SVG images
        #
        # clip-path must be a separate component when using <use> to
        # avoid applying scale to clip-path.
        output = Group(clip=self.clip)

        # Remove clip from Image instance now it is applied to output
        # This makes calculations easier too :)
        self.clip = []

        scaler = min(self.width / self.src.width, self.height / self.src.height)
        self.scale = Coords(
            self.scale.x * scaler,
            self.scale.y * scaler,
        )
        actual_width = self.src.width * scaler
        actual_height = self.src.height * scaler

        tx = (self.width - actual_width) / 2
        ty = (self.height - actual_height) / 2

        # Rotate coords
        rtx = tx * math.cos(math.radians(self.rotate)) - ty * math.sin(
            math.radians(self.rotate)
        )
        rty = tx * math.sin(math.radians(self.rotate)) + ty * math.cos(
            math.radians(self.rotate)
        )

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

    def render(self):
        if isinstance(self.src, Image):
            return self.render_image_def()

        # Use externally referenced image
        tplt = templates.get("image.svg")

        if self.embed:
            encoded_img = base64.b64encode(manager_files.load_data(self.src))
            mediatype = "image/" + pathlib.Path(self.src).suffix.strip(".")
            if mediatype.endswith("svg"):
                mediatype += "+xml"
            self.src = f"data:{mediatype};base64,{encoded_img.decode('utf-8')}"
        return tplt.render(image=self)
