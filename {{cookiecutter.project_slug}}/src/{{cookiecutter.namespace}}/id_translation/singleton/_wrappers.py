"""Convenience functions using the :class:`id_translation.Translator` singleton."""

from ._singleton import get_singleton
from ._wrap import wrap
from .. import config


@wrap(config.TRANSLATOR_TYPE.initialize_sources)
def initialize_sources(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().initialize_sources(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.translate)
def translate(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().translate(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.translated_names)
def translated_names(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().translated_names(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.extract_names)
def extract_names(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().extract_names(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.map)
def map(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().map(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.map_scores)
def map_scores(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().map_scores(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.fetch)
def fetch(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().fetch(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.go_offline)
def go_offline(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().go_offline(*args, **kwargs)
