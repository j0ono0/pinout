import re
from typing import Type
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("pinout", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def get(template_name):
    return env.get_template(template_name)


def to_num(val):
    if "." in val:
        return float(val)
    return int(val)


def calc_units(val, dst_units):
    """Convert value from src_units to dst_units"""

    if type(val) in [int, float]:
        return val

    dst_units = dst_units.strip().lower()
    val = val.strip().lower()

    src_units = re.search(r"([a-zA-Z]+$)", val.strip()).groups()[0]
    val = to_num(re.search(r"(^[0-9]+)", val).groups()[0])

    # units already match return val as a number
    if src_units == dst_units:
        return val

    conversion = {
        "pt": {
            "mm": 0.330,
            "cm": 0.033,
            "in": 0.014,
            "pt": 1,
        },
        "mm": {
            "mm": 1,
            "cm": 0.1,
            "in": 0.394,
            "pt": 2.835,
        },
        "cm": {
            "mm": 10,
            "cm": 1,
            "in": 0.039,
            "pt": 28.35,
        },
        "in": {
            "mm": 25.40,
            "cm": 2.540,
            "in": 1,
            "pt": 96,  # SVG renders at 96dpi in firefox - using that as reference
        },
    }

    return f"calc({val}{src_units} * {conversion[src_units][dst_units]})"


env.globals.update(calc_units=calc_units)
