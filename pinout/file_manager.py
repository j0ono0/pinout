# File Manager: common file manipulation functions
from pathlib import Path
import pkg_resources
import yaml


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


def load_config(path=None):
    """Load a config file either from a user nominated location or, if no path is supplied, load the default config file from the *pinout* package.

    :param path: [description], defaults to None
    :type path: [type], optional
    :return: [description]
    :rtype: [type]
    """
    if path is None:
        # Load default settings
        path = "resources/config.yaml"
        return yaml.safe_load(
            pkg_resources.resource_string(__name__, path).decode("utf-8")
        )
    # Load user supplied settings
    path = Path(path)
    with path.open() as f:
        return yaml.safe_load(f)


def duplicate(resource_name):
    """Duplicate resources from *pinout* package.

    A variety of resources can be copied via this function. Access is also available via the command line::

        py -m pinout.file_manager --duplicate <resource_name>

    Where :code:`<resource_name>` can be any one of the following resources:

        + config
        + quick_start
        + full_sample

    :param resource_name: Name of resource to duplicate.
    :type resource_name: string
    """

    resources = {
        "config": [(".", "config.yaml")],
        "quick_start": [
            ("quick_start", "quick_start_config.yaml"),
            ("quick_start", "quick_start_config_tags.yaml"),
            ("quick_start", "quick_start_hardware.png"),
            ("quick_start", "quick_start_pinout.py"),
        ],
        "full_sample": [
            ("full_sample", "full_sample_config.yaml"),
            ("full_sample", "full_sample_hardware.png"),
            ("full_sample", "full_sample_pinout.py"),
        ],
    }

    resource_package = "pinout"
    for path in resources[resource_name]:
        resource_path = "/".join(("resources", *path))
        data = pkg_resources.resource_string(resource_package, resource_path)
        filename = path[-1]
        with open(filename, "wb") as f:
            f.write(data)
        print(f"{filename} duplicated.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--duplicate",
        action="store",
        choices=["quick_start", "full_sample", "config"],
        help="duplicate pinout resources",
    )
    args = parser.parse_args()
    if args.duplicate:
        duplicate(args.duplicate)