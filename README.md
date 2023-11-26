# ID Translation Cookiecutter Template
A cookiecutter template backed by my [id-translation](https://github.com/rsundqvist/id-translation) package.

-----------------

[![PyPI - Version](https://img.shields.io/pypi/v/id-translation.svg)](https://pypi.python.org/pypi/id-translation)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/id-translation.svg)](https://pypi.python.org/pypi/id-translation)
[![Tests](https://github.com/rsundqvist/id-translation/workflows/tests/badge.svg)](https://github.com/rsundqvist/id-translation/actions?workflow=tests)
[![Codecov](https://codecov.io/gh/rsundqvist/id-translation/branch/master/graph/badge.svg)](https://codecov.io/gh/rsundqvist/id-translation)
[![Read the Docs](https://readthedocs.org/projects/id-translation/badge/)](https://id-translation.readthedocs.io/)


## What is it?
A template for a working starting point for creating specialized [íd-translation](https://pypi.org/project/id-translation/)
packages for an organization. 

# Demo project
Sample output available on GitHub.
* 🖥️ **Code**: [demo/bci-id-translation](demo/bci-id-translation)
* 📚 **Generated documentation**: https://rsundqvist.github.io/id-translation-project/

# Quickstart
Check out the [demo project](demo/bci-id-translation) to see what the end result might be. The documentation for the
demo project is available [here](https://rsundqvist.github.io/id-translation-project/).

## 1. Generate the project
Install the latest version of `cookiecutter`, then generate a new `id-translation` project.
```bash
pip install -U cookiecutter
cookiecutter https://github.com/rsundqvist/id-translation-project.git
```
Cookiecutter will ask you for a few inputs. You can use the defaults for most of them. The most important ones are
listed below.

| The keys               | What they're used for                                                                          |
|------------------------|------------------------------------------------------------------------------------------------|
| organization           | Base name used for generated code, as well as some flavor text, e.g. _Big Corporation Inc._    |
| namespace              | Python namespace for the new package, e.g. `from <namespace>.id_translation import translate`. |
| project_slug           | The name of the new project, e.g. `pip install <namespace>-id-translation`.                    |
| id_translation_version | Version of the [id-translation](https://github.com/rsundqvist/id-translation) package.         |

❗ Subsequent steps will assume that **defaults were used** for all Cookiecutter prompts.

Generated project structure:
```bash
{{cookiecutter.project_slug}}/
├── demo-notebook.ipynb  # <--------------------- basic usage examples (Jupyter)
├── pyproject.toml
├── pytest.ini
├── README.md
├── setup-and-verify.sh  # <----------------------------- run me to get started!
├── src/
│   └── {{cookiecutter.namespace}}/   # <--------------------------- <namespace>
│       └── id_translation/
│           ├── config/
│           │   ├── fetching/  # <------------------------------ fetching config
│           │   │   ├── dvd-rental-store.toml
│           │   │   ├── geography.toml
│           │   │   └── inactive/
│           │   │       ├── csv-files-in-s3.toml  # <-------- fetching from file
│           │   │       ├── override-only.toml  # <- alternative fetching config
│           │   │       └── README.txt
│           │   ├── main.toml  # <---------------------- main translation config
│           │   └── metaconf.toml
│           ├── config.py  # <-------- you might want to change config.CACHE_DIR
│           ├── customization.py  # <---------- optional specialization examples
│           ├── _initialize.py
│           ├── __init__.py
│           ├── py.typed
│           └── _translate.py
└── tests
    ├── conftest.py  # <-------- causes tests to fail if database is unreachable
    ├── __init__.py
    ├── test_basics.py
    └── test_demo_some_things.py
```

## 2. Install the project development environment with Poetry
❗ If you don't have Poetry installed, you can get it here: https://python-poetry.org/docs/#installation

Move into the new project dir, then install and activate the development environment
```bash
cd bci-id-translation/  # <--- <project_slug>
poetry install
poetry shell
```
<pre><span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ poetry install
Creating virtualenv <span style="color: #06989A; ">bci-id-translation</span> in /git/bci-id-translation/.venv
<span style="color: #3465A4; ">Installing dependencies from lock file</span>

<b>Package operations</b>: <span style="color: #3465A4; ">18</span> installs, <span style="color: #3465A4; ">0</span> updates, <span style="color: #3465A4; ">0</span> removals

  ...
  <span style="color: #4E9A06; "><b>•</b></span> Installing <span style="color: #06989A; ">rics</span> (<span style="color: #4E9A06; ">3.0.0</span>)
  <span style="color: #4E9A06; "><b>•</b></span> Installing <span style="color: #06989A; ">sqlalchemy</span> (<span style="color: #4E9A06; ">2.0.4</span>)
  <span style="color: #4E9A06; "><b>•</b></span> Installing <span style="color: #06989A; ">id-translation</span> (<span style="color: #4E9A06; ">0.4.0</span>)
  <span style="color: #4E9A06; "><b>•</b></span> Installing <span style="color: #06989A; ">pg8000</span> (<span style="color: #4E9A06; ">1.29.4</span>)
  <span style="color: #4E9A06; "><b>•</b></span> Installing <span style="color: #06989A; ">pytest</span> (<span style="color: #4E9A06; ">7.2.2</span>)

<b>Installing</b> the current project: <span style="color: #06989A; ">bci-id-translation</span> (<span style="color: #4E9A06; ">0.1.0</span>)
<span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ poetry shell
Spawning shell within <span style="color: #3465A4; ">/git/bci-id-translation/.venv</span>
<span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ . /git/bci-id-translation/.venv/bin/activate
(bci-id-translation-py3.11) <span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ 
</pre>

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
pytest tests/test_basics.py
```
<pre>(bci-id-translation-py3.11) <span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ pytest tests/test_basics.py 
<b>====================================================================== test session starts ======================================================================</b>
platform linux -- Python 3.11.2, pytest-7.2.2, pluggy-1.0.0
rootdir: /git/bci-id-translation, configfile: pytest.ini
<b>collected 6 items                                                                                                                                               </b>

tests/test_basics.py <span style="color: #4E9A06; ">......                                                                                                                               [100%]</span>

<span style="color: #4E9A06; ">======================================================================= </span><span style="color: #4E9A06; "><b>6 passed</b></span><span style="color: #4E9A06; "> in 2.98s =======================================================================</span>
(bci-id-translation-py3.11) <span style="color: #4E9A06; "><b>dev@ubuntu</b></span>:<span style="color: #3465A4; "><b>/git/bci-id-translation</b></span>$ 
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
