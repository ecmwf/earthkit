Welcome to earthkit's documentation
======================================================

.. warning::

    This project is **BETA** and will be **Experimental** for the foreseeable future. Interfaces and functionality are likely to change, and the project itself may be scrapped. **DO NOT** use this software in any project/software that is operational.

**earthkit** is a new open-source Python project led by ECMWF, providing powerful tools for speeding up weather and climate science workflows by simplifying data access, processing, analysis, visualisation and much more.

**earthkit** offers **multiple interoperable** :ref:`software components <components>` built on top of well-established open-source Python libraries like numpy, pandas and matplotlib. earthkit also integrates and leverages the robust and operations-ready software stack that is familiar to ECMWF production systems (e.g. :xref:`eccodes`, FDB, etc).

The interface of :ref:`earthkit components <components>` is designed to be high-level in order to provide common tools to support activities across ECMWF and beyond. The design of the components also takes **scalability** into account, so researchers can enjoy efficiency whilst providing easier transfer to operations.

**earthkit** is still under development but some components are already available in beta through PyPI and their GitHub repositories.

.. .. toctree::
..    :maxdepth: 1
..    :caption: Examples
..    :titlesonly:

..    examples

.. toctree::
    :maxdepth: 1
    :caption: Components
    :titlesonly:

    components_overview
    earthkit-data <https://earthkit-data.readthedocs.io>
    earthkit-geo <https://earthkit-geo.readthedocs.io>
    earthkit-maps <https://earthkit-maps.readthedocs.io>
    earthkit-meteo <https://earthkit-meteo.readthedocs.io>
    earthkit-plots <https://pypi.org/project/earthkit-plots>
    earthkit-regrid <https://earthkit-regrid.readthedocs.io>

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
