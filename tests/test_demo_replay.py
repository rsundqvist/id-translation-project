"""Release gate for ``demo/replay.json``.

* ``id_translation_version`` may pin a local checkout (``@ file:///...``) during development.
* This test fails until it is re-pinned to a released version (see ``tests/replay/*.json``).
* The demo is what adopters read, so its pin must also match the template's own default.
"""

import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
DEMO_REPLAY = REPO / "demo" / "replay.json"
COOKIECUTTER = REPO / "cookiecutter.json"
DEFAULT_REPLAY = REPO / "tests" / "replay" / "default.json"

# A local checkout reaches a dependency spec in more shapes than 'file:'. Anything naming a
# path -- absolute, relative, '~'-rooted, editable, or a file-backed git URL -- is a pin
# that only resolves on the machine it was written on.
_LOCAL_PIN = re.compile(
    r"""
      file:                     # '@ file:///...', 'git+file://...' (any case)
    | (?<![\w.])\.{1,2}/        # '@ ../id-translation', './checkout'
    | @\s*~                     # '@ ~/git/id-translation'
    | @\s*/                     # '@ /home/dev/git/id-translation'
    | (?:^|\s)-e(?=\s)          # '-e ../id-translation'
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _version(path: Path) -> str:
    # cookiecutter.json *is* the context; a replay file wraps it under 'cookiecutter'.
    context = json.loads(path.read_text())
    return context.get("cookiecutter", context)["id_translation_version"]


def test_demo_replay_does_not_pin_a_local_path():
    version = _version(DEMO_REPLAY)

    assert isinstance(version, str)
    assert not _LOCAL_PIN.search(version), (
        f"demo/replay.json pins id_translation_version to a local path ({version!r}). "
        "Re-pin it to a released version (e.g. a '(>=X,<Y)' range or a git URL) before release."
    )


@pytest.mark.parametrize("path", [DEMO_REPLAY, DEFAULT_REPLAY], ids=lambda path: path.name)
def test_replay_matches_the_template_default(path: Path):
    """A bump to cookiecutter.json that misses the replays ships a demo with a stale floor."""
    expected = _version(COOKIECUTTER)

    assert _version(path) == expected, (
        f"{path.relative_to(REPO).as_posix()} pins id_translation_version to "
        f"{_version(path)!r}, but cookiecutter.json defaults to {expected!r}. "
        "Bump both, or the published demo advertises a version range no new project gets. "
        "Regenerating against unreleased code (REPLAY_FILE=tests/replay/master.json) is "
        "expected to leave this red; re-generate with tests/replay/default.json to commit."
    )
