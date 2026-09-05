import pytest

CONNECTION_STRING = "postgresql+pg8000://postgres:Sofia123!@localhost:5002/sakila"

HINT = """The Docker image used is documented at https://hub.docker.com/r/rsundqvist/sakila-preload
To start an ephemeral container for this test, run:
    docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres"""


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(session: pytest.Session, config: pytest.Config, items: list[pytest.Item]) -> None:
    """Stop the session with a readable message when the test database is unreachable.

    Checked after collection rather than in ``pytest_sessionstart`` so that tests marked
    ``no_database`` can run without Docker; ``pytest_sessionstart`` runs too early to know
    what was collected.

    ``trylast`` matters: pytest applies ``-k``/``-m`` deselection in this same hook, and a
    conftest implementation runs *before* the built-in one by default. Without it,
    ``pytest -m no_database`` would still see the database-backed items and demand Docker.
    """
    if all(item.get_closest_marker("no_database") for item in items):
        return
    _require_database()


def _require_database() -> None:
    """Exit the session unless the Sakila test database can be reached.

    Uses :func:`pytest.exit` rather than raising: an exception here is reported as an
    ``INTERNALERROR>`` with a pluggy traceback, which reads as "pytest broke" instead of
    "the database is not running", and prefixes every line of the hint below.
    """
    import sqlalchemy

    try:
        import pg8000  # type: ignore  # noqa: F401
    except ImportError as e:
        pytest.exit(f"Driver not installed: {e}.\n\n{HINT}", returncode=1)

    try:
        engine = sqlalchemy.create_engine(CONNECTION_STRING)
    except Exception as e:
        pytest.exit(f"Could not create an engine for {CONNECTION_STRING!r}: {type(e).__name__}: {e}.", returncode=1)

    try:
        with engine.connect():
            pass
    except Exception as e:
        pytest.exit(f"Could not connect to the test database: {type(e).__name__}: {e}.\n\n{HINT}", returncode=1)
    finally:
        engine.dispose()
