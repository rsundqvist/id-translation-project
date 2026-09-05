"""Regression cases for the name filters in ``cookiecutter_extensions``.

The prompts in ``cookiecutter.json`` derive ``namespace`` and ``project_slug`` from the
organization name, so a bad derivation reaches every generated project. Values here are
real-world shapes that previously crashed or silently mangled the name.
"""

import keyword
import sys

import pytest
from jinja2 import Environment

import cookiecutter_extensions


@pytest.fixture(scope="module")
def filters() -> dict:
    """The filters as cookiecutter sees them: registered by name into a Jinja environment."""
    environment = Environment(  # noqa: S701
        extensions=[cookiecutter_extensions.to_namespace, cookiecutter_extensions.to_slug_prefix]
    )
    return environment.filters


# organization, namespace, slug prefix
CASES = [
    ("Big Corporation Inc.", "big_corporation_inc", "bci"),
    ("Acme", "acme", "acme"),
    ("A B C 9", "a_b_c_9", "abc9"),
    # Digits are not identifiers on their own, so per-character filtering dropped them.
    ("3M Company", "threem_company", "tc"),
    ("1st National Bank", "onest_national_bank", "onb"),
    # Punctuation used to collapse to consecutive underscores and raise IndexError.
    ("Foo & Bar, LLC", "foo_bar_llc", "fbl"),
    # Non-ASCII produced a package name PyPI will not accept.
    ("Ölands Bank AB", "olands_bank_ab", "oba"),
    # A keyword is a valid identifier, but not an importable module name.
    ("Class", "class_", "class_"),
    # A stdlib name installs fine and then never imports: the stdlib wins on sys.path.
    ("Signal", "signal_", "signal_"),
    ("Email", "email_", "email_"),
]


@pytest.mark.parametrize(("organization", "namespace", "slug_prefix"), CASES)
def test_derived_names(filters, organization: str, namespace: str, slug_prefix: str) -> None:
    assert filters["to_namespace"](organization) == namespace
    assert filters["to_slug_prefix"](namespace) == slug_prefix


@pytest.mark.parametrize("organization", [case[0] for case in CASES])
def test_namespace_is_importable(filters, organization: str) -> None:
    namespace = filters["to_namespace"](organization)
    assert namespace.isidentifier()
    assert not keyword.iskeyword(namespace)
    assert namespace.isascii()
    assert namespace not in sys.stdlib_module_names


@pytest.mark.parametrize("organization", ["", "   ", "!!!", "---"])
def test_namespace_rejects_unusable_input(filters, organization: str) -> None:
    with pytest.raises(ValueError, match="Cannot derive a namespace"):
        filters["to_namespace"](organization)
