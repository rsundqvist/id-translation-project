import keyword
import re
import sys
import unicodedata

from cookiecutter.utils import simple_filter

_DIGIT_WORDS = "zero one two three four five six seven eight nine".split()


@simple_filter
def to_namespace(s: str) -> str:
    """Derive an importable Python package name from an organization name."""
    original = s

    # Strip accents; 'Ölands Bank AB' must not yield a non-ASCII package name.
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    # Collapse runs of unsupported characters instead of dropping them one by one:
    # filtering per character also deletes digits, mangling names like '3M Company'.
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")

    if not s:
        raise ValueError(f"Cannot derive a namespace from organization={original!r}.")

    if s[0].isdigit():
        s = digit_to_word(s[0]) + s[1:]
    if keyword.iskeyword(s) or s in sys.stdlib_module_names:
        # 'class' is an identifier but not an importable name, and a package called
        # 'signal' or 'email' loses to the stdlib on sys.path -- it installs, then
        # never imports.
        s += "_"

    if not s.isidentifier():  # Defensive; the substitutions above should guarantee it.
        raise ValueError(f"Derived namespace={s!r} from organization={original!r} is not an identifier.")

    return s


@simple_filter
def to_slug_prefix(s: str) -> str:
    """Abbreviate a namespace to its initials, e.g. 'big_corporation_inc' -> 'bci'."""
    parts = [part for part in s.split("_") if part]
    return "".join(part[0] for part in parts) if len(parts) > 1 else s


def digit_to_word(s: str) -> str:
    def f(c: str) -> str:
        return _DIGIT_WORDS[int(c)] if c.isdigit() else c

    return "".join(map(f, s))
