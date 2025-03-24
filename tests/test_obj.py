#!/usr/bin/env python3

# (C) Copyright 2023 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#


def test_earthkit_data_obj_1():
    import earthkit.data

    assert callable(earthkit.data.from_source)


def test_earthkit_data_obj_2():
    from earthkit import data

    assert callable(data.from_source)


def test_earthkit_geo_obj_1():
    import earthkit.geo

    assert callable(earthkit.geo.nearest_point_kdtree)


def test_earthkit_geo_obj_2():
    from earthkit import geo

    assert callable(geo.nearest_point_kdtree)


def test_earthkit_hydro_obj_1():
    import earthkit.hydro

    assert callable(earthkit.hydro.river_network.load)


def test_earthkit_hydro_obj_2():
    from earthkit import hydro

    assert callable(hydro.river_network.load)


def test_earthkit_meteo_obj_1():
    import earthkit.meteo

    assert callable(earthkit.meteo.thermo.potential_temperature)


def test_earthkit_meteo_obj_2():
    from earthkit import meteo

    assert callable(meteo.thermo.potential_temperature)


def test_earthkit_plots_obj_1():
    import earthkit.plots

    assert callable(earthkit.plots.quickmap.plot)


def test_earthkit_plots_obj_2():
    from earthkit import plots

    assert callable(plots.quickmap.plot)


def test_earthkit_regrid_obj_1():
    import earthkit.regrid

    assert callable(earthkit.regrid.interpolate)


def test_earthkit_regrid_obj_2():
    from earthkit import regrid

    assert callable(regrid.interpolate)


def test_earthkit_time_obj_1():
    import earthkit.time

    x = earthkit.time.DailySequence()
    assert x is not None


def test_earthkit_time_obj_2():
    from earthkit import time

    x = time.DailySequence()
    assert x is not None


def test_earthkit_transforms_obj_1():
    import earthkit.transforms

    assert callable(earthkit.transforms.aggregate.spatial.masks)


def test_earthkit_transforms_obj_2():
    from earthkit import transforms

    assert callable(transforms.aggregate.spatial.masks)
