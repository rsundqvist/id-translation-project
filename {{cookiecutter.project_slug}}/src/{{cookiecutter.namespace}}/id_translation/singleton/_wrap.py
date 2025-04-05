# flake8: noqa E231
import functools as functools
import typing as t

FuncT = t.TypeVar("FuncT", bound=t.Callable[..., t.Any])


def wrap(func: FuncT):  # https://github.com/python/mypy/issues/17166
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

    if "\n" in doc:
        index = doc.index("\n")
        header = doc[:index] + "\n" + header
        obj.__doc__ = header + "\n\n" + textwrap.dedent(doc[index:])
    else:
        obj.__doc__ = doc + "\n" + header
