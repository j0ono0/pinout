# File Manager: common file manipulation functions
from pathlib import Path

def unique_filepath(filepath):
    """Generate a unique filename to ensure existing files are not overwritten.

    :param filepath: File-name, including path, to the file location
    :type filepath: str
    :return: Unique filepath (filename and path to file location)
    :rtype: str
    """
    filepath = Path(filepath)
    suffix = filepath.suffix
    name = filepath.name[:-len(filepath.suffix)]
    path = filepath.parent
    count = 0

    while filepath.is_file():
        count += 1
        filepath = Path('{}/{}_{}{}'.format(path, name, count, suffix))
    return filepath


def export_file(content, path, overwrite=False):
    if isinstance(path, str):
        path = Path(path)
    if not overwrite:
        path = unique_filepath(path)
    path.touch(exist_ok=True)
    path.write_text(content)
    return path