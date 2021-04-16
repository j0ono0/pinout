import io
import math
import random
from pathlib import Path

from . import file_manager
from . import components
from .components import cfg
from .templates import stylesheet


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
        return ((i + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    """Normalised luminance value of an RGB color.

    :param rgb: Tuple (or List) representing RGB value.
    :type rgb: tuple
    :return: Value between 0 and 1.
    :rtype: float
    """
    return (
        0.2126 * luminace(rgb[0])
        + 0.7152 * luminace(rgb[1])
        + 0.0722 * luminace(rgb[2])
    )


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
        contrast = (relative_luminance(lt) + 0.05) / (relative_luminance(dk) + 0.05)
    return rgb


def find_children_by_type(component, target_type):
    results = []
    try:
        for c in component.children:
            if isinstance(c, target_type):
                results.append(c)
            results += find_children_by_type(c, target_type)
    except AttributeError:
        """ No children """

    return results


def default_css(diagram):
    """Generate a stylesheet using metrics from a diagram. Various styles are tailored by making a *best-guess* based on diagram component dimensions or a *lucky-guess* filtered by preset criteria. The output should be considered a boot-strapping step to styling a diagram ...unless you feel lucky!

    :param diagram: The Diagram object requiring styling
    :type diagram: Diagram
    :return: content of a css stylesheet with all required styles to display a diagram.
    :rtype: str
    """
    # Extract css class tags from PinLabels
    pinlabels = find_children_by_type(diagram, components.PinLabel)
    pinlabel_tags = list(
        set([tag for label in pinlabels for tag in label.tags.split(" ")])
    )
    # Remove config tag (common to all PinLabels)
    try:
        pinlabel_tags.remove(cfg.get("pinlabel", {}).get("tag", ""))
    except ValueError:
        pass

    label_font_size = cfg.get("pinlabel", {}).get(
        "font_size", math.floor(cfg["pinlabel"]["box"]["height"] * (3 / 5))
    )
    label_text_color = tuple(
        cfg.get("pinlabel", {}).get("text", {}).get("color", (255, 255, 255))
    )

    pinlabel_categories = {
        label: random_contrasting_rgb(label_text_color) for label in pinlabel_tags
    }

    return stylesheet.render(
        {
            "diagram": cfg["diagram"],
            "pinlabel": cfg["pinlabel"],
            "pinlabel_categories": pinlabel_categories,
            "pinlabelrow": cfg["pinlabelrow"],
            "legend": cfg["legend"],
            "leaderline": cfg["leaderline"],
        }
    )
