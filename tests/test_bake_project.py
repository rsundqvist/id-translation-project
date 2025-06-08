import os
import subprocess
from tempfile import TemporaryDirectory

import pytest
from pathlib import Path

GENERATED_PROJECT_SLUG = "bci-id-translation"
REPLAY_FILE = os.getenv("REPLAY_FILE", "stable")


@pytest.fixture(scope="session")
def tmpdir():
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture(scope="session")
def project_workdir(tmpdir):
    path = tmpdir.joinpath(GENERATED_PROJECT_SLUG)
    os.chdir(path)
    yield path


def test_create(tmpdir):
    replay_file = Path(__file__).parent.joinpath(f"replay/{REPLAY_FILE}").with_suffix(".json")

    result = subprocess.run(
        [
            "cookiecutter", Path(__file__).parent.parent,
            "--replay-file", replay_file,
            "--output-dir", tmpdir,
        ],
        stderr=subprocess.STDOUT
    )
    assert result.returncode == 0  # Cookiecutter returns 0 on failure :(
    assert tmpdir.joinpath(GENERATED_PROJECT_SLUG, "README.md").exists()


def test_poetry_install(project_workdir):
    result = subprocess.run(["poetry", "install"], stderr=subprocess.STDOUT)
    assert result.returncode == 0


def test_run_tests(project_workdir, monkeypatch):
    monkeypatch.setenv("PYTEST_ADDOPTS", "--color=yes")
    result = subprocess.run(["poetry", "run", "pytest"], stderr=subprocess.STDOUT)
    assert result.returncode == 0
