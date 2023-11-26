"""Convenience functions using the :class:`~id_translation.Translator` singleton."""

from ._singleton import get_singleton
from ._wrappers import fetch, map, map_scores, translate, translated_names

__all__ = [
    "translate",
    "translated_names",
    "map",
    "map_scores",
    "fetch",
    "get_singleton",
]
