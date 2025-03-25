#!/usr/bin/env python3

# (C) Copyright 2023 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


def test_earthkit_data_import():
    import earthkit.data  # noqa
    from earthkit.data import from_source  # noqa


def test_earthkit_geo_import():
    import earthkit.geo  # noqa
    from earthkit.geo import nearest_point_kdtree  # noqa


def test_earthkit_transforms_import():
    import earthkit.transforms  # noqa
    from earthkit.transforms import aggregate  # noqa


def test_earthkit_hydro_import():
    import earthkit.hydro  # noqa
    from earthkit.hydro import river_network  # noqa


def test_earthkit_meteo_import():
    import earthkit.meteo  # noqa
    from earthkit.meteo import thermo  # noqa


def test_earthkit_plots_import():
    import earthkit.plots  # noqa
    from earthkit.plots import quickmap  # noqa


def test_earthkit_regrid_import():
    import earthkit.regrid  # noqa
    from earthkit.regrid import interpolate  # noqa


def test_earthkit_time_import():
    import earthkit.time  # noqa
    from earthkit.time import DailySequence  # noqa
