config = {
    ################################
    #
    # Dimension config: mm units
    # note: typography in pt as this
    # is typical for print design
    #
    ################################
    "diagram": {
        "units": "mm",
    },
    "panel": {
        "inset": (2, 2, 2, 2),
    },
    "pinlabel": {
        "body": {
            "x": 1.5,
            "y": 0,
            "width": 16,
            "height": 8,
            "corner_radius": 1,
        },
        "leaderline": {
            "stroke_width": 0.5,
        },
        "text": {},
    },
    "legend": {
        "max_height": None,
        "inset": (5, 5, 5, 5),
        "entry": {
            "width": 45,
            "height": 8,
        },
        "swatch": {
            "width": 5,
            "height": 5,
        },
    },
    "text": {
        "font_size": "9pt",
    },
    "textblock": {
        "line_height": "12pt",
        "width": None,
        "height": None,
        "offset": (0, 0),
    },
    "annotation": {
        "tag": "annotation",
        "content": {
            "x": 20,
            "y": 30,
            "line_height": "16pt",
            "font_size": "14px",
            "font_weight": "bold",
        },
        "body": {
            "x": 40,
            "y": 29,
            "width": 40,
            "height": 16,
            "corner_radius": 8,
            "stroke_width": 0.5,
        },
        "target": {
            "x": -5,
            "y": -5,
            "width": 5,
            "height": 5,
            "corner_radius": 2.5,
            "stroke_width": 0.5,
        },
        "leaderline": {
            "stroke_width": 0.5,
        },
    },
    ################################
    #
    # SvgShapes
    #
    ################################
    "svgshape": {},
    "image": {},
    "circle": {},
    "rect": {},
    "path": {},
    ################################
    #
    # Diagram layout template presets
    #
    ################################
    "diagram_presets": {
        "h1": {
            "font_size": "20pt",
        },
        "panel_00": {
            "inset": (2, 2, 2, 2),
            "inner": {},
            "outer": {},
        },
        "panel_01": {
            "inset": (0.5, 0.5, 0.5, 0.5),
            "inner": {},
            "outer": {},
        },
        "panel_02": {
            "inset": (0.5, 0.5, 0.5, 0.5),
            "inner": {},
            "outer": {},
        },
    },
    ################################
    #
    # Integrated circuits
    #
    ################################
    "ic_dip": {
        "inset": (5, 0, 5, 0),
        "body": {
            "x": 5,
            "y": 0,
            "corner_radius": 3,
            "stroke_width": 0,
        },
        "leg": {
            "stroke_width": 0.5,
        },
        "polarity_mark": {
            "radius": 2.5,
            "stroke_width": 0.5,
        },
    },
    "ic_qfp": {
        "inset": (5, 5, 5, 5),
        "pin_pitch": 10,
        "body": {
            "x": 5,
            "y": 5,
            "corner_radius": 3,
            "stroke_width": 0.5,
        },
        "leg": {
            "stroke_width": 0.5,
        },
        "polarity_mark": {
            "radius": 2.5,
            "stroke_width": 1,
        },
    },
}
