# File Manager: common file manipulation functions
from pathlib import Path

def unique_filepath(filepath):
    filepath = Path(filepath)
    suffix = filepath.suffix
    name = filepath.name[:-len(filepath.suffix)]
    path = filepath.parent
    count = 0

    while filepath.is_file():
        count += 1
        filepath = Path('{}/{}_{}{}'.format(path, name, count, suffix))
    return filepath