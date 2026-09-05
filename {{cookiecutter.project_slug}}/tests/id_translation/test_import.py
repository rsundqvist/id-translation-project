"""Import-time guarantees. Marked ``no_database`` so they run without the test container."""

import os
import subprocess
import sys

import pytest

NAMESPACE = "{{cookiecutter.namespace}}.id_translation"

pytestmark = pytest.mark.no_database

# Subprocesses must not inherit PYTHONOPTIMIZE: it strips assertions, which would make the
# checks below pass whatever happens. The -OO test sets its own optimization explicitly.
_ENV = {**os.environ, "PYTHONOPTIMIZE": ""}


def test_import_under_optimized_python():
    """The package must import with docstrings stripped.

    'python -OO' sets ``__doc__`` to ``None`` everywhere. The singleton wrappers build
    their docstrings from :class:`id_translation.Translator` members at import time, so
    they have to tolerate that -- otherwise deploying with ``PYTHONOPTIMIZE=2`` fails on
    import.
    """
    result = subprocess.run(
        [sys.executable, "-OO", "-c", f"import {NAMESPACE}"],
        capture_output=True,
        text=True,
        env=_ENV,
    )
    assert result.returncode == 0, result.stderr


def test_library_docstrings_are_not_mutated():
    """Importing this package must not rewrite :mod:`id_translation` docstrings.

    The wrappers copy ``Translator`` docstrings; assigning the composed text back onto
    the original member would corrupt it for every other consumer in the process.
    """
    code = f"""
import sys

from id_translation import Translator

before = Translator.translate.__doc__
import {NAMESPACE}  # noqa: F401
if Translator.translate.__doc__ != before:
    sys.exit("id_translation docstring was mutated on import")
"""
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=_ENV)
    assert result.returncode == 0, result.stdout + result.stderr
