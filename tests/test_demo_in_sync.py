"""Verify the committed demo matches what the template generates.

* The demo is the template's rendered output (``dev/generate-project.sh``); drift in either direction fails CI.
* Only tracked demo files are compared; git-ignored artifacts are never committed.
* Every prompt value is pinned in the replay file, so files compare byte-for-byte.
"""

import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
DEMO = REPO / "demo" / "bci-id-translation"
REPLAY = REPO / "demo" / "replay.json"
DEMO_PREFIX = "demo/bci-id-translation/"

# Build artifacts cookiecutter may copy from the template working dir (it is not
# git-aware) but that are git-ignored and never part of a generated project.
_ARTIFACT_DIRS = {".ruff_cache", "__pycache__", ".pytest_cache", ".mypy_cache", ".venv"}
# Anchored to the project root, where these are actually produced: an exemption that
# matches any depth would also hide a real template file that happened to be named this.
_ARTIFACT_ROOT_NAMES = {"poetry.lock", "uv.lock", "pytest.log"}
_ARTIFACT_PATHS = {"docs/_build"}


def _is_artifact(rel: str) -> bool:
    path = Path(rel)
    parts = path.parts
    return (
        bool(set(parts) & _ARTIFACT_DIRS)
        or rel.endswith(".pyc")
        or (len(parts) == 1 and path.name in _ARTIFACT_ROOT_NAMES)
        or any(rel.startswith(f"{prefix}/") for prefix in _ARTIFACT_PATHS)
    )


def _tracked_demo_files() -> list[str]:
    # -z: a path with a space in it must not silently split into two, which would drop it
    # from the comparison on one side and add a phantom on the other.
    result = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z", DEMO_PREFIX],
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted(path[len(DEMO_PREFIX) :] for path in result.stdout.split("\0") if path)


@pytest.fixture(scope="module")
def baked(tmp_path_factory) -> Path:
    output_dir = tmp_path_factory.mktemp("baked")
    subprocess.run(
        ["cookiecutter", str(REPO), "--replay-file", str(REPLAY), "--output-dir", str(output_dir), "-f"],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    return output_dir / "bci-id-translation"


def test_generated_file_set_matches_demo(baked):
    generated = {
        rel for path in baked.rglob("*") if path.is_file() and not _is_artifact(rel := str(path.relative_to(baked)))
    }
    assert generated == set(_tracked_demo_files())


@pytest.mark.parametrize("rel", _tracked_demo_files())
def test_demo_file_matches_generated(baked, rel):
    generated = baked / rel
    assert generated.exists(), f"{rel} is committed in the demo but not produced by the template"

    assert (DEMO / rel).read_bytes() == generated.read_bytes(), (
        f"{rel} differs between the committed demo and freshly generated output; "
        "regenerate the demo (dev/generate-project.sh) or back-port template edits (dev/backport.py)."
    )

    # Content alone misses a dropped executable bit: the demo keeps the mode git recorded,
    # so setup-and-verify.sh would still run here while every generated project got a file
    # that cannot be invoked as './setup-and-verify.sh'.
    demo_executable = bool((DEMO / rel).stat().st_mode & 0o111)
    generated_executable = bool(generated.stat().st_mode & 0o111)
    assert demo_executable == generated_executable, (
        f"{rel} is {'executable' if demo_executable else 'not executable'} in the demo but "
        f"{'executable' if generated_executable else 'not executable'} when generated; "
        "fix the mode in {{cookiecutter.project_slug}}/ and regenerate the demo."
    )
