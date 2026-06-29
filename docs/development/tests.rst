.. _testing:

Testing
-----------------------

To run the test suite, you can use the following command:

.. code-block:: shell

    pytest


Long tests
~~~~~~~~~~~~~

Please note that by default all the tests based on remote services e.g. :ref:`data-sources-mars` are skipped. This is done because they can take a very long time to complete or just hang. To enable all these tests you need to run:

.. code-block:: shell

    pytest -E long -v

If just want to run e.g. the :ref:`data-sources-mars` tests you can use:

.. code-block:: shell

    pytest -E long -v -k mars


Timeout for CDS tests
~~~~~~~~~~~~~~~~~~~~~~

Some :ref:`data-sources-cds` retrieval tests used to hang so an execution timeout was added to all the tests in ``tests/sources/test_cds.py``. The default value is 30 seconds and it can be controlled via the ``--cds-timeout`` custom option to ``pytest``. Please note that some tests have a custom hardcoded timeout value that cannot be changed via this option.

E.g. to set the timeout to 60 seconds for all CDS tests run (supposing their names contain "test_cds"):

.. code-block:: shell

    pytest -E long --cds-timeout=60 -v -k test_cds


Credentials
~~~~~~~~~~~~~~~

Some tests require credentials to access remote services. The existence of credentials are checked and the related tests are skipped accordingly. The logic can be found in ``src/earthkit/data/testing.py``.

FDB tests
~~~~~~~~~~~~

The :ref:`data-sources-fdb` tests are only run if ``pyfdb`` can be imported and the ``FDB_HOME`` environment variable is set. See the logic in ``src/earthkit/data/testing.py``.


Optional dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests generally require all optional dependencies to be installed. However, the availability of some optional dependencies are checked and the related tests are skipped accordingly. This is typically used for dependencies which are not part of the ``[all]`` install option (see :ref:`install`). The logic can be found in ``src/earthkit/data/testing.py``.


no_cache_init tests
~~~~~~~~~~~~~~~~~~~

Tests marked with ``pytest.mark.no_cache_init`` use the ``pytest-forked`` plugin to run in a separate process. They must be run as:

.. code-block:: shell

    pytest --forked -v -m no_cache_init


Notebooks
~~~~~~~~~~~~~

The notebook examples from the ``docs/examples`` folder are part of the test suite and are run automatically. However, some notebooks are skipped mainly because they use remote data sources. This is controlled via the ``SKIP`` list in ``tests/documentation/test_notebooks.py``. You can modify this list to add or remove notebooks to be skipped.

To run only the notebooks tests you can use:

.. code-block:: shell

    pytest -v -m notebook


Documentation code snippets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All ``.py`` files in the ``docs`` folder can potentially contain example code snippets and are part of the test suite and run automatically. Many of these are actually not examples and skipped. This is controlled via the ``SKIP`` list in ``tests/documentation/test_examples.py``. You can modify this list to add or remove snippets to be skipped.
