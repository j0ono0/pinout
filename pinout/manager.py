# Pinout Manager: management and utility functions

import argparse
import importlib
from pathlib import Path
import pkg_resources


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
    if isinstance(path, str):
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


################################################################
#
# Argparse functions
#
################################################################


def get_instance(module_name, instance_name="diagram"):
    module = importlib.import_module(module_name)
    return getattr(module, instance_name)


def create_stylesheet(module_name, path, instance_name="diagram", overwrite=False):
    """Create a stylesheet if none supplied."""
    from pinout import config, style_tools, templates
    from pinout.components.annotation import AnnotationLabel
    from pinout.components.layout import Panel
    from pinout.components.legend import Legend
    from pinout.components.pinlabel import PinLabel
    from pinout.components.integrated_circuits import DIP, QFP

    diagram = get_instance(module_name, instance_name)

    # Extract css class tags from PinLabels
    lbls = diagram.find_children_by_type(diagram, PinLabel)
    tags = list(set([tag for label in lbls for tag in label.tag.strip().split(" ")]))
    if config.pinlabel["tag"] in tags:
        tags.remove(config.pinlabel["tag"])

    context = {}
    if tags:
        context["tags"] = style_tools.assign_color(tags)
        context["pinlabel"] = config.pinlabel
    if diagram.find_children_by_type(diagram, Legend):
        context["legend"] = config.legend
    if diagram.find_children_by_type(diagram, Panel):
        context["panel"] = config.panel
    if diagram.find_children_by_type(diagram, AnnotationLabel):
        context["annotation"] = config.annotation
    if diagram.find_children_by_type(diagram, DIP):
        context["ic_dip"] = config.ic_dip
    if diagram.find_children_by_type(diagram, QFP):
        context["ic_qfp"] = config.ic_qfp

    css_tplt = templates.get("stylesheet.j2")
    css = css_tplt.render(css=context)

    # Export stylesheet file
    if not overwrite:
        path = unique_filepath(path)
    with open(path, "w") as f:
        f.write(css)

    print(f"Stylesheet created: '{path}'")
    print(
        f"To use insert the following line into '{module_name}.py' after '{instance_name}' is declared:"
    )
    print(f"{instance_name}.add_stylesheet('{path}')")


def duplicate(resource_name):
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
        "config": [("config.py",)],
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

    diagram = get_instance(src, instance_name)

    path = Path(dest)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not overwrite:
        path = unique_filepath(path)
    path.touch(exist_ok=True)

    # Render final SVG file
    path.write_text(diagram.render())
    print(f"'{path}' exported successfully.")


def __main__():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--duplicate",
        action="store",
        choices=["quick_start", "config"],
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

    args = parser.parse_args()
    if args.duplicate:
        duplicate(args.duplicate)

    if args.export:
        export_diagram(*args.export, overwrite=args.overwrite)

    if args.css:
        print(args)
        create_stylesheet(*args.css, overwrite=args.overwrite)


if __name__ == "__main__":
    __main__()