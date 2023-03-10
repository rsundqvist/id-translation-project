"""Configuration constants."""
from pathlib import Path as _Path

from id_translation import Translator as _Translator

_config_root = _Path(__file__).parent.joinpath("config")

MAIN_CONFIGURATION_PATH = _config_root.joinpath("main.toml")
"""Contains all configuration which is not specific to a single fetcher."""
FETCHING_CONFIGURATION_PATHS = list(_config_root.glob("fetching/*.toml"))
"""Contains configuration for sources, typically databases."""
CACHE_DIR = _Path.home().joinpath(".{{cookiecutter.organization}}/.cache/.id-translation")
"""Location of Translator cache and associated metadata."""

# TRANSLATOR_IMPLEMENTATION = customization.translator.CustomTranslator
TRANSLATOR_IMPLEMENTATION = _Translator
"""The Translator implementation to use. There's usually little reason to change this."""
