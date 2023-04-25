
import coucal as _coucal
import xarray as xr

from earthkit._inputs_transform.__main__ import transform_module_inputs

KWARG_TYPES = {
    "dataarray": xr.DataArray,
    "dataset": xr.Dataset,
    # "data": np.ndarray,
}

aggregate = transform_module_inputs(_coucal.aggregate, kwarg_types=KWARG_TYPES)

climate = transform_module_inputs(_coucal.climate, kwarg_types=KWARG_TYPES)
