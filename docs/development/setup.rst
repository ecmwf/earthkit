.. _dev_setup:

Development setup with virtualenv
-----------------------------------

The recommended development environment is a **Python virtual environment**.

First, clone the repository locally. You can use the following command:

.. code-block:: shell

   git clone --branch develop git@github.com:ecmwf/earthkit.git


Next, create your Python virtual environment and activate it. E.g. assuming your virtual environment is called `earthkit-dev` you can do:

.. code-block:: shell

   cd YOUR_VENVS_DIR
   python -m venv earthkit-dev
   source earthkit-dev/bin/activate

If you use `conda`, the equivalent would be:

.. code-block:: shell

   conda create -n earthkit-dev python=3.12
   conda activate earthkit-dev


Next, install your repo with the development dependencies in editable mode by running the following commands from the root of the repository:

.. code-block:: shell

   pip install -e .


We strongly recommend using the `pre-commit`_ hooks for the developments. These hooks perform a series of quality control checks on every commit. If any of these checks fails the commit will be rejected. To install the hooks run the following commands in the root of the repository:

.. code-block:: shell

    pip install pre-commit
    pre-commit install

.. _`pre-commit`: https://pre-commit.com/
