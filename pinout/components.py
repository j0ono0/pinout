import base64
from collections import namedtuple
from pathlib import Path
from . import file_manager

from .templates import (
    svg_group,
    svg_image,
    svg_label,
    svg_line,
    svg_rect,
    svg_style,
    svg_text,
)

BoundingBox = namedtuple("BoundingBox", ("x y w h"))
BoundingCoords = namedtuple("BoundingCoords", ("x_min y_min x_max y_max"))
Coords = namedtuple("Coords", ("x y"))


#####################################################################
# Base Element and Component classes


class ClassMethodMissing(Exception):
    """ An element is missing an expected method """

    pass


class SVG:
    def __init__(self, x=0, y=0, scale=(1, 1), rotation=0, tags=""):
        self.x = x
        self.y = y
        self._scale = scale if isinstance(scale, Coords) else Coords(*scale)
        self.rotation = rotation
        self.tags = tags

    @property
    def scale(self):
        """Scale is abstracted as a property here and overridden by Component

        :return: (x, y) where x and y are either 1 or -1
        :rtype: tuple
        """
        return self._scale

    @scale.setter
    def scale(self, value):
        """Scale setter property - overridden by Component

        :param value: (x, y) where x and y are either 1 or -1
        :type value: tuple
        """
        self._scale = value

    def extract_scale(self, coords):
        """Separate scale information from a tuple that represents (x, y) or (width, height) values. Components and elements control orientation via the scale property rather than negative dimension/direction values. **NOTE**: Existing scale property is only overridded if the provided coords include a negative value.

        :param coords: tuple representing  (x, y) or (width, height). values may be positive or negative.
        :type coords: Union(tuple, Coords)
        :return: nametuple with absolute values
        :rtype: Coords
        """

        if not all(val >= 0 for val in coords):
            self.scale = Coords(*[i / abs(i) if i != 0 else 1 for i in coords])
        return Coords(*[abs(i) for i in coords])


class Element(SVG):
    """Container that exclusively handles graphical SVG code. Elements can be considered the smallest building blocks of *pinout*.

    :param width: Width of the renderable SVG code, defaults to 0
    :type width: int, optional
    :param height: Height of the renderable SVG code, defaults to 0
    :type height: int, optional
    """

    def __init__(self, width=0, height=0, *args, **kwargs):
        self.width = width
        self.height = height
        super().__init__(*args, **kwargs)

    @property
    def bounding_coords(self):
        """Coordinates, relative to its parent, representing sides of a rectangle that encompass the rendered element.

        :return: (x_min, y_min, x_max, y_max)
        :rtype: tuple
        """
        x_min, x_max = sorted(
            [self.x * self.scale.x, (self.x + self.width) * self.scale.x]
        )
        y_min, y_max = sorted(
            [self.y * self.scale.y, (self.y + self.height) * self.scale.y]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

    @property
    def bounding_rect(self):
        """Coordinates representing the location of an elements origin (usually top-left corner) within its parent along with the elements width and height.

        :return: (x, y, width, height)
        :rtype: tuple
        """
        x_min, y_min, x_max, y_max = self.bounding_coords
        return BoundingBox(x_min, y_min, x_max - x_min, y_max - y_min)

    def render(self):
        raise ClassMethodMissing(f"{self} requires a 'render' method.")


class Component(SVG):
    """Container object that manages child Components and/or Elements as a group.

    Child coordinates are all relative to their parent Component.

    When scale is applied to a Component no direct affect to the <group> tag is applied but the scale setting is passed down to direct child **Elements**.

    :param children: Component and/or Element objects, defaults to None
    :type children: Union[Component, Element, StyleSheet], optional
    :param config: Default configuration values.
    :type config: dict, optional
    """

    def __init__(self, children=None, config=None, *args, **kwargs):

        self.cfg = config
        self.children = []
        super().__init__(*args, **kwargs)
        if children:
            self.add(children)

    @property
    def bounding_coords(self):
        """Coordinates, relative to its parent, representing sides of a rectangle that encompass all child elements of the rendered Component.

        :return: (x_min, y_min, x_max, y_max)
        :rtype: tuple
        """
        # Untransformed bounding coords
        x_min = y_min = x_max = y_max = 0
        for child in self.children:
            try:
                child_coords = child.bounding_coords
                x_min = min(x_min, child_coords.x_min)
                y_min = min(y_min, child_coords.y_min)
                x_max = max(x_max, child_coords.x_max)
                y_max = max(y_max, child_coords.y_max)
            except AttributeError:
                # The child has no bounding_coords.
                pass
        return BoundingCoords(
            self.x + x_min, self.y + y_min, self.x + x_max, self.y + y_max
        )

    @property
    def width(self):
        """Calculated width that encompasses all child elements

        :return: value representing a width in pixels
        :rtype: int
        """
        try:
            x_min, y_min, x_max, y_max = self.bounding_coords
            return x_max - x_min
        except ValueError:
            # Component has no children with bounding_coords
            return 0

    @property
    def height(self):
        """Calculated height that encompasses all child elements

        :return: value representing a height in pixels
        :rtype: int
        """
        try:
            x_min, y_min, x_max, y_max = self.bounding_coords
            return y_max - y_min
        except ValueError:
            # Component has no children with bounding_coords
            return 0

    @property
    def scale(self):
        """Scale has no direct effect of components however all immediate element children of a component inherit their parents scale value.

        :return: tuple in the form of (x, y) where expected values are either 1 or -1.
        :rtype: tuple
        """
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        for child in self.children:
            if issubclass(type(child), Element):
                child.scale = self.scale

    @property
    def bounding_rect(self):
        """Coordinates representing the location of a components origin (usually top-left corner) within its parent along with a width and height that encompass all child elements.

        :return: (x, y, width, height)
        :rtype: tuple
        """
        x_min, y_min, x_max, y_max = self.bounding_coords
        return BoundingBox(x_min, y_min, x_max - x_min, y_max - y_min)

    def add_and_instantiate(self, cls, *args, **kwargs):
        """Instantiate an instance of a class and add it to the components children. This is done as a method to allow attributes to be added/amended in the single process.

        :return: Instance of the instantiated class
        :rtype: object
        """
        if issubclass(cls, Component):
            kwargs["config"] = self.cfg
        if issubclass(cls, Element):
            kwargs["scale"] = self.scale
        instance = cls(*args, **kwargs)
        self.children.append(instance)
        return instance

    def render(self):
        """Render Component, and children, as SVG markup.
        NOTE: *scale* only affects Elements! It does not affect the grapical appearance of Components.

        :return: SVG markup of component including all children.
        :rtype: str
        """
        output = ""
        for child in self.children:
            output += child.render()
        return svg_group.render(
            x=self.x,
            y=self.y,
            tags=self.tags,
            content=output,
            # NOTE: Graphically, components are *not* affected by scale
            scale=Coords(1, 1),
        )


class StyleSheet:
    def __init__(self, path, embed=False, config=None):
        """Include a stylesheet in the diagram

        :param path: Filename, including path, of the external stylesheet. *NOTE*: If *embedding*, a relative path is relative to the current working directory. If *linking*, a relative path is relative to the location of the final SVG diagram.
        :type path: str
        :param embed: Elect to link or embed the stylesheet, defaults to False
        :type embed: bool, optional
        """
        self.path = path
        self.embed = embed
        self.cfg = config

    def render(self):
        """Create SVG tag with content to either embed or link styles.

        :return: SVG <link> or <style> code
        :rtype: string
        """
        context = {}
        if self.embed:
            p = Path(self.path)
            context["css_data"] = p.read_text()
        else:
            context["path"] = self.path

        return svg_style.render(**context)


#####################################################################
# SVG tag classes


class Image(Element):
    def __init__(self, href, embed=False, *args, **kwargs):
        """Associate a PNG, JPG or SVG formatted image to the diagram. *IMPORTANT*: Image width and height parameters must be supplied for the image to display! *pinout* does not auto-detect these attributes.

        :param href: Location of the image. *Note*: Where :code:`embed=False` the path is relative to the exported file. Where :code:`embed=True` the path is relative to the current working directory.
        :type path: string
        :param embed: Embed or link the image in the exported file, defaults to False
        :type embed: bool, optional
        """
        super().__init__(*args, **kwargs)

        self.href = href
        self.embed = embed

    @property
    def bounding_coords(self):
        """Coordinates, relative to its parent, representing sides of a rectangle that encompass the image.

        :return: (x_min, y_min, x_max, y_max)
        :rtype: tuple
        """
        x_min, x_max = sorted(
            [self.x * self.scale.x, (self.x + self.width) * self.scale.x]
        )
        y_min, y_max = sorted(
            [self.y * self.scale.y, (self.y + self.height) * self.scale.y]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

    def render(self):
        """Generates SVG <image> tag using the image 'filename', Note that JPG and PNG are the only binary images files officially supported by the SVG format. If 'embed' is True the image is assigned to the path as a data URI. JPG and PNG image are base64 encoded, SVG files included verbatim. Otherwise the path 'src' is assigned 'filename'. Note: 'filename' includes the path to the file. Where a relative path is used it must be relative to the **exported file**.

        :return: SVG <image> component
        :rtype: str
        """
        media_type = Path(self.href).suffix[1:]
        path = Path(self.href)
        if self.embed:
            if media_type == "svg":
                with path.open() as f:
                    svg_data = f.read()
                return svg_group.render(x=self.x, y=self.y, content=svg_data)
            else:
                encoded_img = base64.b64encode(open(self.href, "rb").read())
                path = f"data:image/{media_type};base64,{encoded_img.decode('utf-8')}"

        return svg_image.render(
            x=self.x, y=self.y, width=self.width, height=self.height, href=path
        )


class Rect(Element):
    """SVG <rect> (rectangle) element.

    :param rx: corner radius, defaults to 0
    :type rx: int, optional
    """

    def __init__(self, rx=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rx = rx

    def render(self):
        """create an SVG <rect> tag.

        :return: SVG <rect> code
        :rtype: string
        """
        return svg_rect.render(
            rx=self.rx,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            scale=self.scale,
            tags=self.tags,
        )


class Line(Element):
    """Create an SVG <path> tag with (at most) a single 90deg bend in it. The design of this Element is soley for use as a leader line with pin labels.

    :return: SVG <path> code
    :rtype: string
    """

    def render(self):
        """create an SVG <path> tag.

        :return: SVG <path> code
        :rtype: string
        """
        vertical_move = f"V {self.height}" if self.height != 0 else ""
        horizontal_move = f"H {self.width}" if self.width != 0 else ""
        return svg_line.render(
            d=f"M 0 0 {vertical_move} {horizontal_move}",
            scale=self.scale,
            tags=self.tags,
        )


class Text(Element):
    """Create an SVG <text> tag with a single line of text.

    :return: SVG <text> code
    :rtype: string
    """

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text

    def render(self):
        """create an SVG <text> tag.

        :return: SVG <text> code
        :rtype: string
        """
        return svg_text.render(
            text=self.text,
            tags=("textblock " + self.tags).strip(),
            x=self.x,
            y=self.y,
            scale=self.scale,
        )


#####################################################################
# Composite classes


class Label(Element):
    """A single line of text infront of a rectangle. *Note*: Text length is not auto-detected and the element's width should be set to ensure text will not overflow the rectangle in the final diagram export.

    :param text: Text to appear on the label
    :type text: string
    """

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text

    def render(self):
        """create an SVG <group> tag that includes text and an rectangle.

        :return: SVG <group> code
        :rtype: string
        """
        return svg_label.render(
            text=self.text,
            tags=self.tags,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            scale=self.scale,
        )


class LeaderLine(Component):
    """Draws a line from *offset* to the component's (x, y) location.

    :param offset: The (x, y) coordinates the leaderline is drawn from
    :type offset: tuple
    """

    def __init__(self, offset=(0, 0), *args, **kwargs):

        super().__init__(*args, **kwargs)
        cfg_tag = self.cfg.get("leaderline", {}).get("tag", "")
        self.tags = " ".join([cfg_tag, self.tags]).strip()

        offset = self.extract_scale(offset)

        # Add Path to children
        self.add_and_instantiate(
            Line,
            width=abs(offset[0]),
            height=abs(offset[1]),
        )


class PinLabel(Component):
    """Comprised of a Line and Label element, this component encapsulates the requirement for a single pin label. All arguments have default settings in the components config.

    :param text: Text displayed in the label
    :type text: string
    :param offset: x and y distance that the label is offset from its parent. A leader line graphically bridges from the parent origin to the the offset coords.
    :type offset: (tuple)
    :param box_width: Width of the label portion of the PinLabel. Total width is box_width + offset.x
    :type box_width: int
    :param box_height: Height of the label portion of the PinLabel.
    :type box_height: int
    """

    def __init__(
        self,
        text,
        offset=None,
        box_width=None,
        box_height=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # Assign config values if none supplied
        offset = offset or self.cfg["pinlabel"]["box"]["offset"]
        box_width = box_width or self.cfg["pinlabel"]["box"]["width"]
        box_height = box_height or self.cfg["pinlabel"]["box"]["height"]

        # Merge additional tags with config tags
        cfg_tag = self.cfg.get("pinlabel", {}).get("tag", "")
        self.tags = " ".join([cfg_tag, self.tags]).strip()
        # Separate offset and scale data
        offset = self.extract_scale(offset)

        self.add_and_instantiate(Line, width=offset.x, height=offset.y)
        self.add_and_instantiate(
            Label,
            text=text,
            x=offset.x - 1,
            y=offset.y,
            width=box_width,
            height=box_height,
            scale=self.scale,
        )


class PinLabelRow(Component):
    """Assists with grouping and arranging pinlabels that relate to the same pin into a row.

    :param offset: x and y distance that the row is offset from its parent. A leader line graphically bridges from the parent origin to the the offset coords.
    :type offset: tuple in the form of (x, y)
    :param labels: List of tuples documenting label attributes ("text", "tags", "offset", "box_width"). Only 'text' and 'tag' are required. The other optional values fallback to config defaults. :code:`offset=None` can be used to supply a 'box_width' but use the default 'offset' value.
    :type labels: List of tuples
    """

    def __init__(self, offset, labels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = self.extract_scale(offset)
        self.labels = self.add_and_instantiate(
            Component, x=offset[0], y=offset[1], scale=self.scale
        )

        cfg_tag = self.cfg.get("pinlabelrow", {}).get("tag", "")
        self.tags = (cfg_tag + self.tags).strip()

        self.add_labels(labels)

    def add_labels(self, label_list):
        for i, label in enumerate(label_list):
            context = dict(zip(("text", "tags", "offset", "box_width"), label))
            # Remove 'na' entries - they fall-back to default settings
            context = {
                key: val
                for key, val in context.items()
                if val not in [None, "auto", "default", "", "-", "na"]
            }

            # Conditionally set offset if none supplied (first label has no leaderline)
            if i == 0:
                context["offset"] = context.get("offset", (0, 0))

            # Add PinLabel to label_row
            label_x = self.labels.width * self.scale.x
            self.labels.add_and_instantiate(
                PinLabel, **context, x=label_x, scale=self.scale
            )

    def render(self):
        """Prior to rendering, a leaderline is automatically added, joining the first label to the components origin.

        :return: SVG <group> containing a row of pin labels
        :rtype: string
        """

        tags = self.labels.children[0].tags.split(" ")
        tags.remove(self.cfg.get("pinlabel", {}).get("tag", ""))
        tag_str = " ".join(tags)

        self.add_and_instantiate(
            LeaderLine,
            offset=self.offset,
            tags=tag_str,
            scale=self.scale,
            config=self.cfg,
        )
        return super().render()


class PinLabelSet(Component):
    """This is the recommended method of adding pin labels to a diagram.
    :param offset: Relative x and y offset from the pin location for the first label in a row
    :type offset: tuple
    :param labels: tuples nested within a 2 dimensional array. Each list within the 'labels' list represents a pin in the header. Each entry within those lists becomes a label.
    :type labels: Tuples nested within a 2 dimensional array. Each list within 'labels' represents a pin in the header. Each entry within those lists becomes a label. The label is a tuple in the format :code:`(<text>, <css tag>, <offset>, <box_width>)` the second two arguments are optional.
    :param pitch: 'x' and 'y' distance in pixels between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. (30, 0) creates a horizontal header. (-30, 0) creates a horizontal header in the reverse direction. This can be useful for 'stacking' rows in reversed order to avoid leader-lines overlapping.
    :type pitch: tuple, optional
    """

    def __init__(self, offset, labels, pitch=(1, 1), *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a Component for each row in 'labels'
        for i, label_list in enumerate(labels):
            pin_x = pitch[0] * i
            pin_y = pitch[1] * i
            if pitch[1] == 0:
                # Horizontal pinset
                row_offset = (offset[0] - pin_x, offset[1] + abs(pin_x))
            else:
                row_offset = offset

            label_row = self.add_and_instantiate(
                PinLabelRow, offset=row_offset, labels=label_list, x=pin_x, y=pin_y
            )


class Legend(Component):
    """Provide a colour coded legend to describe pin labels. All data to populate a legend must be documented in the diagram's config by adding an YAML formatted file::

        # config.yaml

        legend:
            categories: [
                # [<Title>, <CSS class 'tag'>]
                ["Analog", "analog"],
                ["GPIO", "gpio"],
                ["PWM", "pwm"],
            ]

    *Note*: *pinout* does not calculate text widths. a manually provided with should be included to ensure text remains enclosed within the legend.

    A complete set of *pinout* defaults can be duplicated from the command line for reference::

            >>> py -m pinout.file_manager --duplicate config

    config.yaml includes all legend attributes that can be altered.

    """

    def __init__(
        self,
        categories=None,
        row_height=None,
        padding=None,
        width=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        row_height = row_height or self.cfg["legend"]["row_height"]
        categories = categories or self.cfg["legend"]["categories"]
        width = width or self.cfg["legend"]["width"]

        # Padding fallbacks: arg > config > calculated
        padding = (
            padding
            if padding != None
            else self.cfg.get("legend", {}).get(
                "padding",
                [
                    row_height / 2,
                    row_height * 4 / 5,
                ],
            )
        )

        pad = Coords(*padding)
        swatch_size = row_height * 2 / 3

        for i, (name, tags) in enumerate(categories):
            entry = self.add_and_instantiate(
                Component, x=pad.x, y=pad.y + row_height * i, tags=tags
            )
            entry.add_and_instantiate(
                Text, text=name, x=swatch_size * 2, height=row_height
            )
            entry.add_and_instantiate(
                PinLabel,
                box_height=swatch_size,
                box_width=swatch_size,
                config=self.cfg,
                offset=(-swatch_size / 2, 0),
                tags=tags,
                text="",
                x=swatch_size * 1.5,
            )

        # Add an 'information panel' *behind* component
        cfg_tag = self.cfg.get("informationpanel", {}).get("tag")
        self.children.insert(
            0,
            Rect(
                width=width,
                height=self.height + pad.y - row_height,
                tags=cfg_tag,
                scale=self.scale,
            ),
        )
