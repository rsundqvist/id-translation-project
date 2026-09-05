# Getting started
For an introduction to translation, see:

* https://id-translation.readthedocs.io/en/stable/documentation/translation-primer.html

Generated documentation example:

* https://rsundqvist.github.io/id-translation-project/

> **Which path are you on?**
> - **Building a new, shared translation package** for your organization -- one that other projects will depend on?
>   You're in the right place; keep reading.
> - **Adding id-translation to an application you already have?** This template is likely more than you need. Follow the
>   [Adopting in an existing project](https://id-translation.readthedocs.io/en/stable/documentation/migration-guide.html)
>   guide instead -- it wires `Translator.from_config()` straight into your existing code.

# 🔧 Quickstart 🚀
1. Start the test database
   ```bash
   docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
   ```
2. Then, from a new window, run:
   ```bash
   ./setup-and-verify.sh
   ```

The `setup-and-verify.sh` script will:
1. Install the project and its dependencies (`uv lock`, `uv sync`).
2. Format the generated project (`ruff format`).
3. Run the included unit tests against the test database (`pytest`).
4. Lint the generated project (`ruff check`).
5. Run static type checking (`mypy`).
6. Generate documentation for the new project (`sphinx`).

The bundled configuration translates the Sakila demo database. **Adapting it to your own data is the main task** -- keep
reading!

# Configuration
**The configuration under [`config/`](src/{{cookiecutter.namespace}}/id_translation/config) is the core of this
package** -- the part you study, adapt, and (in an organization) publish for other projects to reuse. The
[factory methods](src/{{cookiecutter.namespace}}/id_translation/_initialize.py) and wrappers around it rarely change.

Copying and adjusting the included [tests](tests/id_translation/test_basics.py) is an easy way to ensure that basic
connectivity and functionality is working as intended while you modify the included configuration to match your domain.

You'll find links to API documentation and crash courses [near the end](#need-help) of this document.

## Structure
The generated project structure, and some possible TODOs.
```bash
{{cookiecutter.project_slug}}/
├── demo-notebook.ipynb  # <------------------- basic usage examples (Jupyter) -
├── docs/
│     ├── _templates/
│     │     └── autosummary/
│     │         └── module.rst
│     ├── api.rst
│     ├── conf.py
│     ├── example.py
│     ├── index.rst
│     ├── transactions.csv
│     └── translated-transactions.csv
├── .gitignore
├── GETTING_STARTED.md
├── pyproject.toml
├── README.md
├── setup-and-verify.sh  # <------------------------------- convenience script -
├── src
│   └── {{cookiecutter.namespace}}/  # <---------------------------- namespace -
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
    │     ├── test_demo_some_things.py
    │     └── test_import.py
    └── __init__.py
```
All commands should be executed from the `{{cookiecutter.project_slug}}` directory.

## Executing the included tests
The included tests run against the [Sakila DVD rental sample database](https://hub.docker.com/r/rsundqvist/sakila-preload).
To start this database temporarily, run
```bash
docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
```
from a **new terminal window**, then run:

```bash
uv run pytest tests/
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

in [main.toml](src/{{cookiecutter.namespace}}/id_translation/config/main.toml) to force manual Name-to-table mapping,
and

```toml
[fetching.mapping]
score_function = "disabled"

[translator.mapping.overrides.table0]
id = "table0_id"
name = "nejm"  # Maybe we could fix this in the database instead?
```

to disable Placeholder-to-column mapping your
[fetching configuration files](src/{{cookiecutter.namespace}}/id_translation/config/fetching). Overrides are not needed
for columns that are an exact match, i.e. you don't have to specify `id = "id"` anywhere. More details may be found in
the [Override-only mapping (link to `id-translation`)](https://id-translation.readthedocs.io/en/stable/documentation/mapping-primer.html#override-only-mapping)
documentation, or check out [inactive/override-only.toml](src/{{cookiecutter.namespace}}/id_translation/config/fetching/inactive/override-only.toml)
for a limited but working example.

## 🔧 Non-SQL translation sources
It's possible to simply enumerate translations manually using
a [MemoryFetcher](https://id-translation.readthedocs.io/en/stable/api/id_translation.fetching.html#id_translation.fetching.MemoryFetcher),
or read them from a file. Pretty much any format and location type that can be read by Pandas is supported, including 
for example S3 (additional dependencies required). See the [PandasFetcher](https://id-translation.readthedocs.io/en/stable/api/id_translation.fetching.html#id_translation.fetching.PandasFetcher)
documentation for details.

An example using CSV files stored in S3 can be found in
[inactive/csv-files-in-s3.toml](src/{{cookiecutter.namespace}}/id_translation/config/fetching/inactive/csv-files-in-s3.toml)
in this project.

## 🔧 Advanced mapping
If the included functions are not enough, you can define your own and tell the `Mapper` to use it by specifying a
fully qualified path as the `function`-argument, e.g.

  ```toml
  [[*.mapping.score_function_heuristics]]
  function = "{{cookiecutter.namespace}}.id_translation.customization.your_function"
  do_a_good_job = true
  ```

will use `your_function` defined in
[customization.py](src/{{cookiecutter.namespace}}/id_translation/customization.py), and will pass
`do_a_good_job=True` whenever it is called. These functions must have the correct signature, see
- https://id-translation.readthedocs.io/en/stable/api/id_translation.mapping.types.html#id_translation.mapping.types.AliasFunction
- https://id-translation.readthedocs.io/en/stable/api/id_translation.mapping.types.html#id_translation.mapping.types.FilterFunction

for details. The `(value, candidates, context)`-arguments are given by the `Mapper` and should not be specified in
configuration. Custom Score and Filter functions may be defined in the same way.

## 🔧 Extensions
Adjust the template to fit your needs.

### Translating more types
All `Translator` instances can translate the "standard" built-in collections, as well as `numpy` arrays, without any
extra dependencies. Integrations for `pandas`, `polars`, `dask` and `pyarrow` ship with `id-translation` and are loaded
automatically when the library in question is installed.

You may also build your own `DataStructureIO` implementation to create a [user-defined integration] for your package.

Per-call options for the built-in integrations go in `io_kwargs`. For `pandas`, the most useful is categorical output:

```python
translate(df, io_kwargs={"as_category": True, "ordered": "id"})
```

Note that `ordered` and `observed` are ignored unless `as_category=True`, so all three belong together. See
[Categorical translation] for what the ordering choices cost.

[user-defined integration]: https://id-translation.readthedocs.io/en/stable/documentation/translation-io.html#user-defined-integrations
[Categorical translation]: https://id-translation.readthedocs.io/en/stable/api/id_translation.dio.integration.pandas.html#categorical-translation

### Handling `translate` arguments from users
The `TranslationHelper` is a utility class for managing how the `Translator.translate()`-method is called in
applications. For example, you might want to provide sane defaults a function that creates a report, while still 
allowing users to make limited adjustments.

See the [documentation][TranslationHelper] for an example of how the ``TranslationHelper`` can help accomplish this task.

[TranslationHelper]: https://id-translation.readthedocs.io/en/stable/api/id_translation.utils.translation_helper.html

### Applying transformations
The `Transformer` interface is useful for handling composite fields, e.g. bitmasks. The built-in [BitmaskTransformer]
may be configured on a per-source basis to allow the `Translator` to handle data which would otherwise be difficult to
process. The interface is generic and may be extended for arbitrary tasks.

There is a commented-out `[transform.'<source>']` block at the end of
[main.toml](src/{{cookiecutter.namespace}}/id_translation/config/main.toml) to start from. Any number of transformers
may be declared per source -- they run in declaration order, with the fetching files running before `main.toml`. For
transformers that depend on the source names (say, one for every source ending in `_bitmask`), register them in code
in [`create_translator()`](src/{{cookiecutter.namespace}}/id_translation/_initialize.py) instead; see
[Programmatic transformer registration].

[BitmaskTransformer]: https://id-translation.readthedocs.io/en/stable/api/id_translation.transform.html#id_translation.transform.BitmaskTransformer
[Programmatic transformer registration]: https://id-translation.readthedocs.io/en/stable/documentation/translator-config.html#programmatic-transformer-registration

### Caching
Two unrelated things are called "caching" here; pick the one you need.

**Whole-translator caching** is already wired up. The `load_cached_translator()` function keeps a ready-made
`Translator` on disk under `TRANSLATOR_CACHE_DIR` (see
[config.py](src/{{cookiecutter.namespace}}/id_translation/config.py)) and reuses it across processes until it exceeds
`max_age`. If you know which IDs you need in advance, `Translator.go_offline()` fetches them once and disconnects.
Between them these cover most needs, and neither requires you to write any code.

**Per-source fetcher caching** is the escape hatch below those. `id-translation` ships no `CacheAccess`
implementations -- you write one against the [CacheAccess] interface and point a fetching config at it:

```toml
[fetching.cache.'{{cookiecutter.namespace}}.id_translation.customization.MyCacheAccess']
some_argument = "forwarded to __init__"
```

Reach for this only when you need per-source control over what is cached and for how long. See
[Choosing a cache] for the trade-offs, and [Implementing `CacheAccess`] to get started.

[CacheAccess]: https://id-translation.readthedocs.io/en/stable/api/id_translation.fetching.html#id_translation.fetching.CacheAccess
[Choosing a cache]: https://id-translation.readthedocs.io/en/stable/documentation/translator-config.html#choosing-a-cache
[Implementing `CacheAccess`]: https://id-translation.readthedocs.io/en/stable/documentation/translator-config.html#implementing-cacheaccess

# Need help?
This section contains links to **ID Translation** project documentation. If nothing else works, you can always ask a
question or report an issue on GitHub:
* https://github.com/rsundqvist/id-translation-project/issues/new

## Home page
* https://id-translation.readthedocs.io

## Overview/crash course pages:
* https://id-translation.readthedocs.io/en/stable/documentation/translation-primer.html
* https://id-translation.readthedocs.io/en/stable/documentation/mapping-primer.html

## TOML configuration files
Documentation of the config format. Click [here](src/{{cookiecutter.namespace}}/id_translation/config/) to go to yours.
* https://id-translation.readthedocs.io/en/stable/documentation/translator-config.html

## Logging
For help interpreting the logs emitted during ID translation, see the **Interpreting `id-translation` Logs**-page.
* https://id-translation.readthedocs.io/en/stable/documentation/translation-logging.html

## API documentation
* The `Translator` class and the `Translate.translate()`-method, which is the main entry point for ID translation tasks.
    - https://id-translation.readthedocs.io/en/stable/api/id_translation.Translator.html
    - https://id-translation.readthedocs.io/en/stable/api/id_translation.Translator.translate.html

* The `Mapper` class is responsible for turning "the names you want" into "the names you have". You'll rarely need to
  do this yourself; the `Translator` and `AbstractFetcher` classes will call `Mapper.apply()` for you when they need it.
  Configuration for this class is found in the `[*.fetching]`-subsections.
    - https://id-translation.readthedocs.io/en/stable/api/id_translation.mapping.html#id_translation.mapping.Mapper
    - https://id-translation.readthedocs.io/en/stable/api/id_translation.mapping.html#id_translation.mapping.Mapper.apply


* There are a number of functions heuristics, filtering, and short-circuiting (a repurposed filter-function) that are
  included with the library.
    - https://id-translation.readthedocs.io/en/stable/api/id_translation.mapping.filter_functions.html
    - https://id-translation.readthedocs.io/en/stable/api/id_translation.mapping.heuristic_functions.html
  These are configured in `[[*.mapping.filter_functions]]` and `[[*.mapping.score_function_heuristics]]`
  list-subsections.
