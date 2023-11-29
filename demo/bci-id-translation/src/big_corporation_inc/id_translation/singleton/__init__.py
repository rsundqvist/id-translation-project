"""Convenience functions using the :class:`~id_translation.Translator` singleton."""

from ._singleton import get_singleton
from ._wrappers import fetch, go_offline, map, map_scores, translate, translated_names

__all__ = [
    "translate",
    "translated_names",
    "map",
    "map_scores",
    "fetch",
    "go_offline",
    "get_singleton",
]
