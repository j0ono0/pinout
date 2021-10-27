# Some experiments parsing kicad file with the
# thought of extracting location data for pinout modules.

from tokenize import tokenize, NUMBER, LPAR, RPAR, OP, NAME

# Generator that yields text file as tokens
def file_tokenizer(filepath):
    with open(filepath, "rb") as f:
        tokens = tokenize(f.readline)
        for token in tokens:
            yield token


def parse_fp_text(td):
    # Parse just the reference and value
    key = next(td).string.strip('"')
    value = next(td).string.strip('"')
    scan_to_item_end(td)
    return (key, value)


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


def get_module_identifiers(td):
    token = next(td)
    start = token.start[1]
    line = token.line
    while token.exact_type not in [LPAR, RPAR]:
        token = next(td)
    end = token.start[1]
    return line[start:end].strip().split(":", 1)


def parse_module(td):
    # Parsing only attributes required for pinout:
    # 'at': coordinates of the module instance
    # 'fp_text': reference and value assigned to the module instance
    module = {"library": None, "footprint": None, "at": None, "fp_text": {}}

    # get library and footprint names
    lib, fp = get_module_identifiers(td)
    module["library"] = lib
    module["footprint"] = fp

    # Collect required module attributes
    token = next(td)
    while token.string != ")":

        # Start a new dict item
        if token.type == NAME:
            key = token.string

            if key == "fp_text":
                k, v = parse_fp_text(td)
                if k in module["fp_text"]:
                    # Convert string to list for multiple attr with same name
                    if isinstance(module["fp_text"], list):
                        module["fp_text"][k].append(v)
                    else:
                        module["fp_text"][k] = [module["fp_text"], v]
                else:
                    module["fp_text"][k] = v

            elif key == "at":
                x, y = parse_at(td)[:2]
                module[key] = [x, y]

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


def scale_module_coords(modules, dpi):
    for module in modules:
        x, y = module["at"]
        module["at"] = [v / 25.4 * dpi for v in module["at"]]


def translate_module_origins(modules, origin_ref):
    # Find origin coords
    for mod in modules:
        if mod["fp_text"]["value"] == origin_ref:
            ox, oy = mod["at"]
    # Translate all coords making origin (0,0)
    for mod in modules:
        x, y = mod["at"]
        mod["at"] = [x - ox, y - oy]


def parse_pinout_modules(pcb_file, dpi=None):
    # scale: dpi resolution of pcb image
    modules = parse_modules(pcb_file)
    if dpi:
        scale_module_coords(modules, dpi)
    # TODO: move origin ref to config
    translate_module_origins(modules, "origin")
    return [
        {"name": m["fp_text"]["value"], "coords": m["at"]}
        for m in modules
        if m["library"] == "pinout"
    ]
