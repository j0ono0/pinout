# Some experiments parsing kicad file with the
# thought of extracting location data for pinout modules.
import math
from tokenize import tokenize, NUMBER, LPAR, RPAR, OP, NAME


class Counter:
    def __init__(self, start_num):
        self.count = start_num

    def __call__(self):
        self.count += 1
        return self.count


# from pinout import kicad_parser as kp
# kp.rotate_point_coord((10,0), (10,0), 180)
def rotate_point_coord(coord, rotate):
    """Rotate a coordinate around (0,0) by angle in degrees."""
    # Rotate in opposite direction to kicad for SVG coordinate space
    rotate = -rotate
    x, y = coord
    x1 = x * math.cos(math.radians(rotate)) - y * math.sin(math.radians(rotate))
    y1 = x * math.sin(math.radians(rotate)) + y * math.cos(math.radians(rotate))
    return (x1, y1)


# Generator that yields text file as tokens
def file_tokenizer(filepath):
    with open(filepath, "rb") as f:
        tokens = tokenize(f.readline)
        for token in tokens:
            yield token


def parse_fp_text(td):
    # fp_text name and value
    fp_text = {}
    token = next(td)
    key = token.string

    token = next(td)
    value = token.string.strip('"')

    fp_text[key] = value
    # "at" attribute
    while token.exact_type != RPAR:
        if token.exact_type == LPAR:
            if next(td).string == "at":
                fp_text["at"] = parse_at(td)
            else:
                scan_to_item_end(td)
        token = next(td)
    return fp_text


def parse_at(td):
    coords = []
    current = ""
    while True:
        token = next(td)
        if token.type == NUMBER:
            current += token.string
            coords.append(float(current))
            current = ""
        elif token.exact_type == RPAR:
            return coords
        elif token.type == OP:
            current += token.string


def scan_to_item_end(td):
    count = 1
    while count > 0:
        token = next(td)
        if token.exact_type == LPAR:
            count += 1
        elif token.exact_type == RPAR:
            count -= 1


def parse_module(td):
    # Parsing only attributes required for pinout:
    # 'at': coordinates of the module instance
    # 'fp_text': reference, value and user defined attributes (name, text, and coordinates)
    module = {
        "library": None,
        "footprint": None,
        "at": None,
        "reference": None,
        "value": None,
        "fp_text": [],
    }

    # Library
    token = next(td)
    module["library"] = token.string

    # Footprint
    token = next(td)
    start = token.end[1]
    line = token.line
    while token.exact_type not in [LPAR, RPAR]:
        token = next(td)
    end = token.start[1]
    module["footprint"] = line[start:end].strip()

    # 'at' and 'fp_text' attributes
    while token.exact_type != RPAR:

        # Start a new dict item
        if token.exact_type == LPAR:
            key = next(td).string

            if key == "fp_text":
                fpt = parse_fp_text(td)
                # Record 'reference' and 'value' in module dict for easy access
                # File other (ie 'user') fp_text list.
                if "reference" in fpt:
                    module["reference"] = fpt["reference"]
                elif "value" in fpt:
                    module["value"] = fpt["value"]
                else:
                    module["fp_text"].append(fpt)

            elif key == "at":
                module[key] = parse_at(td)

            else:
                scan_to_item_end(td)

        token = next(td)

    return module


def parse_modules(path):
    modules = []
    td = file_tokenizer(path)

    for token in td:
        if token.type == NAME and token.string == "module":
            modules.append(parse_module(td))
    return modules


def translate_module_origins(modules, origin_ref):
    # Find pinout origin coords
    pinout_origin_module = [mod for mod in modules if mod["reference"] == origin_ref][0]
    ox, oy = pinout_origin_module["coords"]

    # Translate all coords making origin (0,0)
    for mod in modules:
        coords = mod["coords"]
        coords[0] -= ox
        coords[1] -= oy
        mod["coords"] = coords


def get_pinout_modules(pcb_file, dpi=None):
    # scale: dpi resolution of pcb image
    modules = [mod for mod in parse_modules(pcb_file) if mod["library"] == "pinout"]
    # Provide each module with a unique id
    counter = Counter(0)
    for mod in modules:
        mod["id"] = counter()

    # Split module "at" into coords and orientation.
    # Apply orientation to components as rotation
    for mod in modules:
        mod["coords"] = mod["at"][:2]

        try:
            rotate = mod["at"][2]
        except IndexError:
            rotate = 0

        for fpt in mod["fp_text"]:
            rx, ry = rotate_point_coord(fpt["at"][:2], rotate)
            fpt["coords"] = [rx, ry]

    # Convert mm to dip
    if dpi:
        for mod in modules:
            mod["coords"] = [i / 25.4 * dpi for i in mod["coords"]]

            for fpt in mod["fp_text"]:
                fpt["coords"] = [i / 25.4 * dpi for i in fpt["coords"]]

    # TODO: move origin ref to config
    translate_module_origins(modules, "pinout_origin")
    return [m for m in modules if m["library"] == "pinout"]
