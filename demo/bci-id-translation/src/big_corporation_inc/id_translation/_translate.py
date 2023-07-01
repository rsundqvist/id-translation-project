from typing import Any, Dict, List, Optional, Union

from id_translation.mapping.types import UserOverrideFunction
from id_translation.offline.types import FormatType
from id_translation.types import (
    IdType,
    Names,
    NameToSource,
    NameType,
    NameTypes,
    SourceType,
    Translatable,
)

from ._initialize import create_translator

SINGLETON = None


def translate(
    translatable: Translatable,
    names: Union[NameTypes[NameType], NameToSource[NameType, SourceType]] = None,
    ignore_names: Names[NameType] = None,
    inplace: bool = False,
    override_function: UserOverrideFunction[NameType, SourceType, IdType] = None,
    maximal_untranslated_fraction: float = 0.0,
    reverse: bool = False,
    attribute: str = None,
    fmt: FormatType = None,
    *,
    copy_kwargs: Dict[str, Any] = None,
) -> Optional[Translatable]:
    """Quick and dirty ID translation. Always calls the database to retrieve fresh values.

    Args:
        translatable: A data structure to translate.
        names: Explicit names to translate. Derive from `translatable` if ``None``. Alternatively, you may pass a
            ``dict`` on the form ``{name_in_translatable: source_to_use}``.
        ignore_names: Names **not** to translate, or a predicate ``(str) -> bool``.
        inplace: If ``True``, translate in-place and return ``None``.
        override_function: A callable ``(name, fetcher.sources, ids) -> Source | None``. Returned values (except
            ``None`` override the mapping procedure defined in ``config/main.toml``.
        maximal_untranslated_fraction: The maximum fraction of IDs for which translation may fail before an error is
            raised. 1=disabled.
        reverse: Not supported by this method. Will crash if ``True``.
        attribute: If given, translate ``translatable.attribute`` instead. If ``inplace=False``, the translated
            attribute will be assigned to `translatable` using
            ``setattr(translatable, attribute, <translated-attribute>)``.
        fmt: Format to use. If ``None``, fall back to init format (specified in the main configuration file).
        copy_kwargs: If given, create a copy of the singleton before translating.

    Returns:
        A copy of translated copy of `translatable` if ``inplace=False``, otherwise ``None``.
    """
    translator = _get_singleton(copy_kwargs)

    return translator.translate(
        translatable,
        names=names,
        ignore_names=ignore_names,
        inplace=inplace,
        override_function=override_function,
        maximal_untranslated_fraction=maximal_untranslated_fraction,
        reverse=reverse,  # Will crash unless False, but we let the lib handle informing the user.
        attribute=attribute,
        fmt=fmt,
    )


def translated_names() -> List[NameType]:
    """Return the names that were translated the most recent :func:`translate`-call."""
    return _get_singleton({}).translated_names()


def _get_singleton(copy_kwargs):
    global SINGLETON
    if SINGLETON is None:
        SINGLETON = create_translator()
    assert SINGLETON.online, "This should not happen! What did you do?"

    return SINGLETON.copy(**copy_kwargs) if copy_kwargs else SINGLETON
