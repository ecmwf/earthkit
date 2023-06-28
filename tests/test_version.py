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


def test_earthkit_maps_version():
    import earthkit.maps  # noqa

    # assert VERSION_RX.match(earthkit.maps.__version__) is not None
