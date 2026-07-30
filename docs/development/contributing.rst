Contributing
============

**earthkit** is an open-source project, and contributions are highly welcomed and appreciated for all components.

The code is hosted on GitHub:
- `earthkit <https://github.com/ecmwf/earthkit>`_
- `earthkit-data <https://github.com/ecmwf/earthkit-data>`_
- `earthkit-plots <https://github.com/ecmwf/earthkit-plots>`_
- `earthkit-meteo <https://github.com/ecmwf/earthkit-meteo>`_
- `earthkit-geo <https://github.com/ecmwf/earthkit-geo>`_
- `earthkit-transforms <https://github.com/ecmwf/earthkit-transforms>`_
- `earthkit-hydro <https://github.com/ecmwf/earthkit-hydro>`_
- `earthkit-utils <https://github.com/ecmwf/earthkit-utils>`_


Development workflow
--------------------

1. Fork the repository on GitHub
2. Clone the fork to your local machine
3. Create a virtual environment and install the package in development mode
4. Create a new branch for your changes
5. Make your changes and commit them with a clear message
6. Run tests to ensure everything is working correctly
7. Push your changes to your fork on GitHub
8. Open a pull request against the develop branch of the repository

Code style
----------
This project uses ruff for code styling and formatting. To handle these automatically, you can use pre-commit hooks. To set them up, run:

.. code-block:: bash

    pip install pre-commit
    pre-commit install

Testing
-------
To run the tests, you can use pytest. Make sure you have all dependencies installed, then simply run:

.. code-block:: bash

    pytest

Documentation
-------------
To contribute to the documentation, see the developer
resources in the docs:

- :doc:`documentation` — short guidance for authors (Diátaxis)
