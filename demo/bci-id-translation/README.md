# ID Translation
**Translation of IDs found in *Big Corporation Inc.* databases.**

The ``bci-id-translation`` package provides pre-configured ID translation, powered by the
**ID Translation** [![PyPI - Version](https://img.shields.io/pypi/v/id-translation.svg)](https://pypi.python.org/pypi/id-translation)
library. This project was generated from the [id-translation-project](https://github.com/rsundqvist/id-translation-project)
cookiecutter template on Friday, 30 Jun 2023.

For an introduction to translation, please see the **Translation primer** and **Interpreting `id-translation` Logs**
pages: 
* https://id-translation.readthedocs.io/en/stable/documentation/translation-primer.html
* https://id-translation.readthedocs.io/en/stable/documentation/translation-logging.html

## The ``Translator.translate()``-function
This is the main entry point for all ID translation tasks. Click
[here to see the documentation](https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.html#id_translation.Translator.translate)
for this function.

# Basic usage
Install either for development (with Poetry) or for regular use (with pip).
```bash
poetry install  # Install for development and tests
pip install bci-id-translation  # Install as a regular package
```
The fastest way to translate something is the `big_corporation_inc.id_translation.translate()`-function:
```python
from big_corporation_inc.id_translation import translate
translate(df, inplace=True)
```
This will translate columns in _df_ that end with _'\_id'_, gathering and fetching requested IDs from the database. You
can get a preloaded `Translator` with the `load_cached_translator()`-function:
```python
from big_corporation_inc.id_translation import load_cached_translator
translator = load_cached_translator(max_age="0d")  # max_age="0d" forces recreation of the local cache.
translator.translate(df, inplace=True)
```
The final option is to create a fresh translator instance:
```python
from big_corporation_inc.id_translation import create_translator
translator = create_translator()
```
Translators created this way will be online (connected to a fetcher) with no data stored locally. Having a "clean"
instance allows customization of the translator through the `Translator.copy(**options)`-method.

You can override any pre-configured option this way. Use with care, this may break the Translator in confusing ways 🙂.

# 🔧 Configuring a new project
Basic [configuration](src/big_corporation_inc/id_translation/config) and 
[factory methods](src/big_corporation_inc/id_translation/_initialize.py) are included, as well as some simple
tests. Copying and adjusting the included [tests](tests/test_basics.py) is an easy way to ensure that basic connectivity
and functionality is working as intended while modifying the included configuration to match your domain.

You'll find links to API documentation and crash courses [near the end](#need-help) of this README.

> Consider removing all the 🔧-sections when configuration is complete.

## 🔧 Generated project structure
The generated project structure, and some possible TODOs.
```bash
bci-id-translation/
├── pyproject.toml
├── pytest.ini
├── README.md
├── src/
│   └── big_corporation_inc/
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
All commands should be executed from the `bci-id-translation` directory.

## 🔧 Executing the included tests
The included tests run against the [Sakila DVD rental sample database](https://hub.docker.com/r/rsundqvist/sakila-preload).
To start this database temporarily, run
```bash
docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
```
from a **new terminal window**, then run:

```bash
poetry run pytest tests/test_basics.py
```
to execute the included tests. If the tests pass, the project has been correctly installed and the Docker database is
up and running.  Read through the rest of this README for more information on how to adapt the template project to suit 
the needs of your organization.

## 🔧 Forcing manual configuration
The scoring logic can be disabled, relying only on filters and overrides to perform the mapping. This ensures that IDs
are always translated exactly as intended, but obviously requires more manual work. To do this, define

```toml
[translator.mapping]
score_function = "disabled"

[translator.mapping.overrides]
name0 = "table0"
name1 = "table0"  # Same table as before
name2 = "table2"
```

in [main.toml](src/big_corporation_inc/id_translation/config/main.toml) to force manual Name-to-table mapping,
and

```toml
[fetching.mapping]
score_function = "disabled"

[translator.mapping.overrides.table0]
id = "table0_id"
name = "nejm"  # Maybe we could fix this in the database instead?
```

to disable Placeholder-to-column mapping your
[fetching configuration files](src/big_corporation_inc/id_translation/config/fetching). Overrides are not needed
for columns that are an exact match, i.e. you don't have to specify `id = "id"` anywhere. More details may be found in
the [Override-only mapping (link to `id-translation`)](https://id-translation.readthedocs.io/en/stable/documentation/mapping-primer.html#override-only-mapping)
documentation, or check out [inactive/override-only.toml](src/big_corporation_inc/config/fetching/inactive/override-only.toml) 
for a limited but working example.

## 🔧 Non-SQL translation sources
It's possible to simply enumerate translations manually using
a [MemoryFetcher](https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.fetching.html#id_translation.fetching.MemoryFetcher),
or read them from a file. Pretty much any format and location type that can be read by Pandas is supported, including 
for example S3 (additional dependencies required). See the [PandasFetcher](https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.fetching.html#id_translation.fetching.PandasFetcher)
documentation for details.

An example using CSV files stored in S3 can be found in
[inactive/csv-files-in-s3.toml](src/big_corporation_inc/id_translation/config/fetching/inactive/csv-files-in-s3.toml)
in this project.

## 🔧 Advanced mapping
If the included functions are not enough, you can define your own and tell the `Mapper` to use it by specifying a
fully qualified path as the `function`-argument, e.g.

  ```toml
  [[*.mapping.score_function_heuristics]]
  function = "big_corporation_inc.id_translation.customization.your_function"
  do_a_good_job = true
  ```

will use `your_function` defined in [customization.py](src/ute/id_translation/customization.py), and will pass
`do_a_good_job=True` whenever it is called. These functions must have the correct signature, see

- https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.mapping.types.html#id_translation.mapping.types.AliasFunction
- https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.mapping.types.html#id_translation.mapping.types.FilterFunction

for details. The `(value, candidates, context)`-arguments are given by the `Mapper` and should not be specified in
configuration. Custom Score and Filter functions may be defined in the same way.

# Need help?
This section contains links to **ID Translation** project documentation. If nothing else works, you can  always ask a
question or report an issue on Github:

* https://github.com/rsundqvist/id-translation-project/issues/new

## Home page
* https://id-translation.readthedocs.io

## Overview/crash course pages:
* https://id-translation.readthedocs.io/en/stable/documentation/translation-primer.html
* https://id-translation.readthedocs.io/en/stable/documentation/mapping-primer.html

## TOML configuration files
Documentation of the config format. Click [here](src/big_corporation_inc/id_translation/config/) to go to yours.

* https://id-translation.readthedocs.io/en/stable/documentation/translator-config.html

## Logging
For help interpreting the logs emitted during ID translation, see the **Interpreting `id-translation` Logs**-page.

* https://id-translation.readthedocs.io/en/stable/documentation/translation-logging.html

## API documentation
* The `Translator` class and the `Translate.translate()`-method, which is the main entry point for ID translation tasks.
    - https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.html#id_translation.Translator
    - https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.html#id_translation.Translator.translate


* The `Mapper` class is responsible for turning "the names you want" into "the names you have". You'll rarely need to
  do this yourself; the `Translator` and `AbstractFetcher` classes will call `Mapper.apply()` for you when they need it.
  Configuration for this class is found in the `[*.fetching]`-subsections.

    - https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.mapping.html#id_translation.mapping.Mapper
    - https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.mapping.html#id_translation.mapping.Mapper.apply


* There are a number of functions heuristics, filtering, and short-circuiting (a repurposed filter-function) that are
  included with the library.

    - https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.mapping.filter_functions.html
    - https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.mapping.heuristic_functions.html

  These are configured in `[[*.mapping.filter_functions]]` and `[[*.mapping.score_function_heuristics]]`
  list-subsections.
