from . import config


def create_translator() -> config.TRANSLATOR_TYPE:
    """Create a new preconfigured :class:`~id_translation.Translator` instance."""
    translator = config.TRANSLATOR_TYPE.from_config(
        path=config.MAIN_CONFIGURATION_PATH,
        extra_fetchers=config.FETCHING_CONFIGURATION_PATHS,
    )

    # Transformers that the TOML format cannot express -- e.g. one per source matching a naming convention --
    # belong here, after initialize_sources() has resolved the source names:
    #
    #     translator.initialize_sources()
    #     for source in translator.sources:
    #         if source.endswith("_bitmask"):
    #             translator.register_transformer(source, BitmaskTransformer())
    #
    # https://id-translation.readthedocs.io/en/stable/documentation/translator-config.html#programmatic-transformer-registration
    #
    # Registrations made here do NOT reach load_cached_translator(); see its docstring.

    return translator


def load_cached_translator(max_age: str = "12h") -> config.TRANSLATOR_TYPE:
    """Load or (re)create a cached :class:`~id_translation.Translator` instance.

    .. note::

       Transformers registered in code do **not** apply to this instance.
       :meth:`~id_translation.Translator.load_persistent_instance` rebuilds from the TOML
       configuration alone, bypassing :func:`create_translator`, so a transformer added there
       is silently absent here -- affected sources come back untransformed, without an error.
       Transformers declared in ``[transform]`` sections travel with the configuration and are
       unaffected.

    Args:
        max_age: Maximum age of the cached instance before it is recreated.
    """
    # TODO: give the two factory functions a shared post-construction hook so that
    #  programmatic transformer registration applies to the cached instance too.
    return config.TRANSLATOR_TYPE.load_persistent_instance(
        config_path=config.MAIN_CONFIGURATION_PATH,
        extra_fetchers=config.FETCHING_CONFIGURATION_PATHS,
        cache_dir=config.TRANSLATOR_CACHE_DIR,
        max_age=max_age,
    )
