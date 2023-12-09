from . import config


def create_translator() -> config.TRANSLATOR_TYPE:
    """Create a new preconfigured :class:`~id_translation.Translator` instance."""
    return config.TRANSLATOR_TYPE.from_config(
        path=config.MAIN_CONFIGURATION_PATH,
        extra_fetchers=config.FETCHING_CONFIGURATION_PATHS,
    )


def load_cached_translator(max_age: str = "12h") -> config.TRANSLATOR_TYPE:
    """Load or (re)create a cached :class:`~id_translation.Translator` instance."""
    return config.TRANSLATOR_TYPE.load_persistent_instance(
        config_path=config.MAIN_CONFIGURATION_PATH,
        extra_fetchers=config.FETCHING_CONFIGURATION_PATHS,
        cache_dir=config.TRANSLATOR_CACHE_DIR,
        max_age=max_age,
    )
