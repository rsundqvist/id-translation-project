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

from id_translation import utils as _tmp

# Attribute id_translation warnings to the caller, past the wrappers in this package.
_tmp.add_skip_file_prefix(__file__.removesuffix("__init__.py"))
del _tmp
