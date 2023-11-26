"""Convenience functions using the :class:`id_translation.Translator` singleton."""

from .. import config
from ._singleton import get_singleton
from ._wrap import wrap


@wrap(config.TRANSLATOR_TYPE.translate)
def translate(*args, **kwargs):
    """Docstring will be generated."""
    translator = get_singleton()
    return translator.translate(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.translated_names)
def translated_names(*args, **kwargs):
    """Docstring will be generated."""
    translator = get_singleton()
    return translator.translated_names(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.map)
def map(*args, **kwargs):
    """Docstring will be generated."""
    translator = get_singleton()
    return translator.map(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.map_scores)
def map_scores(*args, **kwargs):
    """Docstring will be generated."""
    translator = get_singleton()
    return translator.map_scores(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.fetch)
def fetch(*args, **kwargs):
    """Docstring will be generated."""
    translator: config.TRANSLATOR_TYPE = get_singleton()
    return translator.fetch(*args, **kwargs)
