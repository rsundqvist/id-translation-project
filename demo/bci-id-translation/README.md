# ID Translation
**Translation of IDs found in *Big Corporation Inc.* databases.**

The ``bci-id-translation`` package provides pre-configured ID translation, powered by the
**ID Translation** [![PyPI - Version](https://img.shields.io/pypi/v/id-translation.svg)](https://pypi.python.org/pypi/id-translation)
library. This project was generated from the [id-translation-project](https://github.com/rsundqvist/id-translation-project)
cookiecutter template on *Saturday, 11 May 2019*.

> **The most important artifact in this package is its configuration.** The TOML files under
> [`src/big_corporation_inc/id_translation/config/`](src/big_corporation_inc/id_translation/config/) declare
> *what* gets translated and *which sources* the labels come from. Adopting id-translation is mostly a matter of studying
> the bundled example config and adapting it to your own data -- the Python wrappers around it rarely change.

# 🔧 Quickstart 🚀
Start the test database:
```bash
docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres
```
Then, from a new window, run:
```bash
./setup-and-verify.sh
```
See [GETTING_STARTED.md](GETTING_STARTED.md) for further instructions.

# 📂 Make it yours: the configuration
The bundled configuration translates the [Sakila demo database](https://hub.docker.com/r/rsundqvist/sakila-preload).
**Replacing it with your own is the main task** -- and the part of this package you will actually maintain:

* [`config/main.toml`](src/big_corporation_inc/id_translation/config/main.toml) -- the `Translator` itself:
  the output format and how column names map to sources.
* [`config/fetching/`](src/big_corporation_inc/id_translation/config/fetching/) -- one file per data source
  (SQL databases, files, or in-memory data).

Study these against the [configuration format documentation](https://id-translation.readthedocs.io/en/stable/documentation/translator-config.html),
then point them at your own databases and tables. Re-running `./setup-and-verify.sh` is a fast way to confirm your edits
still work.

## The ``Translator.translate()``-function
This is the main entry point for all ID translation tasks. Click
[here to see the documentation](https://id-translation.readthedocs.io/en/stable/api/id_translation.Translator.translate.html)
for this function.

# Basic usage
Install either for development (with uv) or for regular use (with pip).
```bash
uv sync  # Install for development and tests
pip install bci-id-translation  # Install as a regular package
```
The fastest way to translate something is the `big_corporation_inc.id_translation.translate()`-function:
```python
from big_corporation_inc.id_translation import translate
translate(df, copy=False)
```
This will translate columns in _df_ that end with _'\_id'_, gathering and fetching requested IDs from the database. You
can get a preloaded `Translator` with the `load_cached_translator()`-function:
```python
from big_corporation_inc.id_translation import load_cached_translator
translator = load_cached_translator(max_age="0d")  # max_age="0d" forces recreation of the local cache.
translator.translate(df, copy=False)
```
The final option is to create a fresh translator instance:
```python
from big_corporation_inc.id_translation import create_translator
translator = create_translator()
```
Translators created this way will be online (connected to a fetcher) with no data stored locally. Having a "clean"
instance allows customization of the translator through the `Translator.copy(**options)`-method.

You can override any pre-configured option this way. Use with care, this may break the Translator in confusing ways 🙂.

# Need help?
This section contains links to **ID Translation** project documentation. If nothing else works, you can  always ask a
question or report an issue on GitHub:

* https://github.com/rsundqvist/id-translation-project/issues/

## Home page
* https://id-translation.readthedocs.io

## Overview/crash course pages:
* https://id-translation.readthedocs.io/en/stable/documentation/translation-primer.html
* https://id-translation.readthedocs.io/en/stable/documentation/mapping-primer.html
* https://id-translation.readthedocs.io/en/stable/documentation/translation-logging.html

## TOML configuration files
Documentation of the config format. Click [here](src/big_corporation_inc/id_translation/config/) to go to yours.

* https://id-translation.readthedocs.io/en/stable/documentation/translator-config.html
