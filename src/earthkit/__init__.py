# (C) Copyright 2025- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import importlib
import pkgutil
import threading

try:
    from earthkit._version import __version__
except:
    __version__ = -1  # decide what to put as a placeholder here

_lock = threading.RLock()

# declare as namespace (older pre PEP 420 approach)
__path__ = pkgutil.extend_path(__path__, __name__)

EXCLUDE = {"importlib", "pkgutil", "threading"}
discovered = {
    name
    for _, name, ispkg in pkgutil.iter_modules(__path__)
    if ispkg and not name.startswith("_") and name not in EXCLUDE
}
# reproducible ordering
__all__ = tuple(sorted(discovered))


# dynamic and lazy module loading
def __getattr__(name):
    with _lock:
        if name in globals():
            return globals()[name]
        try:
            mod = importlib.import_module(f"{__name__}.{name}")
        except Exception as e:
            raise AttributeError(
                f"Module '{__name__}' has no attribute '{name}' " f"(failed to import '{__name__}.{name}'): {e}"
            ) from e
        globals()[name] = mod
        return mod


def __dir__():
    return tuple(globals()) + __all__
