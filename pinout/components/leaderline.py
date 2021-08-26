import math
from pinout import core


class Leaderline(core.Path):
    """Leaderline base object."""

    def __init__(self, direction="hh", **kwargs):
        self.direction = direction
        self.start = core.Coords(0, 0)
        self.end = core.Coords(0, 0)
        super().__init__(**kwargs)

    def end_points(self, origin, destination):
        """Locate origin and destination coordinates."""
        # origin and destination are components with bounding-boxes
        # direction is a 2 char code representing starting and ending directions
        # 'h' horizontal, 'v' vertical
        o_coords = origin.bounding_coords()
        d_coords = destination.bounding_coords()

        start = {
            "h": core.Coords(o_coords.x2, o_coords.y1 + origin.height / 2),
            "v": core.Coords(origin.x + (o_coords.x2 - o_coords.x1) / 2, o_coords.y2),
        }
        end = {
            "h": core.Coords(d_coords.x1, d_coords.y1 + destination.height / 2),
            "v": core.Coords(
                destination.x + (d_coords.x2 - d_coords.x1) / 2, d_coords.y1
            ),
        }
        self.start = start[self.direction[0]]
        self.end = end[self.direction[-1]]
        return (self.start, self.end)

    def bounding_coords(self):
        return core.BoundingCoords(
            min(self.start.x, self.end.x),
            min(self.start.y, self.end.y),
            max(self.start.x, self.end.x),
            max(self.start.y, self.end.y),
        )


class Curved(Leaderline):
    """Leaderline comprised of one or two curved corners."""

    def route(self, origin, destination):

        o_coords = origin.bounding_coords()
        d_coords = destination.bounding_coords()

        r = min(abs(origin.x - destination.x), abs(origin.y - destination.y)) / 3
        len = (d_coords.x1 - o_coords.x2) / 8
        ctl_h = (d_coords.x1 - o_coords.x2) / 2
        ctl_v = (d_coords.y1 - o_coords.y2) / 2

        start, end = self.end_points(origin, destination)

        if self.direction == "vh":
            # start vertical, end horizontal
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {start.x} {end.y - r}",
                    f"A {r} {r} 0 0 0 {start.x + r} {end.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "hv":
            # start horizontal, end vertical
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {end.x - r} {start.y}",
                    f"A {r} {r} 0 0 1 {end.x} {start.y + r}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "hh":
            # start horizontal, end horizontal
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {start.x + len} {start.y}",
                    f"C {start.x + ctl_h} {start.y} {end.x - ctl_h} {end.y} {end.x - len} {end.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "vv":
            # start vertical, end vertical
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {start.x} {start.y + len}",
                    f"C {start.x} {start.y + ctl_v} {end.x} {end.y - ctl_v} {end.x} {end.y - len}",
                    f"L {end.x} {end.y}",
                ]
            )
        else:
            path_def = ""

        self.d = path_def


class Angled(Leaderline):
    """Leaderline comprised of one or two sharp 90 degree corners."""

    def route(self, origin, destination):

        start, end = self.end_points(origin, destination)

        if self.direction == "vh":
            # start vertical, end horizontal
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {start.x} {end.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "hv":
            # start horizontal, end vertical
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {end.x} {start.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "hh":
            # start horizontal, end horizontal
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {start.x + (end.x - start.x)/4} {start.y}",
                    f"L {start.x + (end.x - start.x)/4} {end.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "vv":
            # start vertical, end vertical
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {start.x} {start.y + (end.y - start.y)/4}",
                    f"L {end.x} {start.y + (end.y - start.y)/4}",
                    f"L {end.x} {end.y}",
                ]
            )
        else:
            path_def = ""

        self.d = path_def


class Diagonal(Leaderline):
    """ Leaderline comprised of a diagonal and horizontal line"""

    def route(self, origin, destination):

        start, end = self.end_points(origin, destination)
        x_dist = abs(start.x - end.x)
        y_dist = abs(start.y - end.y)

        min_dist = min(x_dist, y_dist)

        segment = min_dist / 6
        segment_x = segment * math.cos(math.radians(45))
        segment_y = segment * math.sin(math.radians(45))
        radius = segment * math.tan(math.radians(67.5))

        path_def = " ".join(
            [
                f"M {start.x} {start.y}",
                f"L {start.x + min_dist - segment_x} {start.y + min_dist - segment_y}",
                f"A {radius} {radius} 0 0 0  {start.x + min_dist + segment} {end.y}",
                f"L {end.x} {end.y}",
            ]
        )

        self.d = path_def


class DiagonalAngled(Leaderline):
    """ Leaderline comprised of a diagonal and horizontal line"""

    def route(self, origin, destination):

        start, end = self.end_points(origin, destination)
        x_dist = abs(start.x - end.x)
        y_dist = abs(start.y - end.y)
        min_dist = min(x_dist, y_dist)

        path_def = " ".join(
            [f"M {start.x} {start.y}", f"l {min_dist} {min_dist}" f"L {end.x} {end.y}"]
        )

        self.d = path_def


class Straight(Leaderline):
    """Leaderline comprised of a single straight line."""

    def route(self, origin, destination):

        start, end = self.end_points(origin, destination)

        if self.direction == "vh":
            # start vertical, end horizontal
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "hv":
            # start horizontal, end vertical
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "hh":
            # start horizontal, end horizontal
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        elif self.direction == "vv":
            # start vertical, end vertical
            path_def = " ".join(
                [
                    f"M {start.x} {start.y}",
                    f"L {end.x} {end.y}",
                ]
            )
        else:
            path_def = ""

        self.d = path_def
