Welcome to earthkit's documentation
======================================================

|Static Badge| |image1| |License: Apache 2.0|

.. |Static Badge| image:: https://github.com/ecmwf/codex/raw/refs/heads/main/ESEE/foundation_badge.svg
   :target: https://github.com/ecmwf/codex/raw/refs/heads/main/ESEE
.. |License: Apache 2.0| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/apache-2-0

For an interactive overview, see the `earthkit website <https://ecmwf.github.io/earthkit-website/>`__.

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
    earthkit-hydro <https://earthkit-hydro.readthedocs.io>
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
