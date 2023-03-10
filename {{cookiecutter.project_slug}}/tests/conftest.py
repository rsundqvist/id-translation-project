def pytest_sessionstart(session):
    import sqlalchemy

    success = False
    try:
        sqlalchemy.create_engine("postgresql+pg8000://postgres:Sofia123!@localhost:5002/sakila").connect()
        success = True
    except:
        pass

    if not success:
        import sqlalchemy

        raise ValueError("""
        Could not connect to the test database.
        
        The Docker image used is documented at https://hub.docker.com/r/rsundqvist/sakila-preload
        To start an ephemeral container for this test, run:
            docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
        """)