from jinja2 import Environment, PackageLoader, select_autoescape

# Filters

"""
def rgb(rgb_color):
    #
    # NOTE: Inkscape does not support rgb color!!!
    #
    # Convert RGB to hex

    hex_color = "#"
    for val in rgb_color[:3]:
        hex_color += ("0" + hex(val).split("x")[-1])[-2:]
    return hex_color
    
# Add filters to Jinja env
env.filters["rgb"] = rgb
"""

env = Environment(
    loader=PackageLoader("pinout", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def get(template_name):
    return env.get_template(template_name)
