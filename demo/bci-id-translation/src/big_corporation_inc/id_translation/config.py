"""Configuration constants."""
import typing as _t
from pathlib import Path as _Path
from uuid import UUID as _UUID

from id_translation import Translator as _Translator
from id_translation import fetching as _fetching

# from id_translation import types as _tt

# from big_corporation_inc.id_translation import customization as _customization

# IdType = _tt.IdTypes  # TODO(3.8, 3.9, 3.10) or 1.0.0
IdType = _t.Union[int, str, _UUID]
"""The kind of IDs we wish to translate."""
NameType: _t.TypeAlias = str
"""Type of names we wish to translate, such as a pandas.Dataframe column name."""
SourceType: _t.TypeAlias = NameType
"""Name types for sources, such as SQL table names."""

# TRANSLATOR_TYPE = _customization.StandardTranslator  # Uncomment to use custom implementation
TRANSLATOR_TYPE = _Translator[NameType, SourceType, IdType]
"""The Translator implementation to use."""

_config_root = _Path(__file__).parent.joinpath("config/")

MAIN_CONFIGURATION_PATH = _config_root.joinpath("main.toml")
"""Contains all configuration which is not specific to a single fetcher."""
FETCHING_CONFIGURATION_PATHS = list(_config_root.glob("fetching/*.toml"))
"""Contains configuration for sources, typically databases."""

BASE_CACHE_DIR = _Path.home().joinpath(".big_corporation_inc/id-translation/")
"""Root location for cached data and persistent instances.

Default location is ``~/.big_corporation_inc/id-translation/``.

Combining ``Translator`` and ``Fetcher`` caching has its use cases, but
should be done with care as calls to :meth:`id_translation.Translator.go_offline`
does NOT invalidate the individual ``Fetcher`` caches.
"""

TRANSLATOR_CACHE_DIR = BASE_CACHE_DIR / "translator"
"""Location where the persistent ``Translator`` instance is stored.

.. seealso:

   :func:`big_corporation_inc.id_translation.load_cached_translator`.
"""
FETCHER_CACHE_DIR = BASE_CACHE_DIR / "fetcher-data"
"""Location where cached ``Fetcher`` data is stored.

To clear the cache, use :meth:`id_translation.fetching.CacheAccess.clear_all_cache_data`.
"""
_fetching.CacheAccess.BASE_CACHE_PATH = FETCHER_CACHE_DIR
