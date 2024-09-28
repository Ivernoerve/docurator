import pkgutil
import importlib
import os

def invoke_modules(path: str) -> None:
    """Invokes modules starting at the gicen path.

    Args:
        path (str): A path pointing to the root of the modules to invoke.
    """
    abs_path = os.path.abspath(path)
    
    for mod in pkgutil.walk_packages([abs_path]):
        try:   
            importlib.import_module(mod.name)
        except ModuleNotFoundError as e:
            print(f"Failed to import {mod.name}: {e}")
