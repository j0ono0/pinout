import importlib
import sys
import urllib.request
import pathlib


def import_source_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_data(src):
    """Load data from local file system or URL."""
    try:
        with open(src, "rb") as f:
            return f.read()
    except OSError:
        try:
            with urllib.request.urlopen(src) as f:
                return f.read()
        except urllib.error.HTTPError as e:
            print(e.code)


def import_file_from_package(src):
    src = pathlib.Path(src)
    module_path = "pinout." + src.parent.as_posix().replace("/", ".")
    module = importlib.import_module(module_path)
    return importlib.resources.read_text(module, src.name)
