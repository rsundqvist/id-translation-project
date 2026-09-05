"""Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke.
"""

import platform
from pathlib import Path

from invoke import call, task
from invoke.context import Context
from invoke.runners import Result

ROOT_DIR = Path(__file__).parent
DEV_DIR = ROOT_DIR.joinpath("dev")
TEST_DIR = ROOT_DIR.joinpath("tests")
DEMO_DIR = ROOT_DIR.joinpath("demo/bci-id-translation")

# The template dir contains Jinja placeholders and isn't valid Python; the demo dir is
# rendered output with its own pyproject.toml/tooling (see demo/.../setup-and-verify.sh).
# Neither belongs to this project's own format/lint targets.
PYTHON_TARGETS = [
    ROOT_DIR.joinpath("cookiecutter_extensions.py"),
    DEV_DIR,
    TEST_DIR,
    Path(__file__),
]
PYTHON_TARGETS_STR = " ".join([str(p) for p in PYTHON_TARGETS])


def _run(c: Context, command: str, env: dict[str, str] | None = None, cwd: Path = ROOT_DIR) -> Result:
    """Run from the repo root, so a task does the same thing from any working directory.

    'clean' deletes by 'find . -name ...' and 'generate-demo' by 'rm -rf demo/...'; both
    would follow the caller's cwd otherwise -- invoke does not chdir to the tasks file.
    """
    print(f"Command: {command} (in {cwd})")
    with c.cd(str(cwd)):
        return c.run(command, pty=platform.system() != "Windows", env=env)


@task
def clean_python(c: Context) -> None:
    """Clean up python file artifacts."""
    _run(c, "find . -name '*.pyc' -exec rm -f {} +")
    _run(c, "find . -name '*.pyo' -exec rm -f {} +")
    _run(c, "find . -name '*~' -exec rm -f {} +")
    _run(c, "find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(c: Context) -> None:
    """Clean up files from testing."""
    _run(c, "rm -fr .pytest_cache")


@task
def clean_ruff(c: Context) -> None:
    """Clean ruff cache (linter)."""
    _run(c, "uv run ruff clean")


@task
def clean_mypy(c: Context) -> None:
    """Clean mypy caches (type checker).

    Recursive: the demo keeps its own cache, and a stale one there makes
    'demo-verify' fail on imports that resolve fine from a clean state.
    """
    _run(c, "find . -name '.mypy_cache' -exec rm -fr {} +")


@task(pre=[clean_python, clean_ruff, clean_tests, clean_mypy])
def clean(_: Context) -> None:
    """Run all clean sub-tasks."""


@task(name="format")
def format_(c: Context, check: bool = False) -> None:
    """Format code."""
    format_options = ["--check", "--diff"] if check else []
    _run(c, f"uv run ruff format {' '.join(format_options)} {PYTHON_TARGETS_STR}")
    if not check:
        _run(c, f"uv run ruff check --fix-only {' '.join(format_options)} {PYTHON_TARGETS_STR}")


@task
def flake8(c: Context) -> None:
    """Lint with ruff.

    Always '--no-fix': 'fix = true' in pyproject.toml makes a plain 'ruff check' rewrite
    the code and exit 0, so a check meant to verify could never fail. Applying fixes is
    'inv format' ('ruff check --fix-only').
    """
    _run(c, f"uv run ruff check --no-fix {PYTHON_TARGETS_STR}")


@task
def check_links(c: Context) -> None:
    """Check that external links in the template still resolve, anchors included.

    Kept out of 'inv lint' and CI on purpose: it needs the network, and a third-party
    documentation outage must not be able to fail an unrelated build.
    """
    _run(c, "dev/lint.sh --urls")


@task
def template_lint(c: Context) -> None:
    """Check that no concrete (un-templatized) values leaked into the template."""
    _run(c, "dev/lint.sh")


@task(pre=[flake8, call(format_, check=True), template_lint])
def lint(_: Context) -> None:
    """Run all linting."""


@task
def tests(c: Context) -> None:
    """Run tests (bakes the template, so does not require the demo's own venv)."""
    _run(c, f"uv run pytest {TEST_DIR}")


@task
def generate_demo(c: Context, replay_file: str | None = None) -> None:
    """Regenerate demo/bci-id-translation/ from the template.

    Without --replay-file this defaults to tests/replay/master.json (unreleased
    id-translation) and OVERWRITES demo/replay.json with that pin, which is not what the
    committed demo should advertise. To regenerate for a commit, pass the demo's own file:

        inv generate-demo --replay-file=demo/replay.json

    tests/test_demo_replay.py fails if that is forgotten.
    """
    env = {"REPLAY_FILE": replay_file} if replay_file else None
    _run(c, "dev/generate-project.sh", env=env)


@task
def backport(c: Context) -> None:
    """Back-port edits made in the demo into the template, then lint the result."""
    _run(c, "dev/backport.sh")


@task
def demo_verify(c: Context) -> None:
    """Run the demo project's own format/test/lint/typecheck/docs pipeline."""
    _run(c, "./setup-and-verify.sh", cwd=DEMO_DIR)
