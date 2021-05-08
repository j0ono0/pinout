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

    config = {}

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

        x_min, x_max = sorted(
            [(self.x + x_min) * self.scale.x, (self.x + x_max) * self.scale.x]
        )
        y_min, y_max = sorted(
            [(self.y + y_min) * self.scale.y, (self.y + y_max) * self.scale.y]
        )
        return BoundingCoords(x_min, y_min, x_max, y_max)

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

    def add(self, instance):
        """Add an instance to the component's children.

        :param instance: Component or Element
        :type instance: Component or Element
        :return: instance attribute
        :rtype: Component or Element
        """
        self.children.append(instance)
        return instance

    @staticmethod
    def patch_config(source, patch):
        """Recursively update source with patch dict items."""
        try:
            for key, val in patch.items():
                if type(val) == dict:
                    source.setdefault(key, {})
                    Component.patch_config(source[key], patch[key])
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
            row_offset = offset
            if pitch[1] == 0:
                # Horizontal pinset require label_rows to offset vertically
                row_offset = Coords(offset.x - pin_x, offset.y + abs(pin_x))

            row = self.add(
                Component(
                    x=pin_x + row_offset.x,
                    y=pin_y + row_offset.y,
                )
            )

            # Create a leaderline
            leaderline_config = copy.deepcopy(self.config["leaderline"])
            vertical_move = f"V {row_offset.y}" if row_offset.y != 0 else ""
            horizontal_move = (
                f"H {row_offset.x + pitch.x * i * self.scale.x}"
                if row_offset.x != 0
                else ""
            )

            definition = f"M {pin_x} {pin_y} {vertical_move} {horizontal_move}"

            leaderline = self.add(
                elem.Path(
                    definition=definition,
                    config=leaderline_config,
                )
            )

            # Add labels to row
            for j, label in enumerate(label_list):
                label = dict(zip(("text_content", "tag", "config"), label))

                # Copy config and patch with supplied config
                label_config = copy.deepcopy(self.config)
                self.patch_config(label_config, label.get("config", {}))
                # Patch config with tag styles
                tag_color = Component.config["tags"][label["tag"]]["color"]
                self.patch_config(
                    label_config,
                    {
                        "label": {"rect": {"fill": tag_color}},
                        "leaderline": {"stroke": tag_color},
                    },
                )

                # Match leaderline to first label tag color
                if j == 0:
                    leaderline.config["stroke"] = tag_color

                # add label's leaderline
                label_offset = Coords(*label_config["offset"])
                self.patch_config(
                    label_config,
                    {"leaderline": {"stroke": tag_color}},
                )
                definition = f"M {row.width} 0 h {label_offset.x}"
                row.add(
                    elem.Path(
                        x=row.width,
                        y=0,
                        width=label_offset.x,
                        height=self.config["leaderline"]["stroke_width"],
                        scale=self.scale,
                        definition=definition,
                        config=label_config["leaderline"],
                    )
                )

                row.add(
                    elem.Label(
                        text_content=label["text_content"],
                        x=row.width,
                        y=-label_config["label"]["rect"]["height"] / 2,
                        width=label_config["label"]["rect"]["width"],
                        height=label_config["label"]["rect"]["height"],
                        scale=self.scale,
                        config=label_config["label"],
                    )
                )


class Legend(Component):
    """Provide a colour coded legend to describe pin labels.

    :param categories: List of tags to include in legend
    :type categories: [<tag1>, <tag2>, ...] List
    """

    def __init__(self, categories, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # NOTE: pad.y sets the text **baseline**
        pad = Coords(*self.config["padding"])
        row_height = self.config["row_height"]
        swatch_size = row_height * 2 / 3
        categories = categories or Component.config["tags"].keys()
        for i, tag in enumerate(categories):
            entry = self.add(
                Component(x=pad.x, y=pad.y + row_height * i, tag=self.config["tag"])
            )
            entry.add(
                elem.Text(
                    Component.config["tags"][tag]["title"],
                    x=swatch_size * 2,
                    y=0,
                    width=self.config["rect"]["width"],
                    height=row_height,
                    config=self.config["text"],
                )
            )

            # Create icon based on pinlabel config
            pinlabel_config = copy.deepcopy(Component.config["pinlabel"])
            tag_color = Component.config["tags"][tag]["color"]
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
                elem.Rect(
                    x=0,
                    y=-pinlabel_config["label"]["rect"]["height"] / 2
                    - self.config["text"]["size"] / 2,
                    width=swatch_size,
                    height=swatch_size,
                    config=pinlabel_config["label"]["rect"],
                )
            )

            definition = f"M {swatch_size} {-pinlabel_config['label']['text']['size'] / 2} h {swatch_size/2}"
            entry.add(
                elem.Path(
                    definition=definition,
                    x=swatch_size,
                    y=-pinlabel_config["label"]["text"]["size"] / 2,
                    width=swatch_size / 2,
                    height=pinlabel_config["leaderline"]["stroke_width"],
                    config=pinlabel_config["leaderline"],
                )
            )

        # Add an panel *behind* component
        self.config["rect"]["height"] = (
            row_height * len(categories) + pad.y - self.config["text"]["size"]
        )
        self.children.insert(
            0,
            elem.Rect(
                x=0,
                y=0,
                width=self.config["rect"]["width"],
                height=self.config["rect"]["height"],
                scale=self.scale,
                config=self.config["rect"],
            ),
        )


class Annotation(Component):
    """Add text with a leaderline styled as an annotation.

    :param text_content: Annotation text
    :type text_content: String or List
    """

    def __init__(self, text_content, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Extract scale from offset and update x and y
        offset, self.scale = self.extract_scale(self.config["offset"])

        # override scale if explicitly provided
        if "scale" in kwargs.keys():
            self.scale = Coords(*kwargs["scale"])

        self.x = self.x * self.scale.x
        self.y = self.y * self.scale.y

        label_padding = Coords(*self.config["label"]["padding"])

        # Attempt to split on '\n' and convert to list
        if type(text_content) == str:
            text_content = text_content.split("\n")

        # Calculate label dimensions
        line_height = self.config["label"]["text"]["line_height"]
        font_height = self.config["label"]["text"]["size"]
        top_padding = label_padding.y - (line_height - font_height)
        label_height = (
            len(text_content) * self.config["label"]["text"]["line_height"]
            + label_padding.y
            + top_padding
        )
        self.config["label"]["rect"]["height"] = label_height

        # label required nudging to align with leaderline
        stroke_shim = self.config["leaderline"]["stroke_width"] / 2

        # Annotation label
        label = Component(
            tag="anno_label",
            x=offset.x - stroke_shim,
            y=offset.y + stroke_shim,
        )
        self.children.append(label)

        # Add background rect to label
        rect_y = 0 if self.scale.y == -1 else -label_height
        label.add(
            elem.Rect(
                y=rect_y,
                width=self.config["label"]["rect"]["width"],
                height=self.config["label"]["rect"]["height"],
                config=self.config["label"]["rect"],
            )
        )
        # Add textblock to label
        tb_x = label_padding.x
        if self.scale.x == -1:
            tb_x -= self.config["label"]["rect"]["width"]

        tb_y = -self.config["label"]["rect"]["height"] + top_padding

        label.add(
            elem.TextBlock(
                text_content,
                x=tb_x,
                y=tb_y,
                width=self.config["label"]["rect"]["width"] - label_padding.x * 2,
                height=self.config["label"]["rect"]["height"],
                config=self.config["label"],
                scale=self.scale,
            )
        )

        # Leaderline
        # leaderline rect
        leaderline_rect = self.add(
            elem.Rect(
                x=-self.config["leaderline"]["rect"]["width"] / 2,
                y=-self.config["leaderline"]["rect"]["height"] / 2,
                width=self.config["leaderline"]["rect"]["width"],
                height=self.config["leaderline"]["rect"]["height"],
                config=self.config["leaderline"]["rect"]
            )
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
        horizontal_move = f"H {offset.x + label.width - stroke_shim}"

        path_definition = f"M {start_x} {start_y} {vertical_move} {horizontal_move}"

        self.add(elem.Path(path_definition, config=self.config["leaderline"]))
