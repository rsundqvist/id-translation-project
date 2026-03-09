"""Convenience functions using the :class:`~id_translation.Translator` singleton."""

from ._singleton import get_singleton
from ._wrappers import (
    extract_names,
    fetch,
    go_offline,
    initialize_sources,
    map,
    map_scores,
    translate,
    translated_names,
)

__all__ = [
    "translate",
    "translated_names",
    "extract_names",
    "map",
    "map_scores",
    "fetch",
    "initialize_sources",
    "go_offline",
    "get_singleton",
]
