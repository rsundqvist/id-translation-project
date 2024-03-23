# ID Translation
**Translation of IDs found in *Big Corporation Inc.* databases.**

The ``bci-id-translation`` package provides pre-configured ID translation, powered by the
**ID Translation** [![PyPI - Version](https://img.shields.io/pypi/v/id-translation.svg)](https://pypi.python.org/pypi/id-translation)
library. This project was generated from the [id-translation-project](https://github.com/rsundqvist/id-translation-project)
cookiecutter template on Saturday, 23 Mar 2024.

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

## The ``Translator.translate()``-function
This is the main entry point for all ID translation tasks. Click
[here to see the documentation](https://id-translation.readthedocs.io/en/stable/_autosummary/id_translation.Translator.translate.html)
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
