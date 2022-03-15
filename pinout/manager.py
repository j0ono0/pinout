# Pinout Manager: management and utility functions

import argparse
import collections.abc
from multiprocessing.sharedctypes import Value
import os
from pathlib import Path
import pkg_resources
import sys

from pinout import core
from pinout import manager_files as io
from pinout import config_manager

try:
    import cairosvg
except ImportError as e:
    pass
    # export as other (non svg) formats is not available

# user variables
# C:\Program Files\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0\mingw64\bin

# env variables
# C:\Program Files\GTK3-Runtime Win64\bin


def unique_filepath(filepath):
    """Generate a unique filename to ensure existing files are not overwritten.

    :param filepath: File-name, including path, to the file location
    :type filepath: str
    :return: Unique filepath (filename and path to file location)
    :rtype: str
    """
    filepath = Path(filepath)
    suffix = filepath.suffix
    name = filepath.name[: -len(filepath.suffix)]
    path = filepath.parent
    count = 0

    while filepath.is_file():
        count += 1
        filepath = Path("{}/{}_{}{}".format(path, name, count, suffix))
    return filepath


def export_file(content, path, overwrite=False):
    """Create a file and export content to it. If overwrite is False a new filename is generated.

    :param content: Text data to be written to file
    :type content: str
    :param path: Path, including filename, for the file to be created
    :type path: str
    :param overwrite: Dictate if an existing file should be overwritten. If False 'path' is amended to be a unique filename, defaults to False
    :type overwrite: bool, optional
    :return: Actual path the file was written to. Note: this may differ from supplied 'path' if 'overwrite' is False)
    :rtype: str
    """
    # convert path to Path object
    path = Path(path)

    if not overwrite:
        path = unique_filepath(path)
    path.touch(exist_ok=True)
    path.write_text(content)
    return path


def load_data(path):
    path = Path(path)
    with path.open() as f:
        return f.read()


# TODO: I think this function is duplicated in core.py - merge?
def update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


################################################################
#
# Argparse functions
#
################################################################


def get_diagram_instance(src, instance_name="diagram"):
    src = Path(src)
    user_module = io.import_source_file(src.stem, src.name)
    return getattr(user_module, instance_name)


def create_stylesheet(src, path, instance_name="diagram", overwrite=False):
    """Create a stylesheet if none supplied."""
    from pinout import style_tools, templates
    from pinout.components.annotation import AnnotationLabel
    from pinout.components.layout import Panel, Diagram_2Columns, Diagram_2Rows
    from pinout.components.legend import Legend
    from pinout.components.pinlabel import PinLabel
    from pinout.components.integrated_circuits import DIP, QFP

    # Save CWD and return to it and end of function
    # incase multiple diagrams are being built from a script
    init_dir = Path.cwd()

    src = Path(src)
    os.chdir(src.parent)
    sys.path.append("")

    diagram = get_diagram_instance(src, instance_name)

    # Extract css class tags from PinLabels
    lbls = diagram.find_children_by_type(diagram, PinLabel)
    tags = list(set([tag for label in lbls for tag in label.tag.strip().split(" ")]))
    try:
        tags.remove(config_manager.get("pinlabel")["tag"])
    except ValueError:
        # tag not present
        pass

    context = {}
    if tags:
        context["tags"] = style_tools.assign_color(tags)
        context["pinlabel"] = config_manager.get("pinlabel")
    if diagram.find_children_by_type(diagram, Legend):
        context["legend"] = config_manager.get("legend")
    if diagram.find_children_by_type(diagram, Panel):
        context["panel"] = config_manager.get("panel")
    if diagram.find_children_by_type(diagram, AnnotationLabel):
        context["annotation"] = config_manager.get("annotation")
    if diagram.find_children_by_type(diagram, DIP):
        context["ic_dip"] = config_manager.get("ic_dip")
    if diagram.find_children_by_type(diagram, QFP):
        context["ic_qfp"] = config_manager.get("ic_qfp")
    if isinstance(diagram, Diagram_2Columns) or isinstance(diagram, Diagram_2Rows):
        context["diagram_presets"] = config_manager.get("diagram_presets")

    css_tplt = templates.get("stylesheet.j2")
    css = css_tplt.render(css=context)

    # Return to folder script was launched from
    os.chdir(init_dir)

    # Export stylesheet file
    if not overwrite:
        path = unique_filepath(path)
    with open(path, "w") as f:
        f.write(css)

    print(f"Stylesheet created: '{path}'")
    print(
        f"To use insert the following line into '{src.name}' after '{instance_name}' is declared:"
    )
    print(f"{instance_name}.add_stylesheet('{path}')")


def duplicate(resource_name, *args):
    """Duplicate resources from *pinout* package.

    A variety of resources can be copied via this function, access is available via the command line::

        py -m pinout.manager --duplicate <resource_name>

    Where :code:`<resource_name>` can be any one of the following resources:

        + config
        + quick_start

    :param resource_name: Name of resource to duplicate.
    :type resource_name: string
    """

    resources = {
        "quick_start": [
            ("quick_start", "data.py"),
            ("quick_start", "hardware.png"),
            ("quick_start", "pinout_diagram.py"),
            ("quick_start", "styles.css"),
        ],
        "config": [
            ("config", "default_config.py"),
        ],
        "kicad": [("pinout_kicad_example.zip",)],
    }

    resource_package = "pinout"
    for path in resources[resource_name]:
        resource_path = "/".join(("resources", *path))
        data = pkg_resources.resource_string(resource_package, resource_path)
        filename = path[-1]
        with open(filename, "wb") as f:
            f.write(data)
        print(f"{filename} duplicated.")


def export_diagram(src, dest, instance_name="diagram", overwrite=False):

    # reset core.diagram_id.counter. Pytest can create multiple diagrams
    # and requires each new diagram's id counter to commence at 0.
    core.diagram_id.counter = 0

    # Save CWD and return to it and end of function
    # incase multiple diagrams are being built from a script
    init_dir = Path.cwd()

    # Save dest for consistent printing at end
    raw_dest = dest

    # Create 'dest' folder(s) and file - file must exist for Path.resolve() to function as expected.
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not overwrite:
        dest = unique_filepath(dest)
    dest.touch(exist_ok=True)
    # Convert 'dest' to absolute so CWD can be changed without affecting 'dest'.
    dest = dest.resolve()

    # Change CWD to folder 'src' module is located.
    # This allows pinout.manager to be invoked from any location
    # but keeps paths in the src script relative to that script.
    src = Path(src)
    os.chdir(src.parent)
    sys.path.append("")

    diagram = get_diagram_instance(src, instance_name)

    # Prepare linked media depending on output
    if dest.suffix == ".svg":
        # Update relative image.src to be relative to destination
        images = diagram.find_children_by_type(diagram, core.Image)
        for img in images:
            # Follow image references
            while isinstance(img.src, core.Image):
                img = img.src

            if not img.embed and not Path(img.src).is_absolute():
                img.src = os.path.relpath(
                    Path.cwd().joinpath(img.src), Path.cwd().joinpath(dest.parent)
                )

        # Update relative stylesheet.src to be relative to destination.
        stylesheets = diagram.find_children_by_type(diagram, core.StyleSheet)
        for css in stylesheets:
            if not css.embed and not css.src.is_absolute():
                css.src = os.path.relpath(
                    Path.cwd().joinpath(css.src), Path.cwd().joinpath(dest.parent)
                )
    else:
        # Embed styles - required for cairosvg to render correctly
        stylesheets = diagram.find_children_by_type(diagram, core.StyleSheet)
        for css in stylesheets:
            css.embed = True

    # Render final SVG file
    try:
        if dest.suffix == ".svg":
            dest.write_text(diagram.render())

        elif dest.suffix == ".png":
            cairosvg.svg2png(bytestring=diagram.render(), write_to=dest.as_posix())

        elif dest.suffix == ".pdf":
            cairosvg.svg2pdf(bytestring=diagram.render(), write_to=dest.as_posix())

        elif dest.suffix == ".ps":
            cairosvg.svg2ps(bytestring=diagram.render(), write_to=dest.as_posix())

        print(f"'{raw_dest}' exported successfully.")

    except Exception as e:
        print(f"The export falied! Error: {e}")
        raise

    # Return the CWD to the initial directory
    os.chdir(init_dir)


def create_kicad_lib(dest=".", config_file=None, version=None):
    from datetime import datetime
    from pinout import templates

    version = int(version or 6)

    # Load config and create library context
    if version >= 6:
        context = config_manager.get("kicad_6_footprints")
        context["component_type"] = "footprint"
    else:
        context = config_manager.get("kicad_5_footprints")
        context["component_type"] = "module"

    if config_file:
        context = update_dict(
            context, get_diagram_instance(config_file, "kicad_6_footprints")
        )

    context["timestamp"] = datetime.today().strftime("%Y%m%d")

    # Override config version if none supplied
    context["version"] = float(version) or float(context["version"])

    folder = Path(dest, "pinout.pretty")
    folder.mkdir(parents=True, exist_ok=True)
    footprints = ["Annotation", "Origin", "PinLabel"]

    for fp in footprints:
        tplt = templates.get(f"kicad_footprint_lib/{fp}.j2")
        filepath = folder / (fp + ".kicad_mod")
        with filepath.open(mode="w") as f:
            f.write(tplt.render(context))
    print("pinout footprint library for KiCad created successfully.")


def __main__():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--kicad_lib",
        action="store",
        nargs="+",
        help="Create KiCad footprint library. Example usage: python -m pinout.manager --kicad_lib <destination folder> <optional:config_file>",
    )

    parser.add_argument(
        "-d",
        "--duplicate",
        action="store",
        choices=["quick_start", "config", "kicad"],
        help="duplicate pinout resources",
    )

    parser.add_argument(
        "-e",
        "--export",
        nargs="+",
        action="store",
        help="example usage: python -m pinout.manager -e <module name> <export filename> [<instance name>]\n <instance name> defaults to 'diagram'",
    )

    parser.add_argument(
        "--css",
        nargs="+",
        action="store",
        help="example usage: python -m pinout.manager --css <module name> <export filename> [<instance name>]\n <instance name> defaults to 'diagram'",
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Enable file overwriting.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store",
        help="Accepts integer only. Example usage (with --kicad_lib): python -m pinout.manager --kicad_lib <destination folder> <optional:config_file> -v 6",
    )

    args = parser.parse_args()
    if args.duplicate:
        duplicate(args.duplicate, args.overwrite)

    if args.export:
        export_diagram(*args.export, overwrite=args.overwrite)

    if args.css:
        create_stylesheet(*args.css, overwrite=args.overwrite)

    if args.kicad_lib:
        create_kicad_lib(*args.kicad_lib, version=args.version)


if __name__ == "__main__":
    __main__()
