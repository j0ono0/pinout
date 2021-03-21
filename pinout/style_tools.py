import io
import random
import math
from pathlib import Path
from .components import Pin, Label
from .templates import stylesheet
from . import file_manager
    
def luminace(color_component):
    """Luminance of an individual Red, Green, or Blue, color component.

    :param color_component: Value between 0 and 255 (inclusive)
    :type color_component: int
    :return: Luminance value of the color component
    :rtype: float
    """
    i = float(color_component) / 255 

    if i < 0.03928:
        return i / 12.92
    else:
        return (( i + 0.055 ) / 1.055 ) ** 2.4
    
def relative_luminance(rgb):
    """Normalised luminance value of an RGB color.

    :param rgb: Tuple (or List) representing RGB value.
    :type rgb: tuple
    :return: Value between 0 and 1.
    :rtype: float
    """
    return 0.2126 * luminace(rgb[0]) + 0.7152 * luminace(rgb[1]) + 0.0722 * luminace(rgb[2]) 

def random_contrasting_rgb(ref_color):
    """Generate a psudo-random color that, compared to 'ref_color', has a contrast ratio greater than 3. This contrast value is the minimum value to pass WCAG AA contrast recommendation for UI components. 

    :param ref_color: Tuple (or List) representing RGB value.
    :type ref_color: tuple
    :return: Tuple representing an RGB color.
    :rtype: tuple
    """
    contrast = 0
    while contrast < 3:
        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        lt = ref_color if sum(ref_color) > sum(rgb) else rgb
        dk = ref_color if sum(ref_color) < sum(rgb) else rgb
        contrast = ( relative_luminance(lt) + 0.05 ) / ( relative_luminance(dk) + 0.05 )
    return rgb

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