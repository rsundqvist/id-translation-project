from id_translation import Translator

from . import config


def create_translator() -> Translator:
    """Create a preconfigured Translator instance."""
    return Translator.from_config(
        path=config.MAIN_CONFIGURATION_PATH,
        extra_fetchers=config.FETCHING_CONFIGURATION_PATHS,
        clazz=config.TRANSLATOR_IMPLEMENTATION,
    )


def load_cached_translator(max_age: str = "12h") -> Translator:
    """Load or (re)create a cached Translator instance."""
    return Translator.load_persistent_instance(
        config_path=config.MAIN_CONFIGURATION_PATH,
        extra_fetchers=config.FETCHING_CONFIGURATION_PATHS,
        cache_dir=config.CACHE_DIR,
        max_age=max_age,
        clazz=config.TRANSLATOR_IMPLEMENTATION,
    )
