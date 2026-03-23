.. _conda_setup:

Development setup with Conda
------------------------------

You can set up a development environment using Conda. Below are the instructions to do so.

First, clone the repository locally. You can use the following command:

.. code-block:: shell

   git clone --branch develop git@github.com:ecmwf/earthkit.git


Next, enter your git repository and run the following commands:

.. code-block:: shell

    make conda-env-update
    conda activate earthkit
    make setup
    pip install -e .

This will create a new conda environment called "earthkit" with all the dependencies installed into it. This setup enables the `pre-commit`_ hooks, performing a series of quality control checks on every commit. If any of these checks fails the commit will be rejected.
