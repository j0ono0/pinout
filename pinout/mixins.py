from collections import namedtuple

Coords = namedtuple("Coords", ("x y"))
BoundingCoords = namedtuple("BoundingCoords", ("x1 y1 x2 y2"))
BoundingRect = namedtuple("BoundingCoords", ("x y w h"))


class PresentationMixin:
    def __init__(
        self,
        alignment_baseline=None,
        baseline_shift=None,
        clip=None,
        clip_path=None,
        clip_rule=None,
        color=None,
        color_interpolation=None,
        color_interpolation_filters=None,
        color_profile=None,
        color_rendering=None,
        cursor=None,
        direction=None,
        display=None,
        dominant_baseline=None,
        enable_background=None,
        fill=(0, 0, 0, 1),
        fill_opacity=1,
        fill_rule=None,
        filter=None,
        flood_color=None,
        flood_opacity=None,
        font_family="Helvetica, Verdana",
        font_size="16",
        font_size_adjust=None,
        font_stretch=None,
        font_style=None,
        font_variant=None,
        font_weight="normal",
        glyph_orientation_horizontal=None,
        glyph_orientation_vertical=None,
        image_rendering=None,
        kerning=None,
        letter_spacing=None,
        lighting_color=None,
        marker_end=None,
        marker_mid=None,
        marker_start=None,
        mask=None,
        opacity=1,
        overflow=None,
        pointer_events=None,
        shape_rendering=None,
        stop_color=None,
        stop_opacity=None,
        stroke=(0, 0, 0, 1),
        stroke_dasharray=None,
        stroke_dashoffset=None,
        stroke_linecap="round",
        stroke_linejoin=None,
        stroke_miterlimit=None,
        stroke_opacity=1,
        stroke_width=0,
        text_anchor="left",
        text_decoration=None,
        text_rendering=None,
        transform=None,
        transform_origin=None,
        unicode_bidi=None,
        vector_effect=None,
        visibility=None,
        word_spacing=None,
        writing_mode=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.alignment_baseline = alignment_baseline
        self.baseline_shift = baseline_shift
        self.clip = clip
        self.clip_path = clip_path
        self.clip_rule = clip_rule
        self.color = color
        self.color_interpolation = color_interpolation
        self.color_interpolation_filters = color_interpolation_filters
        self.color_profile = color_profile
        self.color_rendering = color_rendering
        self.cursor = cursor
        self.direction = direction
        self.display = display
        self.dominant_baseline = dominant_baseline
        self.enable_background = enable_background
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.fill_rule = fill_rule
        self.filter = filter
        self.flood_color = flood_color
        self.flood_opacity = flood_opacity
        self.font_family = font_family
        self.font_size = font_size
        self.font_size_adjust = font_size_adjust
        self.font_stretch = font_stretch
        self.font_style = font_style
        self.font_variant = font_variant
        self.font_weight = font_weight
        self.glyph_orientation_horizontal = glyph_orientation_horizontal
        self.glyph_orientation_vertical = glyph_orientation_vertical
        self.image_rendering = image_rendering
        self.kerning = kerning
        self.letter_spacing = letter_spacing
        self.lighting_color = lighting_color
        self.marker_end = marker_end
        self.marker_mid = marker_mid
        self.marker_start = marker_start
        self.mask = mask
        self.opacity = opacity
        self.overflow = overflow
        self.pointer_events = pointer_events
        self.shape_rendering = shape_rendering
        self.stop_color = stop_color
        self.stop_opacity = stop_opacity
        self.stroke = stroke
        self.stroke_dasharray = stroke_dasharray
        self.stroke_dashoffset = stroke_dashoffset
        self.stroke_linecap = stroke_linecap
        self.stroke_linejoin = stroke_linejoin
        self.stroke_miterlimit = stroke_miterlimit
        self.stroke_opacity = stroke_opacity
        self.stroke_width = stroke_width
        self.text_anchor = text_anchor
        self.text_decoration = text_decoration
        self.text_rendering = text_rendering
        self.transform = transform
        self.transform_origin = transform_origin
        self.unicode_bidi = unicode_bidi
        self.vector_effect = vector_effect
        self.visibility = visibility
        self.word_spacing = word_spacing
        self.writing_mode = writing_mode


class TransformMixin:
    def __init__(
        self,
        matrix=None,
        translate=None,
        scale=(1, 1),
        rotate=None,
        skewx=None,
        skewy=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.matrix = matrix
        self.translate = translate
        self.scale = Coords(*scale)
        self.rotate = rotate
        self.skewx = skewx
        self.skewy = skewy
