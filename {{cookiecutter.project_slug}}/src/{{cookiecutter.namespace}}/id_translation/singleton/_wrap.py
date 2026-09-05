# flake8: noqa E231
import functools as functools
import textwrap as textwrap
import typing as t

FuncT = t.TypeVar("FuncT", bound=t.Callable[..., t.Any])


def wrap(func: t.Any) -> t.Callable[[FuncT], FuncT]:
    """Give the decorated singleton wrapper the name and docstring of `func`.

    Deliberately not :func:`functools.wraps`. That would set ``__wrapped__``, making
    :func:`inspect.signature` report the underlying method's ``self`` parameter, and it
    reports ``__module__`` as :mod:`id_translation` rather than this package.

    The composed docstring is assigned to the *wrapper*. Assigning it to `func` instead
    would mutate a shared :class:`id_translation.Translator` member for every consumer
    in the process.
    """
    doc = _singleton_docstring(func)
    signature = _singleton_signature(func)
    name = _unwrap(func).__name__

    def decorate(wrapper: FuncT) -> FuncT:
        attrs = t.cast(t.Any, wrapper)
        attrs.__name__ = name
        attrs.__qualname__ = name
        attrs.__doc__ = doc
        if signature is not None:
            # Without this the wrappers document as '(*args, **kwargs)'.
            attrs.__signature__ = signature
        return wrapper

    return decorate


def _unwrap(obj: t.Any) -> t.Any:
    """The underlying function of a :class:`functools.partial`, which has no ``__name__``."""
    return obj.func if isinstance(obj, functools.partial) else obj


def _singleton_signature(obj: t.Any) -> t.Any:
    """Signature of `obj` without ``self``, which callers of the wrapper never pass."""
    import inspect

    try:
        signature = inspect.signature(obj)
    except (TypeError, ValueError):  # pragma: no cover - builtins and C functions.
        return None

    parameters = list(signature.parameters.values())
    if parameters and parameters[0].name == "self":
        parameters = parameters[1:]
    return signature.replace(parameters=parameters)


def _singleton_docstring(obj: t.Any) -> str | None:
    """Compose the wrapper docstring, or ``None`` if `obj` has none."""
    obj = _unwrap(obj)

    doc = obj.__doc__
    if doc is None:
        # 'python -OO' strips docstrings. Importing must still work.
        return None

    meth = f":meth:`id_translation.Translator.{obj.__name__}`"
    header = textwrap.dedent(f"""
    .. note::

       Convenience method. Calls {meth} using the current :func:`get_singleton`
       instance. See below for original docstring.
    """)

    if "\n" in doc:
        index = doc.index("\n")
        return doc[:index] + "\n" + header + "\n\n" + textwrap.dedent(doc[index:])
    return doc + "\n" + header
