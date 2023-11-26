import functools as functools
import typing as t

if t.TYPE_CHECKING:
    from _typeshed import IdentityFunction

FuncT = t.TypeVar("FuncT", bound=t.Callable[..., t.Any])


def wrap(func: FuncT) -> "IdentityFunction":
    _update_translator_member_fn_docstring(func)
    return functools.wraps(func)


def _update_translator_member_fn_docstring(obj: t.Any) -> None:
    import textwrap

    if isinstance(obj, functools.partial):
        obj = obj.func

    meth = f":meth:`id_translation.Translator.{obj.__name__}`"
    header = f"""
    .. note::

       Convenience method. Calls {meth} using the the current :func:`get_singleton`
       instance. See below for original docstring.
    """
    header = textwrap.dedent(header)

    doc = obj.__doc__
    if doc is None:
        raise ValueError(f"Function {obj} has no docstring.")
    try:
        index = doc.index("\n")
        header = doc[:index] + "\n" + header
        doc = doc[index:]
    except ValueError:
        pass
    obj.__doc__ = header + "\n\n" + textwrap.dedent(doc)
