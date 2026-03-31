Earthkit 
=========

.. tip::

   For an interactive overview, see the `earthkit website <https://earthkit.ecmwf.int/>`__.

**earthkit** is a new open-source Python project led by ECMWF, providing powerful tools for speeding up weather
and climate science workflows by simplifying data access, processing, analysis, visualisation and much more.

**earthkit** offers **multiple interoperable** :ref:`software components <components>` built on top of
well-established open-source Python libraries like numpy, pandas and matplotlib. earthkit also integrates
and leverages the robust and operations-ready software stack that is familiar to ECMWF production systems
(e.g. ecCodes, FDB, etc).

The interface of :ref:`earthkit components <components>` is designed to be high-level in order to provide common tools to support activities across ECMWF and beyond. The design of the components also takes **scalability** into account, so researchers can enjoy efficiency whilst providing easier transfer to operations.

**earthkit** is still under development but some components are already available in beta through PyPI and their GitHub repositories.


.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: Installation and Getting Started
      :img-top: _static/rocket.svg
      :link: getting-started
      :link-type: doc
      :class-card: sd-shadow-sm

      New to earthkit? Start here with installation and a quick overview.


   .. grid-item-card:: Tutorials
      :img-top: _static/book.svg
      :link: tutorials/index
      :link-type: doc
      :class-card: sd-shadow-sm

      Step-by-step guides to learn earthkit.



**Support**

Have a feature request or found a bug? Feel free to open an
`issue <https://github.com/ecmwf/earthkit/issues/new/choose>`_.



.. toctree::
   :caption: User guide
   :maxdepth: 2
   :hidden:

   getting-started
   tutorials/index



.. toctree::
   :maxdepth: 1
   :caption: Developer guide
   :hidden:

   development/index


.. toctree::
   :maxdepth: 1
   :caption: Installation and Getting Started
   :titlesonly:
   :hidden:

   getting-started


.. toctree::
   :maxdepth: 2
   :caption: Extras
   :hidden:

   licence
