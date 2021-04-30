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
        # return BoundingCoords(
        #    self.x + x_min, self.y + y_min, self.x + x_max, self.y + y_max
        # )

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

    def add_and_instantiate(self, cls, *args, **kwargs):
        """Instantiate a class and add it to the components children."""

        # if issubclass(cls, Element):
        #     kwargs["scale"] = self.scale

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


class PinLabel(Component):
    """Create a Pinlabel

    :param text_content: Text to appear in label
    :type text_content: string
    """

    def __init__(
        self,
        text_content,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # Assign config values if none supplied
        offset = self.cfg["offset"]

        # Separate offset and scale data
        offset, scale = self.extract_scale(offset)

        vertical_move = f"V {offset.y}" if offset.y != 0 else ""
        horizontal_move = f"H {offset.x}" if offset.x != 0 else ""

        definition = f"M 0 0 {vertical_move} {horizontal_move}"

        self.add_and_instantiate(
            elem.Path,
            definition=definition,
            # scale=self.scale,
            config=self.cfg["leaderline"],
        )

        self.add_and_instantiate(
            elem.Label,
            text_content,
            x=offset.x - 1,
            y=offset.y - self.cfg["label"]["rect"]["height"] / 2,
            # scale=self.scale,
            tag=self.tag,
            config=self.cfg["label"],
        )


class PinLabelRow(Component):
    """Create a row of PinLabels and leaderline connecting the row to an origin coordinate.

    :param offset: (x, y) offset of the row from an origin
    :type offset: (x, y) tuple
    :param labels: List of label data
    :type labels: [(<text>, <tag>, [<config>]),(<text>, <tag>, [<config>]), ...]
    """

    def __init__(self, offset, labels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.scale = self.extract_scale(offset)[1]
        # self.offset, self.scale = self.extract_scale(offset)
        # self.scale = Coords(-1, 1)
        # self.offset = Coords(*offset)
        self.offset = self.extract_scale(offset)[0]

        self.labels = self.add_and_instantiate(
            Component,
            x=self.offset.x,
            y=self.offset.y,
            # scale=self.scale,
        )

        cfg_tag = self.cfg.get("pinlabelrow", {}).get("tag", "")
        self.tag = (cfg_tag + self.tag).strip()

        self.add_labels(labels)

    def add_labels(self, label_list):
        for i, label in enumerate(label_list):
            ctx = dict(zip(("text_content", "tag", "config"), label))

            # Create a duplicate config for each pinlabel
            config = self.patch_config(copy.deepcopy(self.cfg), ctx.get("config", {}))

            # update tag in pinlabel and leaderline
            config["tag"] = " ".join([config["tag"], ctx.get("tag", "")])
            config["leaderline"]["tag"] = " ".join(
                [config["leaderline"]["tag"], ctx.get("tag", "")]
            )

            # update pinlabel config with tag styles
            tag_color = self.conf["tags"][ctx["tag"]]["color"]
            patch = {
                "label": {
                    "rect": {"fill": tag_color},
                },
                "leaderline": {"stroke": tag_color},
            }
            self.patch_config(config, patch)

            if i == 0:
                # Create a leaderline joining the labelrow to the offset origin
                v_move = f"V {self.offset.y}" if self.offset.y != 0 else ""
                h_move = f"H {self.offset.x}" if self.offset.x != 0 else ""
                definition = f"M 0 0 {v_move} {h_move}"

                self.add_and_instantiate(
                    elem.Path,
                    definition=definition,
                    # scale=self.scale,
                    config=config["leaderline"],
                )

            # Add PinLabel to label_row
            label_x = self.labels.width
            self.labels.add_and_instantiate(
                PinLabel,
                ctx["text_content"],
                x=label_x,
                y=0,
                tag=config["tag"],
                # scale=self.scale,
                config=config,
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

        # offset = Coords(*offset)
        offset, self.scale = self.extract_scale(offset)

        self.x = self.x * self.scale.x
        self.y = self.y * self.scale.y

        # Create a Component for each row in 'labels'
        for i, label_list in enumerate(labels):
            pin_x = pitch[0] * i * self.scale.x
            pin_y = pitch[1] * i * self.scale.y
            if pitch[1] == 0:
                # Horizontal pinset require label_rows to offset vertically
                offset = Coords(offset.x - pin_x, offset.y + abs(pin_x))

            self.add_and_instantiate(
                PinLabelRow,
                offset=offset,
                labels=label_list,
                x=pin_x,
                y=pin_y,
                config=self.cfg,
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
            entry = self.add_and_instantiate(
                Component, x=pad.x, y=pad.y + row_height * i, tag=self.cfg["tag"]
            )
            entry.add_and_instantiate(
                elem.Text,
                self.conf["tags"][tag]["title"],
                x=swatch_size * 2,
                y=0,
                width=self.cfg["rect"]["width"],
                height=row_height,
                config=self.cfg["text"],
            )

            pinlabel_config = copy.deepcopy(self.conf["pinlabel"])
            tag_color = self.conf["tags"][tag]["color"]
            pinlabel_patch = {
                "offset": (-swatch_size / 2, 0),
                "label": {
                    "rect": {
                        "fill": tag_color,
                        "height": swatch_size,
                        "width": swatch_size,
                        "rx": 2,
                    },
                },
                "leaderline": {
                    "stroke": tag_color,
                },
            }
            self.patch_config(pinlabel_config, pinlabel_patch)

            entry.add_and_instantiate(
                PinLabel,
                text_content="",
                x=-swatch_size * 1.5,
                tag="pl " + tag,
                config=pinlabel_config,
                scale=(-1, 1),
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
        label_height = (
            len(text_content) * self.cfg["label"]["text"]["line_height"]
            + label_padding.y
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
        rect_y = 0 if self.scale.y == -1 else -self.cfg["label"]["rect"]["height"]
        label.add_and_instantiate(
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

        tb_y = -self.cfg["label"]["rect"]["height"]

        label.add_and_instantiate(
            elem.TextBlock,
            text_content,
            x=tb_x,
            y=tb_y,
            width=self.cfg["label"]["rect"]["width"],
            height=self.cfg["label"]["rect"]["height"],
            config=self.cfg["label"],
            scale=self.scale,
        )
        ########################
        # Leaderline

        # leaderline rect
        leader_rect = self.add_and_instantiate(
            elem.Rect,
            x=-self.cfg["leaderline"]["rect"]["width"] / 2,
            y=-self.cfg["leaderline"]["rect"]["height"] / 2,
            width=self.cfg["leaderline"]["rect"]["width"],
            height=self.cfg["leaderline"]["rect"]["height"],
            config=self.cfg["leaderline"]["rect"],
        )

        # path definition
        vertical_move = f"V {offset.y}" if offset.y != 0 else ""
        horizontal_move = f"H {offset.x}" if offset.x != 0 else ""

        path_definition = f"M 0 0 {vertical_move} {horizontal_move}"

        self.add_and_instantiate(
            elem.Path, path_definition, config=self.cfg["leaderline"]
        )
