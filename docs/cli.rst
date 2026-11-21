Command line interface
======================

Installing earthkit provides a single ``earthkit`` command. Each earthkit package
adds its own commands to it, so the commands available depend on the packages
installed. To list the installed packages, their versions and the commands each
of them provides, run:

.. code-block:: bash

    earthkit info

Use ``earthkit -h`` to list the commands, and ``earthkit COMMAND -h`` for the
syntax and options of a command.

Commands
--------

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Package
     - Commands
     - Description
   * - earthkit-data
     - ``ls``, ``convert``, ``sel``, ``isel``, ``order_by``
     - List, convert, select and reorder data.
   * - earthkit-transforms
     - ``daily-agg``, ``monthly-agg``, ``yearly-agg``
     - Temporal aggregation.
   * - earthkit-geo
     - ``regrid``
     - Regridding.
   * - earthkit-plots
     - ``plot``
     - Plotting data on a map.

See the documentation of each package for the details of its commands, e.g. the
`earthkit-data command line interface <https://earthkit-data.readthedocs.io/en/latest/concepts/cli/index.html>`__.

Sources and targets
-------------------

Commands read data from a ``SOURCE`` and write it to a ``TARGET``, both given as
``[NAME:]VALUE``, where ``NAME`` is an earthkit-data source or target (``file``
if not given):

.. code-block:: bash

    earthkit sel input.grib output.grib --parameter.variable t      # files
    earthkit ls 'data/*.nc'                                          # glob
    earthkit ls url:https://myhost.int/file.nc                       # any earthkit-data source
    earthkit convert 'mars:{"param": "2t", "levtype": "sfc", "date": "-1"}' 2t.nc
    earthkit convert 'cds:{"dataset": "reanalysis-era5-single-levels", "variable": "2m_temperature", "year": "2020"}' t2m.nc

A JSON ``VALUE`` is passed to the source as its request, with its ``dataset`` key,
if any, as the first argument. ``-`` reads GRIB data from stdin or writes to
stdout, so commands can be piped:

.. code-block:: bash

    cat input.grib | earthkit order_by - - --key vertical.level | earthkit sel - out.grib --parameter.variable t

Limitations
-----------

Streaming sources
~~~~~~~~~~~~~~~~~

Some earthkit-data sources stream their data by default, e.g. ``polytope`` and
``fdb``, and so does stdin (``-``). A stream can only be read once, from start to
end. ``ls``, ``sel``, ``isel``, ``order_by`` and ``regrid`` work with these
sources. Commands that convert the data to Xarray (``convert``, ``daily-agg``,
``monthly-agg`` and ``yearly-agg``) or need random access to it (``plot``) cannot
use them, and fail with a ``NotImplementedError``.

Source keyword arguments
~~~~~~~~~~~~~~~~~~~~~~~~

The keyword arguments of a source, e.g. ``stream=False`` for ``polytope``, cannot
be given on the command line. The JSON ``VALUE`` is the request of the source, and
many request languages already use these names, e.g. ``"stream": "oper"`` in a
MARS request, so the two cannot be told apart.

To use the data of a streaming source with one of these commands, write it to a
file first, e.g. with ``sel``, and run the command on the file:

.. code-block:: bash

    earthkit sel 'polytope:{"dataset": "ecmwf-mars", "class": "od", "stream": "oper", "type": "fc", "param": "2t"}' 2t.grib --parameter.variable 2t
    earthkit plot 2t.grib

or use the Python API, where ``earthkit.data.from_source("polytope", ..., stream=False)``
retrieves the data to the cache.
