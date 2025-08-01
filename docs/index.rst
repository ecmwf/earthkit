Welcome to earthkit's documentation
======================================================

.. warning::

   This project is in the **BETA** stage of development. Please be aware that interfaces and functionality may change as the project develops. If this software is to be used in operational systems you are **strongly advised to use a released tag in your system configuration**, and you should be willing to accept incoming changes and bug fixes that require adaptations on your part. ECMWF **does use** this software in operations and abides by the same caveats.

**earthkit** is a new open-source Python project led by ECMWF, providing powerful tools for speeding up weather and climate science workflows by simplifying data access, processing, analysis, visualisation and much more.

**earthkit** offers **multiple interoperable** :ref:`software components <components>` built on top of well-established open-source Python libraries like numpy, pandas and matplotlib. earthkit also integrates and leverages the robust and operations-ready software stack that is familiar to ECMWF production systems (e.g. :xref:`eccodes`, FDB, etc).

The interface of :ref:`earthkit components <components>` is designed to be high-level in order to provide common tools to support activities across ECMWF and beyond. The design of the components also takes **scalability** into account, so researchers can enjoy efficiency whilst providing easier transfer to operations.

**earthkit** is still under development but some components are already available in beta through PyPI and their GitHub repositories.

.. toctree::
   :maxdepth: 1
   :caption: Examples

   examples/index

.. toctree::
    :maxdepth: 1
    :caption: Components
    :titlesonly:

    components_overview
    earthkit-data <https://earthkit-data.readthedocs.io>
    earthkit-geo <https://earthkit-geo.readthedocs.io>
    earthkit-hydro <https://github.com/ecmwf/earthkit-hydro>
    earthkit-meteo <https://earthkit-meteo.readthedocs.io>
    earthkit-plots <https://earthkit-plots.readthedocs.io>
    earthkit-regrid <https://earthkit-regrid.readthedocs.io>
    earthkit-time <https://earthkit-time.readthedocs.io>
    earthkit-transforms <https://earthkit-transforms.readthedocs.io>
    earthkit-workflows <https://github.com/ecmwf/earthkit-workflows/blob/develop/readme.md>

.. toctree::
   :maxdepth: 1
   :caption: Installation
   :titlesonly:

   install
   licence

Indices and tables
==================

* :ref:`genindex`

.. * :ref:`modindex`
.. * :ref:`search`
