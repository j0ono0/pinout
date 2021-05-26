# Pinout Configuration
# Tools to assist with keeping configuration DRY
#
# May store default configurations here?

import copy


class PinConfig:
    """Convenience class to store common pin configurations."""

    def __init__(self, presets):
        self.presets = presets or {}
        self.pitch = None

    def __call__(self, preset=None, **kwargs):
        config = copy.deepcopy(self.presets.get(preset, {}))
        config.update(kwargs)
        # If no offset is supplied use next pitch from generator
        # Convoluted assignment as dict.get always runs default value function!?
        config["offset"] = config.get("offset", None) or next(self.pitch)
        return config

    def pitch_generator(self, start, pitch):
        x = start[0]
        y = start[1]
        while True:
            yield (x, y)
            x += pitch[0]
            y += pitch[1]

    def set_pitch(self, start, pitch):
        self.pitch = self.pitch_generator(start, pitch)
