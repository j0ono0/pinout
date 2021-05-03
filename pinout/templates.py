from jinja2 import Environment, PackageLoader, select_autoescape

# Filters


def rgba(rgba_list):
    # cater for rgb attribute with no alpha value
    color = dict(zip(("r", "g", "b", "a"), rgba_list))

    #
    # Inkscape does not suppled rgb or rgba color!!!
    # return f"rgba({color['r']}, {color['g']}, {color['b']}, {color.get('a', 1)})"
    #

    # Convert to hex
    hex_color = "#"
    for val in rgba_list[:3]:
        hex_color += ("0" + hex(val).split("x")[-1])[-2:]
    return hex_color


env = Environment(
    loader=PackageLoader("pinout", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

# Add filters to Jinja env
env.filters["rgb"] = rgba
env.filters["rgba"] = rgba

# Base SVG elements
svg = env.get_template("svg.svg")
svg_group = env.get_template("group.svg")
svg_image = env.get_template("image.svg")
svg_rect = env.get_template("rect.svg")

# Component SVG templates (made from multiple svg elements)
svg_label = env.get_template("label.svg")
svg_annotation = env.get_template("annotation.svg")

svg_path = env.get_template("path.svg")
svg_text = env.get_template("text.svg")
svg_textblock = env.get_template("textblock.svg")
