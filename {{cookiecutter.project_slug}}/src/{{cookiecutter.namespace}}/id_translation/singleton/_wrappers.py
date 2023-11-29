"""Convenience functions using the :class:`id_translation.Translator` singleton."""

from .. import config
from ._singleton import get_singleton
from ._wrap import wrap


@wrap(config.TRANSLATOR_TYPE.translate)
def translate(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().translate(*args, **kwargs)


@wrap(config.TRANSLATOR_TYPE.translated_names)
def translated_names(*args, **kwargs):
    """Docstring will be generated."""
    return get_singleton().translated_names(*args, **kwargs)


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


if hasattr(config.TRANSLATOR_TYPE, "go_offline"):

    @wrap(config.TRANSLATOR_TYPE.go_offline)
    def go_offline(*args, **kwargs):
        """Docstring will be generated."""
        return get_singleton().go_offline(*args, **kwargs)

elif hasattr(config.TRANSLATOR_TYPE, "store"):

    @wrap(config.TRANSLATOR_TYPE.store)
    def go_offline(*args, **kwargs):
        """Docstring will be generated."""
        # TODO: Remove this for 1.0.0
        return get_singleton().store(*args, **kwargs)  # type: ignore[attr-defined]
