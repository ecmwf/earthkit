# (C) Copyright 2023- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import importlib
import pkgutil
import threading

_lock = threading.RLock()

__all__ = (
    name
    for _, name, ispkg in pkgutil.iter_modules(__path__)
    if ispkg and not name.startswith("_") and not name in {"importlib", "pkgutil", "threading"}
)


def __getattr__(name):
    if name not in __all__:
        raise AttributeError(f"No such submodule: {name}")

    with _lock:
        if name in globals():
            return globals()[name]
        mod = importlib.import_module(f"{__name__}.{name}")
        globals()[name] = mod
    return mod


def __dir__():
    return tuple(globals()) + __all__
