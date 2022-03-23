import collections.abc
import importlib.resources
from pathlib import Path
import types
import json

from pinout import manager_files as io


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def load_module(package, resource):
    config_path_manager = importlib.resources.path(package, resource)
    with config_path_manager as file_path:
        config_modules.insert(-1, io.import_source_file("config", file_path))


def add_file(src):
    src = Path(src)
    config_modules.insert(-1, io.import_source_file(src.stem, src.name))


def add_dict(name, value):
    setattr(adhoc_config, name, value)


##########################################################


def add_json(src):
    data = json.loads(io.load_data(src))
    update(config_dict, data)


def set(data_dict):
    update(config_dict, data_dict)


def add_config_from_package(src):
    set(json.loads(io.import_file_from_package(src)))


def get(attr=None):
    if not attr:
        return config_dict
    data = config_dict
    for key in attr.split("."):
        data = data[key]
    return data


##########################################################


def init():
    global adhoc_config, config_modules, config_dict
    # adhoc_config used for variable added directly via script
    adhoc_config = types.ModuleType("adhoc_config")
    config_modules = [adhoc_config]
    load_module("pinout.resources.config", "default_config.py")

    config_dict = json.loads(
        io.import_file_from_package("resources/config/default_config.json")
    )


##################################################
#
# initialize config on module load
#
##################################################

init()
