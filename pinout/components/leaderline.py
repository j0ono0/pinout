from pinout import core


class Base:
    def __init__(self, direction="hh", **kwargs):
        self.direction = direction
        self.path_def = ""
        self.kwargs = kwargs

    def end_points(self, origin, destination):
        # origin and destination are components with bounding-boxes
        # direction is a 2 char code representing starting and ending directions
        # 'h' horizontal, 'v' vertical
        o_coords = origin.bounding_coords()
        d_coords = destination.bounding_coords()

        start = {
            "h": core.Coords(o_coords.x2, origin.y + (o_coords.y2 - o_coords.y1) / 2),
            "v": core.Coords(origin.x + (o_coords.x2 - o_coords.x1) / 2, o_coords.y2),
        }
        end = {
            "h": core.Coords(
                d_coords.x1, destination.y + (d_coords.y2 - d_coords.y1) / 2
            ),
            "v": core.Coords(
                destination.x + (d_coords.x2 - d_coords.x1) / 2, d_coords.y1
            ),
        }
        return (start[self.direction[0]], end[self.direction[-1]])

    def render(self):
        path = core.Path(path_definition=self.path_def, **self.kwargs)
        path.add_tag("lline lline--curved")
        print("rendering lline")
        return path.render()


class Curved(Base):
    def route(self, origin, destination):

        o_coords = origin.bounding_coords()
        d_coords = destination.bounding_coords()

        r = min(destination.x, destination.y) / 3
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

        self.path_def = path_def


class Angled(Base):
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

        self.path_def = path_def


class Straight(Base):
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

        self.path_def = path_def
