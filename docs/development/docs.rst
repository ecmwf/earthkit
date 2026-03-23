.. _dev_docs:


Documentation
-------------------

Building the documentation locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build the documentation locally, please install the Python dependencies first:

.. code-block:: shell

    cd docs
    pip install -r requirements.txt

Then the documentation can be built by running the following command from the ``docs`` folder:

.. code-block:: shell

    make html

To see the generated HTML documentation open the ``docs/_build/html/index.html`` file in your browser.

Notebook examples
~~~~~~~~~~~~~~~~~~~~~~

The notebook examples are located in the ``docs/examples`` folder and are listed in ``docs/examples/index.rst``.


If you add a new notebook example please:

- also add it to ``docs/examples/index.rst`` so that it appears in the documentation.
- ensure the title and the subchapter headings have the same size as in the other notebook. Title with ``##``, subchapter with ``###``.
