

.. note::

   This is the generated documentation for the
   https://github.com/rsundqvist/id-translation-project/tree/master/demo/bci-id-translation
   demo project.



ID Translation
==============
Translation of IDs found in **Big Corporation Inc.** databases.

.. seealso::

   See docs for the backing API for additional help:  https://id-translation.readthedocs.io/

This documentation was generated from the https://github.com/rsundqvist/id-translation-project template on
`Sunday, 14 Sep 2025`, a cookiecutter template template for the
https://github.com/rsundqvist/id-translation package suite.

Example
-------
Using :func:`~big_corporation_inc.id_translation.singleton.translate` with a temporary translation
:class:`~id_translation.offline.Format`. Input file: :download:`transactions.csv`.

.. literalinclude:: example.py
   :pyobject: demo_translate

.. csv-table:: Output: :download:`translated-transactions.csv`.
   :file: translated-transactions.csv

Modules
-------
Available modules are listed below. See :ref:`key-functions` for an overview of the most important functions of the
package.

.. include:: api.rst
.. _key-functions:

Reexported functions
--------------------
.. automodule:: big_corporation_inc.id_translation
