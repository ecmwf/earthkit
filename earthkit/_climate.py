"""
Package for hypercube operations, such as calculating daily/monthly/climatologicial statistics.

Although typically over geographical and temporal dimensions, the operations are not limited to this.

Code makes use of xarray and pandas data representation and functionality but with numerical operations
optimised for highest performance.
"""

from earthkit import climate as _climate
import xarray as xr

from earthkit._inputs_transform import transform_function_inputs, transform_module_inputs

KWARG_TYPES = {
    "dataarray": xr.DataArray,
    "dataset": xr.Dataset,
    # "data": np.ndarray,
}

aggregate = transform_module_inputs(_climate.aggregate, kwarg_types=KWARG_TYPES)

climatology = transform_module_inputs(_climate.climatology, kwarg_types=KWARG_TYPES)


