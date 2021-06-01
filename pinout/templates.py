from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("pinout", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def get(template_name):
    return env.get_template(template_name)
