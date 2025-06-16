# (C) Copyright 2023- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import importlib
import sys
import types

from ._version import __version__


class EarthkitModuleProxy(types.ModuleType):
    def __getattr__(self, name):
        full = f"{__name__}.{name}"
        mod = importlib.import_module(full)
        setattr(self, name, mod)
        return mod


current = sys.modules[__name__]
proxy = EarthkitModuleProxy(current.__name__)
proxy.__dict__.update(current.__dict__)
sys.modules[__name__] = proxy
