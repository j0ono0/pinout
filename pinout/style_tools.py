import random


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


def unique_contrasting_rgb(ref_color):
    """Generate a psudo-random color that, compared to 'ref_color', has a contrast ratio greater than 3. This contrast value is the minimum value to pass WCAG AA contrast recommendation for UI components.

    :param ref_color: Tuple (or List) representing RGB value.
    :type ref_color: tuple
    :return: Tuple representing an RGB color.
    :rtype: tuple
    """
    contrast = 0
    unique = False
    while contrast < 3 and not unique:
        rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        lt = ref_color if sum(ref_color) > sum(rgb) else rgb
        dk = ref_color if sum(ref_color) < sum(rgb) else rgb
        contrast = (relative_luminance(lt) + 0.05) / (relative_luminance(dk) + 0.05)
        unique = is_distinct_rbg(rgb)
    palette.append(rgb)
    return rgb


def is_distinct_rbg(rgb_color, threshold=30):
    r, g, b = rgb_color
    for (pr, pg, pb) in palette:
        diff = abs(r - pr) + abs(g - pg) + abs(b - pb)
        if diff > threshold:
            return False
    return True


def assign_color(tag_list, ref_color=(0, 0, 0)):
    """Generate a stylesheet using metrics from a diagram. Various styles are tailored by making a *best-guess* based on diagram component dimensions or a *lucky-guess* filtered by preset criteria. The output should be considered a boot-strapping step to styling a diagram ...unless you feel lucky!

    :param diagram: The Diagram object requiring styling
    :type diagram: Diagram
    :return: content of a css stylesheet with all required styles to display a diagram.
    :rtype: str
    """

    # Assign random-ish color to each tag
    return [(tag, unique_contrasting_rgb(ref_color)) for tag in tag_list]


# Store created color for reference
palette = []