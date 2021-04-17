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


def update_config(dest, src):
    for key, val in src.items():
        if type(val) == dict:
            update_config(dest[key], src[key])
        else:
            dest[key] = val


def load_config(path):
    path = Path(path)
    with path.open() as f:
        update_config(cfg, yaml.safe_load(f))


# Load default settings
path = "resources/config.yaml"
cfg = yaml.safe_load(pkg_resources.resource_string(__name__, path).decode("utf-8"))