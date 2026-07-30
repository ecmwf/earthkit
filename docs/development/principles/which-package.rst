Where should my function go?
============================

Functionality in the ``earthkit`` ecosystem is split across a small number of
packages, each with a well-defined scope. Before adding a new function, consider
which package is the most appropriate home.

* ``earthkit-data``

  Reading, writing, indexing and manipulating Earth science datasets. This
  includes access to local and remote data, file formats, metadata, and data
  containers.

* ``earthkit-geo``

  Geospatial functionality, including coordinate systems, grids, spatial
  operations, interpolation, and geographic utilities.

* ``earthkit-meteo``

  Meteorological algorithms and calculations.

* ``earthkit-hydro``

  Hydrological algorithms and calculations.

* ``earthkit-plots``

  Visualisation and plotting functionality for Earth science data.

* ``earthkit-transforms``

  General data transformations that are not specific to a particular scientific
  domain e.g. temporal aggregations (climatologies) etc.

* ``earthkit-utils``

  Shared utilities used across the ``earthkit`` ecosystem. This package should
  contain generic infrastructure (for example dispatch mechanisms, common
  decorators and helper utilities) rather than user-facing scientific
  functionality.

General guidelines
------------------

* Domain-specific algorithms belong in the relevant domain package (for example,
  meteorological calculations in ``earthkit-meteo`` and hydrological
  calculations in ``earthkit-hydro``).
* Infrastructure and reusable implementation helpers belong in
  ``earthkit-utils``.
* Avoid introducing duplicate functionality across packages.
* If functionality could reasonably fit in more than one package, prefer the
  package with the narrower, more natural scope.

If you are still unsure after reading this guide, please open an issue on
GitHub.
