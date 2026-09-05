# ID Translation Cookiecutter Template
A cookiecutter template backed by my [id-translation](https://github.com/rsundqvist/id-translation) package.

-----------------

[![PyPI - Version](https://img.shields.io/pypi/v/id-translation.svg)](https://pypi.python.org/pypi/id-translation)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/id-translation.svg)](https://pypi.python.org/pypi/id-translation)
[![Tests](https://github.com/rsundqvist/id-translation/workflows/tests/badge.svg)](https://github.com/rsundqvist/id-translation/actions?workflow=tests)
[![Codecov](https://codecov.io/gh/rsundqvist/id-translation/branch/master/graph/badge.svg)](https://codecov.io/gh/rsundqvist/id-translation)
[![Read the Docs](https://readthedocs.org/projects/id-translation/badge/)](https://id-translation.readthedocs.io/)


## What is it?
A template for a working starting point for creating specialized [id-translation](https://pypi.org/project/id-translation/)
packages for an organization. 

# Demo project
Sample output available on GitHub.
* 🖥️ **Code**: [demo/bci-id-translation](demo/bci-id-translation)
* 📚 **Generated documentation**: https://rsundqvist.github.io/id-translation-project/

# Quickstart
Uses [cookiecutter](https://pypi.org/project/cookiecutter/) to generate the project (directly or through `uvx`).

You will need...
* [uv](https://docs.astral.sh/uv/getting-started/installation/) to install the project, and
* [Docker](https://www.docker.com/products/docker-desktop/) to run the included tests.

Everything else will be installed when you run `uv sync`. Steps:
1. Generate project (`uvx`)
   ```bash
   uvx cookiecutter https://github.com/rsundqvist/id-translation-project.git
   ```
2. Start test database (separate window)
   ```bash
   docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
   ```
3. Run the included script
   ```bash
   cd <project_slug>
   ./setup-and-verify.sh
   ```

The `setup-and-verify.sh` script will:
1. Install the project and its dependencies (`uv lock`, `uv sync`).
2. Format the generated project (`ruff format`).
3. Run the included unit tests against the test database (`pytest`).
4. Lint the generated project (`ruff check`).
5. Run static type checking (`mypy`).
6. Generate documentation for the new project (`sphinx`).

## 1. Generate the project

Generate a new `id-translation` project, e.g. using `uvx` (no separate `cookiecutter` install required):
```bash
uvx cookiecutter https://github.com/rsundqvist/id-translation-project.git
```
Cookiecutter will ask you for a few inputs. You can use the defaults for most of them. The most important ones are
listed below.

| The keys               | What they're used for                                                                          |
|------------------------|------------------------------------------------------------------------------------------------|
| organization           | Base name used for generated code, as well as some flavor text, e.g. _Big Corporation Inc._    |
| namespace              | Python namespace for the new package, e.g. `from <namespace>.id_translation import translate`. |
| project_slug           | The name of the new project, e.g. `pip install <project_slug>`. Derived from the namespace.    |
| id_translation_version | A [PEP 508](https://peps.python.org/pep-0508/) version specifier for [id-translation](https://github.com/rsundqvist/id-translation), e.g. `==1.3.0` or `(>=1.3.0,<2.0.0)` -- **not** a bare version number like `1.3.0`, which produces an invalid `pyproject.toml`. |

❗ Subsequent steps will assume that **defaults were used** for all Cookiecutter prompts.

## 2. Install the project development environment with uv
❗ If you don't have uv installed, you can get it here: https://docs.astral.sh/uv/getting-started/installation/

Move into the new project dir, then install and activate the development environment
```bash
cd bci-id-translation/  # <--- <project_slug>
uv sync
source .venv/bin/activate
```
<pre><span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ uv sync
<span style="color: #06989A; ">Using CPython 3.14.6</span>
<span style="color: #06989A; ">Creating virtual environment at:</span> .venv
<span style="color: #06989A; ">Resolved</span> <b>62 packages</b> in 11ms
<span style="color: #06989A; ">Installed</span> <b>56 packages</b> in 138ms
 <span style="color: #4E9A06; "><b>+</b></span> <span style="color: #06989A; ">id-translation</span>==<span style="color: #4E9A06; ">1.3.0</span>
 <span style="color: #4E9A06; "><b>+</b></span> <span style="color: #06989A; ">pandas</span>==<span style="color: #4E9A06; ">3.0.5</span>
 <span style="color: #4E9A06; "><b>+</b></span> <span style="color: #06989A; ">pg8000</span>==<span style="color: #4E9A06; ">1.31.5</span>
 <span style="color: #4E9A06; "><b>+</b></span> <span style="color: #06989A; ">pytest</span>==<span style="color: #4E9A06; ">9.0.3</span>
 <span style="color: #4E9A06; "><b>+</b></span> <span style="color: #06989A; ">rics</span>==<span style="color: #4E9A06; ">6.2.1</span>
 <span style="color: #4E9A06; "><b>+</b></span> <span style="color: #06989A; ">sqlalchemy</span>==<span style="color: #4E9A06; ">2.0.52</span>
 <span style="color: #3465A4; ">...</span>
<span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ source .venv/bin/activate
(bci-id-translation) <span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ </pre>
## 3. Start the test database for the template project
The pre-configured tests are based on the `rsundqvist/sakila-preload:postgres` Docker image. From a **❗ new terminal
window**, run
```
docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
```
to start the database on your machine. The container will be removed as soon as the process terminates. See
https://hub.docker.com/r/rsundqvist/sakila-preload for more information about this image.

To connect to the database yourself using Python Console, run:

```pycon
>>> import sqlalchemy
>>> connection_string = "postgresql+pg8000://postgres:Sofia123!@localhost:5002/sakila"
>>> engine = sqlalchemy.create_engine(connection_string)
>>> print(f"Tables for {engine=}:\n" + "\n".join(sorted(sqlalchemy.inspect(engine).get_table_names())))
Tables for engine=Engine(postgresql+pg8000://postgres:***@localhost:5002/sakila):
actor
address
category
city
country
[more tables...]
```
SQLAlchemy is used internally by the `SqlFetcher` fetching implementation.

## 4. Run the included tests
```bash
pytest tests/id_translation/test_basics.py
```
<pre>(bci-id-translation) <span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ pytest tests/id_translation/test_basics.py 
<b>====================================================================== test session starts ======================================================================</b>
platform linux -- Python 3.14.6, pytest-9.0.3, pluggy-1.6.0
rootdir: /git/bci-id-translation, configfile: pyproject.toml
<b>collected 5 items                                                                                                                                               </b>

tests/id_translation/test_basics.py <span style="color: #4E9A06; ">.....                                                                                                                                [100%]</span>

<span style="color: #4E9A06; ">======================================================================= </span><span style="color: #4E9A06; "><b>5 passed</b></span><span style="color: #4E9A06; "> in 0.95s =======================================================================</span>
(bci-id-translation) <span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ 
</pre>

# Next steps
Check out the `README.md`-file of the generated project for more information, or take a peek at the **ID Translation**
project documentation:
* https://id-translation.readthedocs.io/

For an introduction to translation, please see the **Translation primer** and **Interpreting `id-translation` Logs**
pages:
* https://id-translation.readthedocs.io/en/stable/documentation/translation-primer.html
* https://id-translation.readthedocs.io/en/stable/documentation/translation-logging.html

Happy translating!

# License
[MIT](LICENSE.md)
