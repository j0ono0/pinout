import collections.abc
import importlib.resources
from pathlib import Path
import types

from pinout import manager_files as io


def load_module(package, resource):
    config_path_manager = importlib.resources.path(package, resource)
    with config_path_manager as file_path:
        config_modules.insert(-1, io.import_source_file("config", file_path))


def add_file(src):
    src = Path(src)
    config_modules.insert(-1, io.import_source_file(src.stem, src.name))


def add_dict(name, value):
    setattr(adhoc_config, name, value)


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def get(attr):
    merged_config = {}
    instances = []
    for module in config_modules:
        try:
            cfg = getattr(module, "config")
            if attr == "config":
                instances.insert(0, cfg)
            else:
                instances.insert(0, cfg[attr])
        except KeyError:
            pass  # No attr present in config dict
        except AttributeError:
            # No config dict.
            # Module likely to be legacy format:
            # Each config dict is its own attribute
            if hasattr(module, attr):
                instances.insert(0, getattr(module, attr))

    while instances:
        update(merged_config, instances.pop())
    return merged_config


def init():
    global adhoc_config, config_modules
    # adhoc_config used for variable added directly via script
    adhoc_config = types.ModuleType("adhoc_config")
    config_modules = [adhoc_config]
    load_module("pinout.resources.config", "default_config.py")


##################################################
#
# initialize config on module load
#
##################################################

init()
