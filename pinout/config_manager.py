import collections.abc
import importlib.resources
from pathlib import Path
import types

from pinout import manager_files as io


def load_module(package, resource):
    config_path_manager = importlib.resources.path(package, resource)
    with config_path_manager as file_path:
        config_modules.insert(0, io.import_source_file("config", file_path))


def add_file(src):
    src = Path(src)
    config_modules.insert(0, io.import_source_file(src.stem, src.name))


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
    for cfg in config_modules:
        if hasattr(cfg, attr):
            instances.insert(0, getattr(cfg, attr))
            # return getattr(cfg, attr)

    while instances:
        update(merged_config, instances.pop())
    # warnings.warn(f"'{attr}' not found in config.")
    return merged_config


##################################################
#
# Init config
#
##################################################
# Config module that accepts attrs set from within a pinout script
adhoc_config = types.ModuleType("adhoc_config")

config_modules = [adhoc_config]
load_module("pinout.resources.config", "default_config.py")
