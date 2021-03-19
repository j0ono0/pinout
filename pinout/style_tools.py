import io
import random
import math
from pathlib import Path
from .components import Pin, Label
from .templates import stylesheet

    
def luminace(color_component):
    i = float(color_component) / 255 

    if i < 0.03928:
        return i / 12.92
    else:
        return (( i + 0.055 ) / 1.055 ) ** 2.4
    
def relative_luminance(rgb):
    return 0.2126 * luminace(rgb[0]) + 0.7152 * luminace(rgb[1]) + 0.0722 * luminace(rgb[2]) 

def random_contrasting_rgb(ref_color):
    contrast = 0
    while contrast < 3:
        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        lt = ref_color if sum(ref_color) > sum(rgb) else rgb
        dk = ref_color if sum(ref_color) < sum(rgb) else rgb
        contrast = ( relative_luminance(lt) + 0.05 ) / ( relative_luminance(dk) + 0.05 )
    return rgb

def export_default_css(style_data, svgpath, overwrite=False):
    cssname = svgpath.name[:-len(svgpath.suffix)]
    csspath = Path(svgpath.parent, '{}.css'.format(cssname))
    if not overwrite:
        # Ensure filename is unique
        count = 0
        while csspath.is_file():
            count += 1
            csspath = Path(svgpath.parent, '{}_{}.css'.format(cssname, count))
    
    csspath.touch(exist_ok=True)
    csspath.write_text(style_data)
    return csspath

def default_css(diagram):
    labels = [[l.tags for l in c.labels] for c in diagram.components if isinstance(c, Pin)]
    labelset = set([tag for lbl in labels for tag in lbl])
    
    label_font_size = math.floor(Label.default_height * (3/5))
    label_text_color = (255,255,255)
    
    return stylesheet.render(
        legend = [(l.capitalize(), l, 'rgb' + str(random_contrasting_rgb(label_text_color))) for l in labelset],
        legend_font_size = max(13, label_font_size),
        label_font_size = label_font_size,
        label_text_color = 'rgb' + str(label_text_color),
    )