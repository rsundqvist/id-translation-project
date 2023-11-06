import functools
from typing import List, Dict

from id_translation.types import SourceType

from . import config
from ._initialize import create_translator

SINGLETON = None


@functools.wraps(config.TRANSLATOR_IMPLEMENTATION.translate)
def translate(*args, **kwargs):
    return _get_singleton().translate(*args, **kwargs)


@functools.wraps(config.TRANSLATOR_IMPLEMENTATION.translated_names)
def translated_names(*args, **kwargs):
    return _get_singleton().translated_names(*args, **kwargs)


@functools.wraps(config.TRANSLATOR_IMPLEMENTATION.map)
def map(*args, **kwargs):
    return _get_singleton().map(*args, **kwargs)


@functools.wraps(config.TRANSLATOR_IMPLEMENTATION.map_scores)
def map_scores(*args, **kwargs):
    return _get_singleton().map_scores(*args, **kwargs)


def get_sources_and_placeholders() -> Dict[SourceType, List[str]]:
    """Returns a dict ``{table: [columns..]}.``"""
    return _get_singleton().placeholders


def _get_singleton():
    global SINGLETON
    if SINGLETON is None:
        SINGLETON = create_translator()
    assert SINGLETON.online, "This should not happen! What did you do?"

    return SINGLETON
