import importlib
import sys

from types import ModuleType
from typing import Callable


def load_module(module_name: str) -> ModuleType:
    """
    Import the python module with the provided `module_name`.

    :param module_name: the fully qualified module name.
    :type module_name: str.

    :returns: loaded module.
    :rtype: ModuleType.
    """
    return importlib.import_module(module_name)


def unload_module(module_name: str):
    """
    Remove the python module with the provided `module_name` from python path.

    :param module_name: the fully qualified module name.
    :type module_name: str.
    """
    sys.modules.pop(module_name)


def reload_module(qualified_module_name: str) -> ModuleType:
    unload_module(qualified_module_name)
    return load_module(qualified_module_name)
