# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import big_corporation_inc.id_translation

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "bci-id-translation"
copyright = "Big Corporation Inc., 2025"
author = "Richard Sundqvist"

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


# -- Hacks -------------------------------------------------------------------
def monkeypatch_autosummary_toc() -> None:
    from sphinx.addnodes import toctree
    from sphinx.ext.autosummary import Autosummary, autosummary_toc

    original = Autosummary.run

    def make_toc_tree_titles_shorter(self: Autosummary):
        # tocnode['entries'] = [(".".join(docn.partition("/")[-1].split(".")[-2:]), docn) for docn in docnames]
        toc: toctree
        nodes = original(self)

        for node in nodes:
            if isinstance(node, autosummary_toc):
                for toc in node.children:
                    entries = toc["entries"]

                    for i, (title, ref) in enumerate(entries):
                        if title is None and ref.count(".") > 1:
                            title = ref.split(".")[-1].title()
                            entries[i] = (title, ref)

        return nodes

    Autosummary.run = make_toc_tree_titles_shorter


monkeypatch_autosummary_toc()
