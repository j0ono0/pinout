import math
from .core import Group, SvgShape, Rect, BoundingCoords, Coords
from . import config


class Pin(Group):
    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)
        self.add(SvgShape(width=width, height=height))

    def render(self):
        self.add(
            Rect(
                x=0,
                y=-self.height / 2,
                width=self.width,
                height=self.height,
                tag="pin__leg",
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
            x = self.inset.x1
        else:
            # rhs header
            index = index - self.pin_count // 2
            x = self.width - self.inset.x2
        y = self.pin_pitch * index
        return Coords(x, y)

    def render(self):
        # Add body
        x1, y1, x2, y2 = self.inset
        body = self.add(
            Rect(
                x=x1,
                y=y1,
                width=self.width - (x1 + x2),
                height=self.height - (y1 + y2),
            )
        )
        # Add pin legs
        for i in range(1, self.pin_count + 1):
            if i <= self.pin_count // 2:
                scale = (-1, 1)
            else:
                scale = (1, 1)
            x, y = self.pin_coords(i)
            self.add(
                Pin(
                    width=self.inset.x1,
                    height=self.pin_pitch / 2,
                    x=x,
                    y=y,
                    tag=f"ic__leg pin_{i}",
                    scale=scale,
                )
            )

        return super().render()


class QFP(Group):
    def __init__(self, pin_count, length, **kwargs):
        self.pin_count = pin_count
        super().__init__(**kwargs)
        self.update_config(config.ic_qfp)

        self.inset = BoundingCoords(*self.config["inset"])
        self.add(SvgShape(width=length, height=length))
        self.add_tag(self.config["tag"])

    @property
    def pin_pitch(self):
        body_height = self.height - (self.inset.y1 + self.inset.y2)
        header_len = self.pin_count // 4
        return body_height / (header_len + 1)

    def pin_coords(self, index, rotate=True):
        if index <= self.pin_count * 0.25:
            # bottom
            x = self.inset.x1 + self.pin_pitch * index
            y = self.height - self.inset.y2
        elif index <= self.pin_count * 0.5:
            # rhs
            x = self.width - self.inset.x2
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
            y = self.inset.y2
        else:
            # lhs
            x = self.inset.x2
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
                )
            )

        return super().render()