"""Checks that the template stays free of values belonging to a generated project.

Three failure modes, the first two seen in practice:

1. A concrete value is committed where a Jinja placeholder belongs. The values to look for
   are derived from the replay files rather than hardcoded, so adding a prompt to
   ``cookiecutter.json`` extends the check for free. Paths are checked as well as file
   contents: a directory called ``big_corporation_inc`` renders identically in the demo,
   so no other gate sees it.
2. A relative link points at a path no generated project has -- a stale namespace, or a
   missing path segment. No value grep can find these, so links are resolved against the
   rendered demo instead. Only *tracked* demo files count: resolving against the working
   tree would let a link to ``docs/_build/index.html`` pass on any machine where the demo
   has been built.
3. An external link is dead, or points at an anchor that no longer exists. Most of the
   guidance in a generated project is a link into the id-translation documentation, and a
   section that gets renamed upstream leaves a link that still returns 200 but lands the
   reader at the top of the wrong page. Opt-in (``--urls``): it needs the network, and a
   third-party outage must not be able to fail CI.

Run directly, or via ``dev/lint.sh`` / ``uv run inv template-lint``; add ``--urls`` (or
``uv run inv check-links``) for the network check.
"""

import concurrent.futures
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "{{cookiecutter.project_slug}}"
DEMO = ROOT / "demo" / "bci-id-translation"
DEMO_PREFIX = "demo/bci-id-translation/"

REPLAY_FILES = [
    *(ROOT / "tests" / "replay").glob("*.json"),
    ROOT / "demo" / "replay.json",
    ROOT / "dev" / "manual.json",
]

# Values that are legitimately concrete, and how many times each may appear. Counted
# rather than simply permitted, so a genuine leak into the same file is still caught:
# docs/index.rst links the demo directory on GitHub, which is always named for the demo.
ALLOWED = {
    "docs/index.rst": {"bci-id-translation": 1},
}

# Prompts whose values are not substituted into generated files as literals.
SKIP_KEYS = {"id_translation_version"}

_PLACEHOLDER = re.compile(r"{{\s*(cookiecutter\.\w+)\s*}}")
# A ']' straight after '^' is a literal member of the set, so it needs no escape.
_MARKDOWN_LINK = re.compile(r"\[[^]]*]\(([^)\s]+)\)")
# Reference-style definitions ('[label]: target'). GETTING_STARTED.md is written this way,
# so a relative link there would otherwise never be resolved at all.
_MARKDOWN_REFERENCE = re.compile(r"^ {0,3}\[[^]]+]:\s*<?([^>\s]+)>?\s*(?:\"[^\"]*\")?$")
_TRAILING_PUNCTUATION = " .,:;!?'\"()"


def variants(value: str) -> set[str]:
    """Spellings of ``value`` that are still a leak.

    'Big Corporation Inc' (no period) and 'BIG_CORPORATION_INC' are the same mistake as
    the exact value; matching only the literal replay value misses both. The pre-'inv'
    dev/lint.sh grepped for 'Big Corporation Inc' without the period, so dropping these
    would be a regression.
    """
    forms = {value, value.strip(_TRAILING_PUNCTUATION)}
    forms |= {form.replace("-", "_") for form in list(forms)}
    forms |= {form.replace("_", "-") for form in list(forms)}
    return {form.casefold() for form in forms if len(form) > 3}


def leak_candidates() -> dict[str, set[str]]:
    """Concrete values a generated project would carry, taken from the replay files."""
    values: dict[str, set[str]] = {}
    for path in REPLAY_FILES:
        if not path.exists():
            continue
        for key, value in json.loads(path.read_text())["cookiecutter"].items():
            # Short values produce noise; '__'-prefixed keys are cookiecutter internals.
            if key not in SKIP_KEYS and isinstance(value, str) and len(value) > 3:
                values[value] = variants(value)
    return values


def check_leaked_values() -> list[str]:
    """Report concrete values that should have been Jinja placeholders."""
    candidates = leak_candidates()
    problems = []

    for path in sorted(TEMPLATE.rglob("*")):
        if not path.is_file():
            continue

        relative = path.relative_to(TEMPLATE).as_posix()
        budget = dict(ALLOWED.get(relative, {}))

        def hit(value: str) -> bool:
            """True unless this occurrence is covered by the file's ALLOWED budget."""
            if budget.get(value, 0) > 0:
                budget[value] -= 1
                return False
            return True

        # The path itself: cookiecutter renders 'src/big_corporation_inc/' for the demo
        # exactly like 'src/{{cookiecutter.namespace}}/', so the in-sync gate sees nothing.
        folded_relative = relative.casefold()
        for value, forms in candidates.items():
            if any(form in folded_relative for form in forms) and hit(value):
                problems.append(f"{path.relative_to(ROOT)}: leaked {value!r} in the template PATH")

        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue

        seen: set[str] = set()
        for number, line in enumerate(text.splitlines(), 1):
            folded = line.casefold()
            for value, forms in candidates.items():
                if any(form in folded for form in forms) and hit(value):
                    seen.add(value)
                    problems.append(f"{path.relative_to(ROOT)}:{number}: leaked {value!r}\n    {line.strip()[:120]}")

        # A value wrapped across a line break is invisible above; look again with runs of
        # whitespace collapsed. Only multi-word values can wrap.
        unwrapped = " ".join(text.split()).casefold()
        for value, forms in candidates.items():
            if " " not in value or value in seen:
                continue
            if any(form in unwrapped for form in forms) and hit(value):
                problems.append(f"{path.relative_to(ROOT)}: leaked {value!r} (wrapped across lines)")

    return problems


def render(text: str) -> str:
    """Substitute the demo's context, so a template path can be looked up on disk."""
    context = {"cookiecutter.namespace": "big_corporation_inc", "cookiecutter.project_slug": "bci-id-translation"}

    def substitute(match: re.Match[str]) -> str:
        return context.get(match.group(1), match.group(0))

    return _PLACEHOLDER.sub(substitute, text)


def tracked_demo_paths() -> set[str]:
    """Every file and directory a generated project actually ships, demo-relative.

    Tracked files only: ``docs/_build/`` and ``uv.lock`` exist in the working tree after
    ``inv demo-verify``, and resolving links against them makes this check pass or fail
    depending on what the developer happened to run first.
    """
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z", DEMO_PREFIX],
        capture_output=True,
        text=True,
        check=True,
    )
    paths: set[str] = {""}
    for entry in result.stdout.split("\0"):
        if not entry:
            continue
        relative = PurePosixPath(entry[len(DEMO_PREFIX) :])
        paths.add(relative.as_posix())
        paths.update(parent.as_posix() for parent in relative.parents if parent.as_posix() != ".")
    return paths


def resolve(base: str, target: str) -> str | None:
    """Normalize ``target`` against ``base``; None if it leaves the generated project."""
    if target.startswith("/"):
        return None

    parts: list[str] = [part for part in PurePosixPath(base).parts if part not in (".", "")]
    for part in PurePosixPath(target).parts:
        if part in (".", ""):
            continue
        if part == "..":
            if not parts:
                return None  # Escapes the project root.
            parts.pop()
        else:
            parts.append(part)
    return "/".join(parts)


def check_relative_links() -> list[str]:
    """Report relative links that do not resolve in a generated project."""
    if not DEMO.is_dir():
        return [f"{DEMO.relative_to(ROOT)} is missing; regenerate it with 'inv generate-demo'."]

    known = tracked_demo_paths()
    problems = []
    for path in sorted(TEMPLATE.rglob("*.md")):
        # Links are relative to the file that contains them, not to the project root.
        base = render(path.relative_to(TEMPLATE).parent.as_posix())
        for number, line in enumerate(path.read_text().splitlines(), 1):
            targets = [*_MARKDOWN_LINK.findall(line), *_MARKDOWN_REFERENCE.findall(line)]
            for target in targets:
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                resolved = resolve(base, render(target).split("#")[0])
                if resolved is None:
                    problems.append(f"{path.relative_to(ROOT)}:{number}: link escapes the project: {target!r}")
                elif resolved not in known:
                    problems.append(f"{path.relative_to(ROOT)}:{number}: unresolvable link {target!r}")
    return problems


# Trailing punctuation belongs to the prose, not the URL. ')' is deliberately absent from
# the URL character class: a markdown '[x](url)' would otherwise swallow the delimiter.
_URL = re.compile(r"https?://[^\s<>\"'`)\]}]+")
_URL_TRAILING = ".,;:!?*_"
_TIMEOUT = 20
# Default urllib identification is rejected by some documentation hosts.
_USER_AGENT = "id-translation-project-linter (+https://github.com/rsundqvist/id-translation-project)"
# Enough of a Sphinx page to contain any anchor; a whole page is not worth holding.
_MAX_BYTES = 4_000_000
# Hosts that add heading ids client-side, so a fragment cannot be verified from the HTML.
_CLIENT_SIDE_ANCHORS = {"github.com", "www.github.com"}
# Not addresses of documentation: an example endpoint the reader is meant to run locally.
_LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}
# Vendored boilerplate (the standard GitHub Python .gitignore). Its comments link tools
# this project does not use, and their anchors are nobody here's to keep current.
_SKIPPED_FILES = {".gitignore"}


def collect_urls() -> dict[str, list[str]]:
    """External URLs in the template, mapped to the ``file:line`` sites that use them."""
    sites: dict[str, list[str]] = {}
    for path in sorted(TEMPLATE.rglob("*")):
        if not path.is_file() or path.relative_to(TEMPLATE).as_posix() in _SKIPPED_FILES:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue

        for number, line in enumerate(text.splitlines(), 1):
            for raw in _URL.findall(line):
                # A notebook stores prose as JSON, so a URL at end-of-line carries '\n'.
                url = render(raw).removesuffix("\\n").rstrip(_URL_TRAILING)
                if urllib.parse.urlparse(url).hostname in _LOCAL_HOSTS:
                    continue
                sites.setdefault(url, []).append(f"{path.relative_to(ROOT)}:{number}")
    return sites


def verify_url(url: str) -> str | None:
    """Fetch `url`; return a problem description, or None if it is good."""
    target, _, fragment = url.partition("#")
    request = urllib.request.Request(target, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=_TIMEOUT) as response:
            status = response.status
            body = response.read(_MAX_BYTES)
            content_type = response.headers.get_content_type()
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:  # Network, DNS, TLS, timeout -- all equally unusable.
        return f"{type(e).__name__}: {e}"

    if status >= 400:
        return f"HTTP {status}"
    if not fragment or content_type != "text/html":
        return None
    if urllib.parse.urlparse(target).hostname in _CLIENT_SIDE_ANCHORS:
        return None

    # Sphinx renders a section anchor as an id; older pages may use a bare name.
    html = body.decode(errors="replace")
    anchor = urllib.parse.unquote(fragment)
    if any(f'{attribute}="{anchor}"' in html for attribute in ("id", "name")):
        return None
    return f"anchor '#{anchor}' not found on the page"


def check_external_links() -> list[str]:
    """Report template URLs that are unreachable or whose anchor has gone."""
    sites = collect_urls()
    problems = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for url, problem in zip(sites, pool.map(verify_url, sites)):
            if problem is not None:
                problems.append(f"{url}\n    {problem}\n    used by: {', '.join(sites[url])}")
    return problems


def main() -> int:
    checks = [("leaked values", check_leaked_values), ("relative links", check_relative_links)]
    if "--urls" in sys.argv[1:]:
        checks.append(("external links", check_external_links))

    failed = False
    for name, check in checks:
        problems = check()
        if problems:
            failed = True
            print(f"FAIL: {name} ({len(problems)})")
            for problem in problems:
                print(f"  {problem}")
        else:
            print(f"ok: {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
