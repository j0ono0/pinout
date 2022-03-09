############################################################
#
# Component settings for mm (millimetre) diagram units
# This file supplies override values to default_config.py
#
############################################################


diagram = {
    "units": "mm",
    "dpi": 300,
}

pinlabel = {
    "body": {
        "x": 3,
        "y": 0,
        "width": 26,
        "height": 9,
        "corner_radius": 1,
    },
}

legend = {
    "inset": (2, 2, 2, 2),
    "tag": "legend",
    "entry": {
        "width": 50,
        "height": 9,
        "tag": "legend__entry",
    },
    "swatch": {
        "width": 5,
        "height": 5,
        "tag": "swatch",
    },
}

# TextBlock
textblock = {
    "line_height": "12.5pt",
}


# Annotation
annotation = {
    "tag": "annotation",
    "content": {
        "x": 3,
        "y": 19,
        "line_height": 11,
    },
    "body": {
        "x": 30,
        "y": 15,
        "width": 60,
        "height": 16,
        "corner_radius": 3,
    },
    "target": {
        "x": -3,
        "y": -3,
        "width": 6,
        "height": 6,
        "corner_radius": 3,
    },
}

"""

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
