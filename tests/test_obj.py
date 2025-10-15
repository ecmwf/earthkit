#!/usr/bin/env python3

# (C) Copyright 2023 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import pytest


def test_earthkit_data_obj_1():
    import earthkit.data as ekd

    assert callable(ekd.from_source)


def test_earthkit_data_obj_2():
    from earthkit import data

    assert callable(data.from_source)


def test_earthkit_data_obj_3():
    import earthkit as ek

    assert callable(ek.data.from_source)


def test_earthkit_geo_obj_1():
    import earthkit.geo as ekg

    assert callable(ekg.nearest_point_kdtree)


def test_earthkit_geo_obj_2():
    from earthkit import geo

    assert callable(geo.nearest_point_kdtree)


def test_earthkit_geo_obj_3():
    import earthkit as ek

    assert callable(ek.geo.nearest_point_kdtree)


def test_earthkit_hydro_obj_1():
    import earthkit.hydro as ekh

    assert callable(ekh.river_network.load)


def test_earthkit_hydro_obj_2():
    from earthkit import hydro

    assert callable(hydro.river_network.load)


def test_earthkit_hydro_obj_3():
    import earthkit as ek

    assert callable(ek.hydro.river_network.load)


@pytest.mark.skip(reason="does not work")
def test_earthkit_meteo_obj_1():
    import earthkit.meteo as ekm

    assert callable(ekm.thermo.potential_temperature)


@pytest.mark.skip(reason="does not work")
def test_earthkit_meteo_obj_2():
    from earthkit import meteo

    assert callable(meteo.thermo.potential_temperature)


@pytest.mark.skip(reason="does not work")
def test_earthkit_meteo_obj_3():
    import earthkit as ek

    assert callable(ek.meteo.thermo.potential_temperature)


@pytest.mark.skip(reason="does not work")
def test_earthkit_plots_obj_1():
    import earthkit.plots as ekp

    assert callable(ekp.quickmap.plot)


@pytest.mark.skip(reason="does not work")
def test_earthkit_plots_obj_2():
    from earthkit import plots

    assert callable(plots.quickmap.plot)


@pytest.mark.skip(reason="does not work")
def test_earthkit_plots_obj_3():
    import earthkit as ek

    assert callable(ek.plots.quickmap.plot)


def test_earthkit_regrid_obj_1():
    import earthkit.regrid as ekr

    assert callable(ekr.interpolate)


def test_earthkit_regrid_obj_2():
    from earthkit import regrid

    assert callable(regrid.interpolate)


def test_earthkit_regrid_obj_3():
    import earthkit as ek

    assert callable(ek.regrid.interpolate)


def test_earthkit_time_obj_1():
    import earthkit.time as ektime

    x = ektime.DailySequence()
    assert x is not None


def test_earthkit_time_obj_2():
    from earthkit import time

    x = time.DailySequence()
    assert x is not None


def test_earthkit_time_obj_3():
    import earthkit as ek

    x = ek.time.DailySequence()
    assert x is not None


@pytest.mark.skip(reason="does not work")
def test_earthkit_transforms_obj_1():
    import earthkit.transforms as ekt

    assert callable(ekt.aggregate.spatial.masks)


@pytest.mark.skip(reason="does not work")
def test_earthkit_transforms_obj_2():
    from earthkit import transforms

    assert callable(transforms.aggregate.spatial.masks)


@pytest.mark.skip(reason="does not work")
def test_earthkit_transforms_obj_3():
    import earthkit as ek

    assert callable(ek.transforms.aggregate.spatial.masks)


@pytest.mark.skip(reason="does not work")
def test_earthkit_utils_obj_1():
    import earthkit.utils as eku

    assert callable(eku.array.array_to_numpy)


@pytest.mark.skip(reason="does not work")
def test_earthkit_utils_obj_2():
    from earthkit import utils

    assert callable(utils.array.array_to_numpy)


@pytest.mark.skip(reason="does not work")
def test_earthkit_utils_obj_3():
    import earthkit as ek

    assert callable(ek.utils.array.array_to_numpy)


def test_earthkit_workflows_obj_1():
    import earthkit.workflows as ekw

    assert callable(ekw.fluent.Payload)


def test_earthkit_workflows_obj_2():
    from earthkit import workflows

    assert callable(workflows.fluent.Payload)


def test_earthkit_workflows_obj_3():
    import earthkit as ek

    assert callable(ek.workflows.fluent.Payload)
