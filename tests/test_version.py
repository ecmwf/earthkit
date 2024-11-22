#!/usr/bin/env python3

# (C) Copyright 2023 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import re
from importlib.metadata import version

import pytest

VERSION_RX = re.compile(r"""\d+\.\d+\.*""")


def test_version():
    import earthkit

    assert VERSION_RX.match(earthkit.__version__) is not None
    assert VERSION_RX.match(earthkit.data.__version__) is not None


def test_earthkit_data_version_1():
    import earthkit.data

    assert VERSION_RX.match(earthkit.data.__version__) is not None


def test_earthkit_data_version_2():
    from earthkit import data

    assert VERSION_RX.match(data.__version__) is not None


def test_earthkit_data_import():
    import earthkit.data  # noqa
    from earthkit.data import from_source  # noqa


def test_earthkit_data_obj_1():
    import earthkit.data

    assert callable(earthkit.data.from_source)


def test_earthkit_data_obj_2():
    from earthkit import data

    assert callable(data.from_source)


def test_earthkit_geo_version_1():
    import earthkit.geo  # noqa

    assert VERSION_RX.match(earthkit.geo.__version__) is not None


def test_earthkit_geo_version_2():
    from earthkit import geo  # noqa

    assert VERSION_RX.match(geo.__version__) is not None


def test_earthkit_geo_import():
    import earthkit.geo  # noqa
    from earthkit.geo import nearest_point_kdtree  # noqa


def test_earthkit_geo_obj_1():
    import earthkit.geo

    assert callable(earthkit.geo.nearest_point_kdtree)


def test_earthkit_geo_obj_2():
    from earthkit import geo

    assert callable(geo.nearest_point_kdtree)


def test_earthkit_meteo_version_1():
    import earthkit.meteo  # noqa

    assert VERSION_RX.match(earthkit.meteo.__version__) is not None


def test_earthkit_meteo_version_2():
    from earthkit import meteo  # noqa

    assert VERSION_RX.match(meteo.__version__) is not None


def test_earthkit_meteo_import():
    import earthkit.meteo  # noqa
    from earthkit.meteo import thermo  # noqa


def test_earthkit_meteo_obj_1():
    import earthkit.meteo

    assert callable(earthkit.meteo.thermo.potential_temperature)


def test_earthkit_meteo_obj_2():
    from earthkit import meteo

    assert callable(meteo.thermo.potential_temperature)


def test_earthkit_plots_version_1():
    import earthkit.plots  # noqa

    assert VERSION_RX.match(earthkit.plots.__version__) is not None


def test_earthkit_plots_version_2():
    from earthkit import plots  # noqa

    assert VERSION_RX.match(plots.__version__) is not None


def test_earthkit_plots_import():
    import earthkit.plots  # noqa
    from earthkit.plots import quickmap  # noqa


def test_earthkit_plots_obj_1():
    import earthkit.plots

    assert callable(earthkit.plots.quickmap.plot)


def test_earthkit_plots_obj_2():
    from earthkit import plots

    assert callable(plots.quickmap.plot)


def test_earthkit_regrid_version_1():
    import earthkit.regrid  # noqa

    assert VERSION_RX.match(earthkit.regrid.__version__) is not None


def test_earthkit_regrid_version_2():
    from earthkit import regrid  # noqa

    assert VERSION_RX.match(regrid.__version__) is not None


def test_earthkit_regrid_import():
    import earthkit.regrid  # noqa
    from earthkit.regrid import interpolate  # noqa


def test_earthkit_regrid_obj_1():
    import earthkit.regrid

    assert callable(earthkit.regrid.interpolate)


def test_earthkit_regrid_obj_2():
    from earthkit import regrid

    assert callable(regrid.interpolate)


def test_earthkit_time_version_1():
    import earthkit.time  # noqa

    assert VERSION_RX.match(version("earthkit.time")) is not None


@pytest.mark.xfail(reason="version not available")
def test_earthkit_time_version_2():
    from earthkit import time  # noqa

    assert VERSION_RX.match(time.__version__) is not None


def test_earthkit_time_import():
    import earthkit.time  # noqa
    from earthkit.time import DailySequence  # noqa


def test_earthkit_time_obj_1():
    import earthkit.time

    x = earthkit.time.DailySequence()
    assert x is not None


def test_earthkit_time_obj_2():
    from earthkit import time

    x = time.DailySequence()
    assert x is not None


def test_earthkit_transforms_version_1():
    import earthkit.transforms  # noqa

    assert VERSION_RX.match(earthkit.transforms.__version__) is not None


def test_earthkit_transforms_version_2():
    from earthkit import transforms  # noqa

    assert VERSION_RX.match(transforms.__version__) is not None


def test_earthkit_transforms_import():
    import earthkit.transforms  # noqa
    from earthkit.transforms import aggregate  # noqa


def test_earthkit_transforms_obj_1():
    import earthkit.transforms

    assert callable(earthkit.transforms.aggregate.spatial.masks)


def test_earthkit_transforms_obj_2():
    from earthkit import transforms

    assert callable(transforms.aggregate.spatial.masks)
