from typing import Optional

from id_translation.types import Names, NameType, NameTypes, Translatable

from ._initialize import create_translator

SINGLETON = None


def translate(
    translatable: Translatable,
    names: NameTypes[NameType] = None,
    ignore_names: Names[NameType] = None,
    inplace: bool = False,
    maximal_untranslated_fraction: float = 0.0,
    attribute: str = None,
) -> Optional[Translatable]:
    """Quick and dirty ID translation. Always calls the database to retrieve fresh values.

    Args:
        translatable: A data structure to translate.
        names: Explicit names to translate. Derive from `translatable` if ``None``.
        ignore_names: Names **not** to translate, or a predicate ``(str) -> bool``.
        inplace: If ``True``, translate in-place and return ``None``.
        maximal_untranslated_fraction: The maximum fraction of IDs for which translation may fail before an error is
            raised. 1=disabled.
        attribute: If given, translate ``translatable.attribute`` instead. If ``inplace=False``, the translated
            attribute will be assigned to `translatable` using
            ``setattr(translatable, attribute, <translated-attribute>)``.

    Returns:
        A copy of translated copy of `translatable` if ``inplace=False``, otherwise ``None``.
    """
    global SINGLETON

    if SINGLETON is None:
        SINGLETON = create_translator()

    assert SINGLETON.online, "This should not happen. What did you do?"

    return SINGLETON.translate(
        translatable,
        names=names,
        ignore_names=ignore_names,
        inplace=inplace,
        override_function=None,  # Should not be needed if configuration is correct.
        maximal_untranslated_fraction=maximal_untranslated_fraction,
        reverse=False,  # Not supported in online mode (the singleton should never go offline).
        attribute=attribute,
    )
