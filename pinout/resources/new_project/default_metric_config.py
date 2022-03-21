config = {
    ################################
    #
    # Component settings
    #
    ################################
    "diagram": {
        "tag": "diagram",
        "units": "mm",
        "dpi": 96,
    },
    "group": {
        "tag": "group",
    },
    "panel": {
        "inset": (2, 2, 2, 2),
        "tag": "panel",
        "inner": {
            "tag": "panel__inner",
            "fill": "#fff",
        },
        "outer": {
            "tag": "panel__outer",
            "fill": "#333",
        },
    },
    "pinlabel": {
        "tag": "pinlabel",
        "body": {
            "x": 1.5,
            "y": 0,
            "width": 16,
            "height": 8,
            "corner_radius": 1,
            "tag": "pinlabel__body",
        },
        "leaderline": {
            "direction": "hh",
            "tag": "pinlabel__leader",
            "stroke_width": 0.5,
        },
        "text": {
            "tag": "pinlabel__text",
        },
    },
    "legend": {
        "max_height": None,
        "inset": (10, 10, 10, 10),
        "tag": "legend",
        "entry": {
            "width": 159,
            "height": 28,
            "tag": "legend__entry",
            "dominant_baseline": "central",
        },
        "swatch": {
            "width": 20,
            "height": 20,
            "tag": "legend__swatch",
        },
    },
    "text": {
        "font_family": "Verdana, Georgia, sans-serif",
        "font_size": "9pt",
        "font_weight": "normal",
    },
    "textblock": {
        "line_height": 22,
        "width": None,
        "height": None,
        "offset": (0, 0),
        "tag": "textblock",
    },
    "annotation": {
        "tag": "annotation",
        "content": {
            "x": 28,
            "y": 17,
            "line_height": 16,
            "tag": "annotation__text",
            "dominant_baseline": "hanging",
            "font_size": "14px",
            "font_weight": "bold",
            "fill": "rgb(63, 40, 6)",
            "text_anchor": "start",
        },
        "body": {
            "x": 40,
            "y": 29,
            "width": 250,
            "height": 50,
            "corner_radius": 25,
            "tag": "annotation__body",
            "fill": "rgb(253, 203, 36)",
            "stroke_width": 0.5,
        },
        "target": {
            "x": -5,
            "y": -5,
            "width": 5,
            "height": 5,
            "corner_radius": 2.5,
            "tag": "annotation__target",
            "fill": "none",
            "stroke": "rgb(253, 203, 36)",
            "stroke_width": 0,
        },
        "leaderline": {
            "direction": "vh",
            "tag": "annotation__leaderline",
            "fill": "none",
            "stroke": "rgb(253, 203, 36)",
            "stroke_width": 0,
        },
    },
    ################################
    #
    # SvgShapes
    #
    ################################
    "svgshape": {"tag": "svgshape"},
    "image": {"tag": "image"},
    "circle": {"tag": "circle"},
    "rect": {"tag": "rect"},
    "path": {"tag": "path"},
    ################################
    #
    # Diagram layout template presets
    #
    ################################
    "diagram_presets": {
        "tag": "layout",
        "h1": {
            "tag": "h1",
            "font_size": "20pt",
            "font_weight": "bold",
        },
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
            "inner": {
                "tag": "panel__inner",
                "fill": "#ededed",
            },
            "outer": {"tag": "panel__outer"},
        },
    },
    ################################
    #
    # Integrated circuits
    #
    ################################
    "ic_dip": {
        "inset": (15, 0, 15, 0),
        "tag": "ic ic--dip",
        "body": {
            "x": 15,
            "y": 0,
            "corner_radius": 3,
            "tag": "ic__body",
            "fill": "none",
            "stroke": "rgb(0, 0, 0)",
            "stroke_width": 0,
        },
        "leg": {
            "tag": "ic__leg",
            "fill": "rgb(255, 255, 255)",
            "stroke": "rgb(0, 0, 0)",
            "stroke_width": 0.5,
        },
        "polarity_mark": {
            "radius": 5,
            "tag": "polarity",
            "fill": "rgb(85, 85, 85)",
            "stroke": "rgb(0, 0, 0)",
            "stroke_width": 0.5,
        },
    },
    "ic_qfp": {
        "inset": (15, 15, 15, 15),
        "pin_pitch": 30,
        "tag": "ic ic--qfp",
        "body": {
            "x": 15,
            "y": 15,
            "corner_radius": 3,
            "tag": "ic__body",
            "fill": "rgb(85, 85, 85)",
            "stroke": "rgb(0, 0, 0)",
            "stroke_width": 0.5,
        },
        "leg": {
            "tag": "ic__leg",
            "fill": "rgb(255, 255, 255)",
            "stroke": "rgb(0, 0, 0)",
            "stroke_width": 0.5,
        },
        "polarity_mark": {
            "radius": 5,
            "tag": "polarity",
            "fill": "rgb(85, 85, 85)",
            "stroke": "rgb(138, 138, 138)",
            "stroke_width": 1,
        },
    },
    ################################
    #
    # KiCad footprint settings
    #
    ################################
    "kicad_6_footprints": {
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
    },
    "kicad_5_footprints": {
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
    },
}
