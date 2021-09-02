def pitch_generator(start, pitch):
    x = start[0]
    y = start[1]
    while True:
        yield (x, y)
        x += pitch[0]
        y += pitch[1]


################################
#
# Default component settings
#
################################

# Pinlabel
pinlabel = {
    "tag": "pinlabel",
    "body": {
        "x": 6,
        "y": 0,
        "width": 80,
        "height": 26,
        "corner_radius": 3,
        "tag": "pinlabel__body",
    },
    "leaderline": {
        "direction": "hh",
        "tag": "pinlabel__leader",
    },
    "text": {
        "tag": "pinlabel__text",
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
        "tag": "legendentry",
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
    "content": {
        "tag": "annotation__text",
        "x": 28,
        "y": 17,
        "line_height": 16,
    },
    "body": {
        "x": 40,
        "y": 29,
        "width": 250,
        "height": 50,
        "corner_radius": 25,
        "tag": "annotation__body",
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

# Panel
panel = {
    "inset": (5, 5, 5, 5),
    "tag": "panel",
    "inner": {"tag": "panel__inner"},
    "outer": {"tag": "panel__outer"},
}


# Integrated circuit
ic_dip = {
    "inset": (15, 0, 15, 0),
    "tag": "ic ic--dip",
    "body": {
        "x": 15,
        "y": 0,
        "corner_radius": 3,
        "tag": "ic__body",
    },
    "leg": {
        "tag": "ic__leg",
    },
    "polarity_mark": {
        "radius": 5,
        "tag": "polarity",
    },
}
ic_qfp = {
    "inset": (15, 15, 15, 15),
    "pin_pitch": 30,
    "tag": "ic ic--qfp",
    "body": {
        "x": 15,
        "y": 15,
        "corner_radius": 3,
        "tag": "ic__body",
    },
    "leg": {
        "tag": "ic__leg",
    },
    "polarity_mark": {
        "radius": 5,
        "tag": "polarity",
    },
}

# Diagram layout template presets
diagram_presets = {
    "tag": "layout",
    "panel_00": {
        "inset": (2, 2, 2, 2),
        "tag": "panel",
        "inner": {"tag": "panel__inner"},
        "outer": {"tag": "panel__outer"},
    },
    "panel_01": {
        "inset": (0.5, 0.5, 0.5, 0.5),
        "tag": "panel--main",
        "inner": {"tag": "panel__inner"},
        "outer": {"tag": "panel__outer"},
    },
    "panel_02": {
        "inset": (0.5, 0.5, 0.5, 0.5),
        "tag": "panel--info",
        "inner": {"tag": "panel__inner"},
        "outer": {"tag": "panel__outer"},
    },
}
