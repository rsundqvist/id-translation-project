# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import {{cookiecutter.namespace}}.id_translation

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "{{cookiecutter.project_slug}}"
copyright = "{{cookiecutter.organization}}, {{ cookiecutter.__generation_date.split(' ') | last }}"
author = "{{cookiecutter.full_name}}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

add_module_names = False  # Remove namespaces from class/method signatures

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]
autosummary_ignore_module_all = True
autosummary_imported_members = True

autodoc_typehints = "none"
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "member-order": "bysource",
    "show-inheritance": True,
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "id_translation": ("https://id-translation.readthedocs.io/en/stable/", None),
    "rics": ("https://rics.readthedocs.io/en/stable/", None),
}


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Theme -------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "pydata_sphinx_theme"
html_static_path = []
html_theme_options = {}

# -- Nitpicky configuration ----------------------------------------------------
nitpicky = True
nitpick_ignore = []
nitpick_ignore_regex = []

