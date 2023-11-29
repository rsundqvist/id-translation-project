import pytest


def pytest_sessionstart(session: pytest.Session) -> None:
    import sqlalchemy

    try:
        import pg8000  # type: ignore  # noqa: F401
    except ImportError as e:
        raise ImportError("Driver not installed.") from e

    try:
        sqlalchemy.create_engine("postgresql+pg8000://postgres:Sofia123!@localhost:5002/sakila").connect()
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"

        raise ValueError(
            f"""Could not connect to the test database: {exc}.

            The Docker image used is documented at https://hub.docker.com/r/rsundqvist/sakila-preload
            To start an ephemeral container for this test, run:
                docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
            """  # noqa
        )
