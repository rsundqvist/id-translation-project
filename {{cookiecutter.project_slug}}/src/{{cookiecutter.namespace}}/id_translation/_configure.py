import logging

from id_translation import settings


def configure_lib() -> None:
    """Configure the library. This is done as soon as ``{{cookiecutter.namespace}}`` is imported."""
    settings.logging.TRANSLATE_ONLINE = settings.KeyEventLogLevel(exit=logging.INFO)


def configure_wrapper() -> None:
    """Configure the wrapper. This is done as soon as ``{{cookiecutter.namespace}}`` is imported."""
