import logging
import typing as t

from .. import config

INSTANCE: t.Optional[config.TRANSLATOR_TYPE] = None


def get_singleton(*, recreate: bool = False) -> config.TRANSLATOR_TYPE:
    """Get the :class:`~id_translation.Translator` singleton instance.

    The exact type returned depends on :attr:`~big_corporation_inc.id_translation.config.TRANSLATOR_TYPE`. By
    default, this is the regular :class:`id_translation.Translator` type provided by :mod:`id_translation`.

    Args:
        recreate: If ``True``, force recreating the current singleton instance.

    Returns:
        A :class:`id_translation.Translator`.

    Notes:
        Creating the instance is not thread safe, and neither is the first
        :meth:`~id_translation.Translator.initialize_sources` call it performs -- that call resolves the sources and
        registers fetcher-provided transformers, mutating the ``Translator``. Since
        :meth:`~id_translation.Translator.translate` triggers it implicitly, the first concurrent ``translate()`` call
        through the singleton is the hazard. Warm the singleton once during startup::

            get_singleton().initialize_sources()

        before handing it to worker threads. See
        https://id-translation.readthedocs.io/en/stable/documentation/translation-concurrency.html#thread-safety.
    """
    from id_translation.exceptions import ConnectionStatusError

    from .._initialize import create_translator

    global INSTANCE
    if recreate and INSTANCE is not None:
        try:
            INSTANCE.fetcher.close()
        except ConnectionStatusError:
            pass

        INSTANCE = None
        logging.getLogger(__package__).info("Singleton reset.")

    if INSTANCE is None:
        INSTANCE = create_translator()
        assert INSTANCE.online, "This should not happen! What did you do?"

    return INSTANCE
