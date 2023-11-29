# Getting started
For an introduction to translation, see:

* https://id-translation.readthedocs.io/en/stable/documentation/translation-primer.html

Generated documentation example:

* https://rsundqvist.github.io/id-translation-project/

# 🔧 Quickstart 🚀
1. Start the test database
   ```bash
   docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
   ```
2. Then, from a new window, run:
   ```bash
   ./setup-and-verify.sh
   ```

The `setup-and-generate.sh` script will:
1. Lint the generated project (`flake8`, `black`, `isort`).
2. Run the included unit tests against the test database (`pytest`).
3. Run static type checking (`mypy`).
4. Generate documentation for the new project (`sphinx`).

To configure the project for your own needs, keep reading!

# Configuration
Basic [configuration](src/big_corporation_inc/id_translation/config) and 
[factory methods](src/big_corporation_inc/id_translation/_initialize.py) are included, as well as some simple
tests. Copying and adjusting the included [tests](tests/id_translation/test_basics.py) is an easy way to ensure that
basic connectivity and functionality is working as intended while modifying the included configuration to match your domain.

You'll find links to API documentation and crash courses [near the end](#need-help) of this document.

## Structure
The generated project structure, and some possible TODOs.
```bash
bci-id-translation/
├── demo-notebook.ipynb  # <------------------- basic usage examples (Jupyter) -
├── docs/
│     ├── api.rst
│     ├── conf.py
│     ├── example.py
│     ├── index.rst
│     ├── transactions.csv
│     └── translated-transactions.csv
├── GETTING_STARTED.md
├── pyproject.toml
├── README.md
├── setup-and-verify.sh  # <------------------------------- convenience script -
├── src
│   └── big_corporation_inc/  # <---------------------------- namespace -
│         └── id_translation/
│             ├── config/
│             │     ├── fetching/  # <------------------------ fetching config -
│             │     │     ├── dvd-rental-store.toml
│             │     │     ├── geography.toml
│             │     │     └── inactive/ 
│             │     │         ├── csv-files-in-s3.toml
│             │     │         ├── override-only.toml
│             │     │         └── README.txt
│             │     ├── main.toml  # <---------------- main translation config -
│             │     └── metaconf.toml
│             ├── config.py
│             ├── customization.py  # <------ optional specialization examples -
│             ├── _initialize.py
│             ├── __init__.py
│             ├── py.typed
│             └── singleton
│                 ├── __init__.py
│                 ├── _singleton.py
│                 ├── _wrappers.py
│                 └── _wrap.py
└── tests/
    ├── conftest.py   # <----- causes tests to fail if database is unreachable -
    ├── id_translation/
    │     ├── __init__.py
    │     ├── test_basics.py
    │     └── test_demo_some_things.py
    └── __init__.py
```
All commands should be executed from the `bci-id-translation` directory.

## Executing the included tests
The included tests run against the [Sakila DVD rental sample database](https://hub.docker.com/r/rsundqvist/sakila-preload).
To start this database temporarily, run
```bash
docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
```
from a **new terminal window**, then run:

```bash
pytest tests/
```
to execute the included tests. If the tests pass, the project has been correctly installed and the Docker database is
up and running. Read through the rest of this document for more information on how to adapt the template project to suit 
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
    - https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.Translator.html
    - https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.Translator.translate.html


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
