"""Configuration constants."""
from pathlib import Path as _Path

from id_translation import Translator as _Translator

_config_root = _Path(__file__).parent.joinpath("config/")

MAIN_CONFIGURATION_PATH = _config_root.joinpath("main.toml")
"""Contains all configuration which is not specific to a single fetcher."""
FETCHING_CONFIGURATION_PATHS = list(_config_root.glob("fetching/*.toml"))
"""Contains configuration for sources, typically databases."""
CACHE_DIR = _Path.home().joinpath(".big_corporation_inc/id-translation/")
"""Location of the persistent ``Translator`` instance.

This variable determines where the ``Translator`` instance created by
:func:`big_corporation_inc.id_translation.load_cached_translator`
is placed. If ``Fetcher``-specific caching is used as well, this data is
stored in ``~/.big_corporation_inc/id-translation/cached-fetcher-data/``.

Combining ``Translator`` and ``Fetcher`` caching has its use cases, but
should be done with care as calls to :meth:`id_translation.Translator.store`
does NOT invalidate the individual ``Fetcher`` caches.
"""

# TRANSLATOR_IMPLEMENTATION = customization.translator.CustomTranslator
TRANSLATOR_IMPLEMENTATION = _Translator
"""The Translator implementation to use. There's usually little reason to change this."""
