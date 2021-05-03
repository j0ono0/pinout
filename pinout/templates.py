from jinja2 import Environment, PackageLoader, select_autoescape

# Filters


def rgb(rgb_color):
    #
    # NOTE: Inkscape does not support rgb color!!!
    #
    # Convert RGB to hex

    hex_color = "#"
    for val in rgb_color[:3]:
        hex_color += ("0" + hex(val).split("x")[-1])[-2:]
    return hex_color


env = Environment(
    loader=PackageLoader("pinout", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

# Add filters to Jinja env
env.filters["rgb"] = rgb

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
