# Pinout Configuration
# Tools to assist with keeping configuration DRY
#
# TODO: investigate storing default configurations here?

import warnings
import copy


class PinConfig:
    """Convenience class to store common pin configurations."""

    def __init__(self, presets):
        self.presets = presets or {}
        self.offset = None
        self.origin = None

    def __call__(self, preset=None, **kwargs):
        config = copy.deepcopy(self.presets.get(preset, {}))
        config.update(kwargs)
        # If no offset is supplied use next offset from generator
        # Convoluted assignment as dict.get always runs default value function!?
        offset = config.get("offset", None)
        if offset is None:
            config["x"], config["y"] = next(self.origin)
            config["offset"] = next(self.offset)

        return config

    def pitch_generator(self, start, pitch):
        x = start[0]
        y = start[1]
        while True:
            yield (x, y)
            x += pitch[0]
            y += pitch[1]

    def set_offset(self, start, pitch):
        if start[0] < 0:
            msg = f"""
                {self}:
                Negative 'x' value in 'start' argument has unintended results! 
                Value has been converted to absolute value.
                Use Label.scale=(-1, 1) to 'flip' a label horizontally
                """
            warnings.warn(msg)
            start = (abs(start[0]), start[1])
        self.offset = self.pitch_generator(start, pitch)

    def set_origin(self, start, pitch):
        self.origin = self.pitch_generator(start, pitch)


def pitch_generator(start, pitch):
    x = start[0]
    y = start[1]
    while True:
        yield (x, y)
        x += pitch[0]
        y += pitch[1]


###########################
#
# Defaults
#

# Pinlabel
pinlabel = {
    "tag": "pinlabel",
    "body": {
        "x": 6,
        "y": 0,
        "width": 80,
        "height": 26,
        "corner_radius": 30,
    },
    "leaderline": {
        "direction": "hh",
    },
}

# Legend
legend = {
    "max_height": None,
    "inset": (10, 10, 10, 10),
    "tag": "legend",
    "entry": {
        "width": 159,
        "height": 28,
        "swatch": {
            "width": 20,
            "height": 20,
            "tag": "swatch",
        },
        "tag": "legend-entry",
    },
}

# TextBlock
textblock = {
    "line_height": 22,
    "width": None,
    "height": None,
    "offset": (0, 0),
    "tag": "textblock",
}

# Annotation
annotation = {
    "tag": "annotation",
    "body": {
        "x": 40,
        "y": 20,
        "width": 250,
        "height": 60,
        "corner_radius": 30,
        "tag": "annotation__body",
        "textblock": {
            "x": 28,
            "y": 22,
            "line_height": 18,
        },
    },
    "target": {
        "x": -10,
        "y": -10,
        "width": 20,
        "height": 20,
        "corner_radius": 10,
        "tag": "annotation__target",
    },
    "leaderline": {
        "direction": "vh",
        "tag": "annotation__leaderline",
    },
}
