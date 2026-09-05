#!/usr/bin/env python
"""Back-port edits from the rendered demo into the cookiecutter template.

The inverse of ``dev/generate-project.sh``; ``demo/replay.json`` maps concrete demo
values back to ``{{cookiecutter.*}}`` variables.

* Edit in the demo (full IDE support), run this, review ``git diff``.
* Files with Jinja logic (``{% now %}``, ``{% if %}``) cannot be reconstructed from
  rendered output; they are skipped and listed - edit those directly in the template.
* Substitution is blind: an occurrence that must stay literal (a URL pointing at the demo
  on GitHub, say) is templatized too, and the result still renders - it just renders
  *wrong*, and no other gate sees it, since the demo round-trips back to the same bytes.
  Lines where a substitution landed inside a URL are reported for review.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

_URL = re.compile(r"https?://\S*{{cookiecutter\.")

REPO = Path(__file__).resolve().parent.parent
DEMO_PREFIX = "demo/bci-id-translation/"
TEMPLATE = REPO / "{{cookiecutter.project_slug}}"
REPLAY = REPO / "demo" / "replay.json"

# Template files containing Jinja logic ({% ... %}); rendered output cannot be
# inverted into these, so they are maintained directly in the template.
JINJA_LOGIC_FILES = {"README.md", "docs/conf.py", "docs/index.rst"}


def substitutions() -> list[tuple[str, str]]:
    """(concrete value -> cookiecutter variable), longest first so specific values win."""
    context = json.loads(REPLAY.read_text())["cookiecutter"]
    # Non-string values ('__is_demo' is a bool) never appear verbatim in rendered output.
    pairs = [(value, "{{cookiecutter.%s}}" % key) for key, value in context.items() if isinstance(value, str) and value]
    return sorted(pairs, key=lambda pair: len(pair[0]), reverse=True)


def templatize(text: str, subs: list[tuple[str, str]]) -> str:
    for value, variable in subs:
        text = text.replace(value, variable)
    return text


def suspicious_lines(rel: str, text: str) -> list[str]:
    """Lines where a substitution landed inside a URL, i.e. probably should not have.

    A URL is an address, not a rendered value: 'github.com/.../demo/bci-id-translation'
    must survive back-porting verbatim. docs/index.rst is the known case and is skipped
    outright; anything else is flagged here rather than silently rewritten.
    """
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        if "{{cookiecutter." in line and _URL.search(line):
            found.append(f"  {rel}:{number}: {line.strip()[:110]}")
    return found


def main() -> int:
    subs = substitutions()
    raw = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z", DEMO_PREFIX],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    tracked = [path for path in raw.split("\0") if path]

    copied: list[str] = []
    skipped: list[str] = []
    suspicious: list[str] = []
    for path in tracked:
        rel = path[len(DEMO_PREFIX) :]
        if rel in JINJA_LOGIC_FILES:
            skipped.append(rel)
            continue

        destination = TEMPLATE / templatize(rel, subs)
        destination.parent.mkdir(parents=True, exist_ok=True)
        source = REPO / path
        try:
            rendered = templatize(source.read_text(), subs)
        except UnicodeDecodeError:
            destination.write_bytes(source.read_bytes())  # binary file: copy verbatim
        else:
            destination.write_text(rendered)
            suspicious.extend(suspicious_lines(rel, rendered))
        copied.append(rel)

    print(f"Back-ported {len(copied)} file(s) into the template.")
    if skipped:
        print("\nSkipped (contain Jinja logic - edit in the template directly):")
        for rel in sorted(skipped):
            print("  - {{cookiecutter.project_slug}}/" + rel)
    if suspicious:
        print("\nCHECK: a substitution landed inside a URL. A URL is an address, not a")
        print("rendered value, so this is probably a literal that must be restored by hand:")
        for line in suspicious:
            print(line)
    print("\nReview `git diff`, then run dev/lint.sh and tests/test_demo_in_sync.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
