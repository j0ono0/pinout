import copy
from . import file_manager
from .templates import svg_group
from .elements import Element, SVG, Coords, BoundingBox, BoundingCoords
from . import elements as elem


class Component(SVG):
    """Container object that manages child Components and/or Elements as a group.

    :param children: Components and/or elements, defaults to None
    :type children: SVG subtypes, optional
    """

    conf = {}

    def __init__(self, children=None, *args, **kwargs):
        """[summary]"""
        self.children = []
        super().__init__(*args, **kwargs)

    @property
    def bounding_coords(self):
        """Coordinates of the components's bounding rectangle.

        :return: (x_min, y_min, x_max, y_max)
        :rtype: BoundingCoords (namedtuple)
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
            min((self.x + x_min) * self.scale.x, (self.x + x_max) * self.scale.x),
            min((self.y + y_min) * self.scale.y, (self.y + y_max) * self.scale.y),
            max((self.x + x_min) * self.scale.x, (self.x + x_max) * self.scale.x),
            max((self.y + y_min) * self.scale.y, (self.y + y_max) * self.scale.y),
        )

    @property
    def bounding_rect(self):
        """Components's coordinates and size.

        :return: (x, y, width, height)
        :rtype: BoundingBox (namedtuple)
        """
        x_min, y_min, x_max, y_max = self.bounding_coords
        return BoundingBox(x_min, y_min, x_max - x_min, y_max - y_min)

    @property
    def width(self):
        """Calculated width that encompasses all child elements

        :return: value representing width in pixels
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

        :return: value representing height in pixels
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
        """See :func:`~pinout.elements.SVG.scale`"""
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        for child in self.children:
            if issubclass(type(child), Element):
                child.scale = self.scale

    def add(self, cls, *args, **kwargs):
        """Instantiate a class and add it to the components children."""

        # Do any pre-process on args before instantiation.

        instance = cls(*args, **kwargs)
        self.children.append(instance)
        return instance

    def patch_config(self, source, patch):
        """Recursively update source with patch dict items."""
        try:
            for key, val in patch.items():
                if type(val) == dict:
                    source.setdefault(key, {})
                    self.patch_config(source[key], patch[key])
                else:
                    source[key] = val
        except KeyError:
            # patch has no items
            pass
        return source

    def render(self):
        """Render Component, and children, as SVG markup.

        :return: SVG markup of component including all children.
        :rtype: str
        """
        output = ""
        for child in self.children:
            output += child.render()
        return svg_group.render(
            x=self.x,
            y=self.y,
            tag=self.tag,
            content=output,
            scale=self.scale,
        )


class PinLabelSet(Component):
    """Add rows of PinLabels to a 'header' of pins

    :param offset: Offset of the first PinLabelRow from the origin
    :type offset: (x, y) tuple
    :param labels: List of PinLabelRows
    :type labels: List
    :param pitch: Offset between each PinLabelRow, defaults to (1, 1)
    :type pitch: (x, y) tuple, optional
    """

    def __init__(self, offset, labels, pitch=(1, 1), *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Extract scale and update x and y of pinlabelset instance
        offset, self.scale = self.extract_scale(offset)
        self.x = self.x * self.scale.x
        self.y = self.y * self.scale.y

        pitch = Coords(*pitch)

        # Create a Component for each row in 'labels'
        for i, label_list in enumerate(labels):
            pin_x = pitch.x * i * self.scale.x
            pin_y = pitch.y * i * self.scale.y

            if pitch[1] == 0:
                # Horizontal pinset require label_rows to offset vertically
                offset = Coords(offset.x - pin_x, offset.y + abs(pin_x))

            row = self.add(
                Component,
                x=pin_x + offset.x,
                y=pin_y + offset.y,
            )

            # Create a leaderline
            leaderline_config = copy.deepcopy(self.cfg["leaderline"])
            vertical_move = f"V {offset.y}" if offset.y != 0 else ""
            horizontal_move = (
                f"H {offset.x + pitch.x * i * self.scale.x}" if offset.x != 0 else ""
            )

            definition = f"M {pin_x} {pin_y} {vertical_move} {horizontal_move}"

            leaderline = self.add(
                elem.Path,
                definition=definition,
                config=leaderline_config,
            )

            # Add labels to row
            for j, label in enumerate(label_list):
                label = dict(zip(("text_content", "tag", "config"), label))

                # Copy config and patch with supplied config
                label_config = copy.deepcopy(self.cfg)
                self.patch_config(label_config, label.get("config", {}))
                # Patch config with tag styles
                tag_color = Component.conf["tags"][label["tag"]]["color"]
                self.patch_config(
                    label_config,
                    {
                        "label": {"rect": {"fill": tag_color}},
                        "leaderline": {"stroke": tag_color},
                    },
                )

                # Match leaderline to first label tag color
                if j == 0:
                    leaderline.cfg["stroke"] = tag_color

                # add label's leaderline
                label_offset = Coords(*label_config["offset"])
                self.patch_config(
                    label_config,
                    {"leaderline": {"stroke": tag_color}},
                )
                definition = f"M {row.width} 0 h {label_offset.x}"
                row.add(
                    elem.Path,
                    x=row.width,
                    y=0,
                    width=label_offset.x,
                    height=self.cfg["leaderline"]["stroke_width"],
                    scale=self.scale,
                    definition=definition,
                    config=label_config["leaderline"],
                )

                row.add(
                    elem.Label,
                    text_content=label["text_content"],
                    x=row.width,
                    y=-label_config["label"]["rect"]["height"] / 2,
                    width=label_config["label"]["rect"]["width"],
                    height=label_config["label"]["rect"]["height"],
                    scale=self.scale,
                    config=label_config["label"],
                )


class Legend(Component):
    """Provide a colour coded legend to describe pin labels.

    :param categories: List of tags to include in legend
    :type categories: [<tag1>, <tag2>, ...] List
    """

    def __init__(self, categories, *args, **kwargs):
        """[summary]"""
        super().__init__(*args, **kwargs)

        pad = Coords(*self.cfg["padding"])
        row_height = self.cfg["row_height"]
        swatch_size = row_height * 2 / 3
        categories = categories or self.conf["tags"].keys()
        for i, tag in enumerate(categories):
            entry = self.add(
                Component, x=pad.x, y=pad.y + row_height * i, tag=self.cfg["tag"]
            )
            entry.add(
                elem.Text,
                self.conf["tags"][tag]["title"],
                x=swatch_size * 2,
                y=0,
                width=self.cfg["rect"]["width"],
                height=row_height,
                config=self.cfg["text"],
            )

            # Create icon based on pinlabel config
            pinlabel_config = copy.deepcopy(self.conf["pinlabel"])
            tag_color = self.conf["tags"][tag]["color"]
            pinlabel_patch = {
                "offset": (-swatch_size / 2, 0),
                "label": {
                    "rect": {
                        "fill": tag_color,
                        "height": swatch_size,
                        "width": swatch_size,
                        "rx": pinlabel_config["label"]["rect"]["rx"],
                    },
                },
                "leaderline": {
                    "stroke": tag_color,
                },
            }
            self.patch_config(pinlabel_config, pinlabel_patch)

            entry.add(
                elem.Rect,
                x=0,
                y=-pinlabel_config["label"]["rect"]["height"] / 2
                - self.cfg["text"]["size"] / 2,
                width=swatch_size,
                height=swatch_size,
                config=pinlabel_config["label"]["rect"],
            )

            definition = f"M {swatch_size} {-pinlabel_config['label']['text']['size'] / 2} h {swatch_size/2}"
            entry.add(
                elem.Path,
                definition=definition,
                x=swatch_size,
                y=-pinlabel_config["label"]["text"]["size"] / 2,
                width=swatch_size / 2,
                height=pinlabel_config["leaderline"]["stroke_width"],
                config=pinlabel_config["leaderline"],
            )

        # Add an panel *behind* component
        self.cfg["rect"]["height"] = row_height * len(categories) + pad.y
        self.children.insert(
            0,
            elem.Rect(
                x=0,
                y=0,
                width=self.cfg["rect"]["width"],
                height=self.cfg["rect"]["height"],
                scale=self.scale,
                config=self.cfg["rect"],
            ),
        )


class Annotation(Component):
    def __init__(self, text_content, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Extract scale from offset and update x and y
        offset, self.scale = self.extract_scale(self.cfg["offset"])
        self.x = self.x * self.scale.x
        self.y = self.y * self.scale.y

        label_padding = Coords(*self.cfg["label"]["padding"])

        # Attempt to split on '\n' and convert to list
        if type(text_content) == str:
            text_content = text_content.split("\n")

        # Calculate label dimensions
        line_height = self.cfg["label"]["text"]["line_height"]
        font_height = self.cfg["label"]["text"]["size"]
        top_padding = label_padding.y - (line_height - font_height)
        label_height = (
            len(text_content) * self.cfg["label"]["text"]["line_height"]
            + label_padding.y
            + top_padding
        )
        self.cfg["label"]["rect"]["height"] = label_height

        # Annotation label
        label = Component(
            tag="anno_label",
            x=offset.x,
            y=offset.y,
        )
        self.children.append(label)

        # Add background rect to label
        rect_y = 0 if self.scale.y == -1 else -label_height
        label.add(
            elem.Rect,
            y=rect_y,
            width=self.cfg["label"]["rect"]["width"],
            height=self.cfg["label"]["rect"]["height"],
            config=self.cfg["label"]["rect"],
        )

        # Add textblock to label
        tb_x = label_padding.x
        if self.scale.x == -1:
            tb_x -= self.cfg["label"]["rect"]["width"]

        tb_y = -self.cfg["label"]["rect"]["height"] + top_padding

        label.add(
            elem.TextBlock,
            text_content,
            x=tb_x,
            y=tb_y,
            width=self.cfg["label"]["rect"]["width"] - label_padding.x * 2,
            height=self.cfg["label"]["rect"]["height"],
            config=self.cfg["label"],
            scale=self.scale,
        )

        # Leaderline
        # leaderline rect
        leaderline_rect = self.add(
            elem.Rect,
            x=-self.cfg["leaderline"]["rect"]["width"] / 2,
            y=-self.cfg["leaderline"]["rect"]["height"] / 2,
            width=self.cfg["leaderline"]["rect"]["width"],
            height=self.cfg["leaderline"]["rect"]["height"],
            config=self.cfg["leaderline"]["rect"],
        )

        # leaderline start location at edge of leaderline_rect
        start_y = 0
        start_x = 0
        if offset.y > leaderline_rect.height / 2:
            start_y = leaderline_rect.height / 2
        elif -leaderline_rect.height / 2 < offset.y < leaderline_rect.height / 2:
            start_x = leaderline_rect.width / 2

        # leaderline path
        vertical_move = f"V {offset.y}" if offset.y != 0 else ""
        horizontal_move = f"H {offset.x + label.width}" if offset.x != 0 else ""

        path_definition = f"M {start_x} {start_y} {vertical_move} {horizontal_move}"

        self.add(elem.Path, path_definition, config=self.cfg["leaderline"])
