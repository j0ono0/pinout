from jinja2 import Environment, PackageLoader, select_autoescape

# Filters


def rgba(rgba_list):
    # cater for rgb attribute with no alpha value
    color = dict(zip(("r", "g", "b", "a"), rgba_list))
    return f"rgba({color['r']}, {color['g']}, {color['b']}, {color.get('a', 1)})"


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
