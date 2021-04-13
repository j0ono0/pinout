from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("pinout", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

# Base SVG elements
svg = env.get_template("svg.svg")
svg_group = env.get_template("group.svg")
svg_image = env.get_template("image.svg")
svg_style = env.get_template("style.svg")
svg_rect = env.get_template("rect.svg")

# CSS styles
stylesheet = env.get_template("stylesheet.css")

# Component SVG templates (made from multiple svg elements)
svg_label = env.get_template("label.svg")
svg_annotation = env.get_template("annotation.svg")

svg_line = env.get_template("line.svg")
svg_textblock = env.get_template("textblock.svg")
