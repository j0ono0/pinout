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
        "y": 29,
        "width": 250,
        "height": 50,
        "corner_radius": 25,
        "tag": "annotation__body",
        "textblock": {
            "x": 28,
            "y": 17,
            "line_height": 16,
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
