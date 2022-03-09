################################
#
# Default component settings
#
################################

# Diagram
diagram = {
    "units": "mm",
    "dpi": 300,
}


# Pinlabel
pinlabel = {
    "body": {
        "x": 6,
        "y": 0,
        "width": 28,
        "height": 10,
        "corner_radius": 1,
    },
}

"""

# Legend
legend = {
    "max_height": None,
    "inset": (10, 10, 10, 10),
    "tag": "legend",
    "entry": {
        "width": 159,
        "height": 28,
        "tag": "legend__entry",
    },
    "swatch": {
        "width": 20,
        "height": 20,
        "tag": "swatch",
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
    "inset": (2, 2, 2, 2),
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

################################
#
# SvgShapes
#
################################
svgshape = {"tag": "svgshape"}
image = {"tag": "image"}
text = {"tag": "text"}
circle = {"tag": "circle"}
rect = {"tag": "rect"}
path = {"tag": "path"}

################################
#
# KiCad footprint settings
#
################################
kicad_6_footprints = {
    "version": 6,
    "layer": "User.1",
    "pinlabel": {
        "hide_fp_text_reference": True,
        "hide_fp_text_user": True,
        "value_offset": (0, 25),  # (mm dimensions)
    },
    "annotation": {
        "hide_fp_text_reference": True,
        "hide_fp_text_user": True,
        "value_offset": (25, 25),  # (mm dimensions)
    },
    "textblock": {
        "hide_fp_text_reference": True,
        "hide_fp_text_user": True,
    },
}
kicad_5_footprints = {
    "version": 5,
    "layer": "Eco1.User",
    "pinlabel": {
        "hide_fp_text_reference": True,
        "hide_fp_text_user": True,
        "value_offset": (0, 25),  # (mm dimensions)
    },
    "annotation": {
        "hide_fp_text_reference": True,
        "hide_fp_text_user": True,
        "value_offset": (25, 25),  # (mm dimensions)
    },
    "textblock": {
        "hide_fp_text_reference": True,
        "hide_fp_text_user": True,
    },
}

"""
