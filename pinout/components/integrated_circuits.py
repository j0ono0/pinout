import math
from pinout.core import Group, SvgShape, Rect, BoundingCoords, Coords
from pinout import config
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.leaderline import Curved


class Pin(Group):
    def __init__(self, width, height, polarity_mark=False, **kwargs):
        self.polarity_mark = polarity_mark
        super().__init__(**kwargs)
        self.add(
            SvgShape(
                x=-width / 2,
                y=-height / 2,
                width=width,
                height=height,
            )
        )

    def render(self):
        self.add(
            Rect(
                x=-self.width / 2,
                y=-self.height / 2,
                width=self.width,
                height=self.height,
                tag="pin__leg",
            )
        )
        # Add polarity marking
        if self.polarity_mark:
            radius = self.config["radius"]
            self.add(
                Rect(
                    x=-self.width / 2 - radius * 3,
                    y=-radius,
                    width=radius * 2,
                    height=radius * 2,
                    corner_radius=radius,
                    tag=self.config["tag"],
                )
            )
        return super().render()


class DIP(Group):
    def __init__(self, pin_count, width, height, **kwargs):
        self.pin_count = pin_count
        super().__init__(**kwargs)
        self.update_config(config.ic_dip)

        self.inset = BoundingCoords(*self.config["inset"])
        self.add(SvgShape(width=width, height=height))
        self.add_tag(self.config["tag"])

    @property
    def pin_pitch(self):
        body_height = self.height - (self.inset.y1 + self.inset.y2)
        header_len = self.pin_count // 2
        return body_height / (header_len + 1)

    def pin_coords(self, index):
        if index <= self.pin_count // 2:
            # lhs header
            x = self.inset.x1 / 2
        else:
            # rhs header
            index = index - self.pin_count // 2
            x = self.width - self.inset.x2 / 2
        y = self.pin_pitch * index
        return Coords(x, y)

    def render(self):
        # Add body
        x1, y1, x2, y2 = self.inset
        self.add(
            Rect(
                x=x1,
                y=y1,
                width=self.width - (x1 + x2),
                height=self.height - (y1 + y2),
                corner_radius=self.config["body"]["corner_radius"],
                tag=self.config["body"]["tag"],
            )
        )
        # Add pin legs
        for i in range(1, self.pin_count + 1):
            if i <= self.pin_count // 2:
                scale = Coords(-1, 1)
            else:
                scale = Coords(1, 1)
            x, y = self.pin_coords(i)
            self.add(
                Pin(
                    width=self.inset.x1,
                    height=self.pin_pitch / 2,
                    x=x,
                    y=y,
                    tag=f"ic__leg pin_{i}",
                    scale=scale,
                    polarity_mark=i == 1,
                    config=self.config["polarity_mark"],
                )
            )

        return super().render()


class QFP(Group):
    def __init__(self, pin_count, length, **kwargs):
        if pin_count % 4 != 0:
            raise ValueError("pin_count not divisible by 4.")
        self.pin_count = pin_count
        super().__init__(**kwargs)
        self.update_config(config.ic_qfp)

        self.inset = BoundingCoords(*self.config["inset"])
        self.add(SvgShape(width=length, height=length))
        self.add_tag(self.config["tag"])

    @property
    def pin_pitch(self):
        body_length = self.height - (self.inset.y1 + self.inset.y2)
        pins_per_side = self.pin_count // 4
        return body_length / (pins_per_side + 1)

    @property
    def pitch_coords(self):
        pitch_x = math.cos(math.radians(self.rotate)) * self.pin_pitch
        pitch_y = math.sin(math.radians(self.rotate)) * self.pin_pitch
        return Coords(pitch_x, pitch_y)

    def pin_coords(self, index, rotate=True):
        if index <= self.pin_count * 0.25:
            # bottom
            x = self.inset.x1 + self.pin_pitch * index
            y = self.height - self.inset.y2 / 2
        elif index <= self.pin_count * 0.5:
            # rhs
            x = self.width - self.inset.x2 / 2
            y = (
                self.height
                - self.inset.y2
                - self.pin_pitch * (index - self.pin_count * 0.25)
            )
        elif index <= self.pin_count * 0.75:
            # top
            x = (
                self.width
                - self.inset.x1
                - self.pin_pitch * (index - self.pin_count * 0.5)
            )
            y = self.inset.y2 / 2
        else:
            # lhs
            x = self.inset.x2 / 2
            y = self.inset.y1 + self.pin_pitch * (index - self.pin_count * 0.75)

        # calculate for rotation
        if rotate:
            rotate = math.radians(self.rotate)
            rx = math.cos(rotate) * x - math.sin(rotate) * y
            ry = math.sin(rotate) * x + math.cos(rotate) * y
            return Coords(rx, ry)

        return Coords(x, y)

    def render(self):
        # Add body
        x1, y1, x2, y2 = self.inset
        self.add(
            Rect(
                x=x1,
                y=y1,
                width=self.width - (x1 + x2),
                height=self.height - (y1 + y2),
                corner_radius=self.config["body"]["corner_radius"],
                tag=self.config["body"]["tag"],
            )
        )
        # Add pin legs
        for i in range(1, self.pin_count + 1):
            if i <= self.pin_count * 0.25:
                scale = (1, 1)
                rotate = 90
            elif i <= self.pin_count * 0.5:
                scale = (1, 1)
                rotate = 0
            elif i <= self.pin_count * 0.75:
                scale = (1, 1)
                rotate = -90
            else:
                scale = (-1, 1)
                rotate = 0
            x, y = self.pin_coords(i, False)
            self.add(
                Pin(
                    width=self.inset.x1,
                    height=self.pin_pitch / 2,
                    x=x,
                    y=y,
                    tag=f"ic__leg pin_{i}",
                    scale=scale,
                    rotate=rotate,
                    polarity_mark=i == 1,
                    config=self.config["polarity_mark"],
                )
            )

        return super().render()


def labelled_qfn(labels, length=160, label_start=(100, 20), label_pitch=(0, 30)):

    graphic = Group()
    ic = graphic.add(
        QFP(
            pin_count=len(labels),
            length=length,
            rotate=45,
        )
    )
    pins_per_side = int(ic.pin_count * 0.25)

    # Side 1
    graphic.add(
        PinLabelGroup(
            x=ic.pin_coords(1).x,
            y=ic.pin_coords(1).y,
            pin_pitch=(ic.pitch_coords),
            label_start=label_start,
            label_pitch=label_pitch,
            scale=(-1, 1),
            labels=labels[:pins_per_side],
            leaderline=Curved(direction="vh"),
        )
    )

    # Side 2
    graphic.add(
        PinLabelGroup(
            x=ic.pin_coords(pins_per_side * 2).x,
            y=ic.pin_coords(pins_per_side * 2).y,
            pin_pitch=(-ic.pitch_coords.y, ic.pitch_coords.x),
            label_start=label_start,
            label_pitch=label_pitch,
            scale=(1, 1),
            labels=labels[int(pins_per_side * 2) - 1 : pins_per_side - 1 : -1],
            leaderline=Curved(direction="vh"),
        )
    )

    # Side 3
    graphic.add(
        PinLabelGroup(
            x=ic.pin_coords(pins_per_side * 2 + 1).x,
            y=ic.pin_coords(pins_per_side * 2 + 1).y,
            pin_pitch=(-ic.pitch_coords.x, -ic.pitch_coords.y),
            label_start=label_start,
            label_pitch=label_pitch,
            scale=(1, -1),
            labels=labels[pins_per_side * 2 : pins_per_side * 3],
            leaderline=Curved(direction="vh"),
        )
    )

    # Side 4
    graphic.add(
        PinLabelGroup(
            x=ic.pin_coords(pins_per_side * 4).x,
            y=ic.pin_coords(pins_per_side * 4).y,
            pin_pitch=(ic.pitch_coords.x, -ic.pitch_coords.y),
            label_start=label_start,
            label_pitch=label_pitch,
            scale=(-1, -1),
            labels=labels[pins_per_side * 4 - 1 : pins_per_side * 3 - 1 : -1],
            leaderline=Curved(direction="vh"),
        )
    )
    return graphic
