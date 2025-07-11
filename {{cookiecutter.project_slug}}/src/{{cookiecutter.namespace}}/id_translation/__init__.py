"""Translation of IDs found in {{cookiecutter.organization}} databases.

The most important functions are reexported here (:mod:`{{cookiecutter.namespace}}.id_translation`). See the various
submodules (navigation bar at the top) for complete documentation.
"""

from ._initialize import create_translator, load_cached_translator
from .singleton import get_singleton, translate

__all__ = [
    # Reexport convenience functions
    "get_singleton",
    "translate",
    # Reexport initialization functions
    "create_translator",
    "load_cached_translator",
]

from ._configure import configure_lib, configure_wrapper

configure_lib()
configure_wrapper()
del configure_lib, configure_wrapper
