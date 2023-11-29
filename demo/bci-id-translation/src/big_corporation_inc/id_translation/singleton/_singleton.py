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
    """
    from id_translation.exceptions import ConnectionStatusError

    from .._initialize import create_translator

    global INSTANCE
    if recreate and INSTANCE is not None:
        try:
            INSTANCE.fetcher.close()
        except ConnectionStatusError:
            pass

    if INSTANCE is None:
        INSTANCE = create_translator()
        assert INSTANCE.online, "This should not happen! What did you do?"

    return INSTANCE
