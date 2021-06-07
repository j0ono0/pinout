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
pinlabel_body = {"width": 80, "height": 26}
pinlabel_offset = (6, 0)


# Annotation
annotation = {
    "body": {
        "width": 200,
        "height": 60,
        "offset": (60, 60),
        "tag": "annotation__body",
    },
    "target": {
        "width": 10,
        "height": 10,
        "tag": "annotation__target",
    },
    "text": {
        "line_height": 22,
        "offset": (0, 0),
    },
    "leaderline": {
        "direction": "vv",
    },
}

annotation_body_width = 200
annotation_body_height = 60
annotation_body_offset = (0, 0)

annotation_target_width = 10
annotation_target_height = 10

annotation_text_line_height = 22
annotation_text_offset = (0, 0)