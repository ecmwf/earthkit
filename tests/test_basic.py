#!/usr/bin/env python3

# (C) Copyright 2023 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

def test_basic():
    import earthkit.data
    from earthkit.data.testing import earthkit_examples_file
    ds = earthkit.data.from_source("file", earthkit_examples_file("test.grib"))
    assert len(ds) == 2



