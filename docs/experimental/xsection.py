# (C) Copyright 2024 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

"""Experimental cross-section helper for the notebooks in ``docs/experimental``.

The helper turns data (a fieldlist or xarray data) and the points sampled along a
line into an :class:`xarray.Dataset` that is ready to be plotted as a vertical
cross-section. Fieldlists are converted to xarray first; everything else is done
with xarray.

Functions
---------
cross_section
    Build the cross-section (a CF-style :class:`xarray.Dataset`) from data and the
    points of a line.
wind_components
    Add the wind components normal to and parallel with the cross-section.
geometric_height
    Geometric height (m) from geopotential.
orography
    Orography (m) from the surface geopotential.
pressure_to_height
    Interpolate the variables of a pressure-level cross-section to height levels.
hybrid_coefficients
    Hybrid level coefficients (A, B) of the model levels of fieldlist or xarray data.
surface_pressure
    Surface pressure (Pa) from the logarithm of the surface pressure.
pressure_on_model_levels
    Pressure (Pa) on the model levels of a cross-section.
height_on_model_levels
    Geometric height (m) on the model levels of a cross-section.
model_to_pressure
    Interpolate the variables of a model-level cross-section to pressure levels.
model_to_height
    Interpolate the variables of a model-level cross-section to height levels.

The vertical functions of earthkit-meteo for model levels do not work with xarray
yet, so the model-level helpers call their numpy implementations with the values of
the cross-section and wrap the results into xarray objects.
"""

import numpy as np
import xarray as xr
from earthkit.geo import regrid
from earthkit.geo.distance import haversine_distance
from earthkit.geo.polyline import polyline_normals
from earthkit.meteo import vertical

# dimensions added when a fieldlist is converted to xarray (squeezed when they have a single value)
_TIME_DIMS = ("forecast_reference_time", "step")

# CF attributes of the coordinates of the result
_DISTANCE_ATTRS = {"long_name": "distance along the cross-section", "units": "km"}
_LATITUDE_ATTRS = {"standard_name": "latitude", "long_name": "latitude", "units": "degrees_north"}
_LONGITUDE_ATTRS = {"standard_name": "longitude", "long_name": "longitude", "units": "degrees_east"}

# CF attributes of the results of the helpers
_HEIGHT_ATTRS = {"standard_name": "altitude", "long_name": "geometric height", "units": "m"}
_OROGRAPHY_ATTRS = {"standard_name": "surface_altitude", "long_name": "orography", "units": "m"}
_HEIGHT_COORD_ATTRS = {
    "standard_name": "altitude",
    "long_name": "height above sea level",
    "units": "m",
    "positive": "up",
    "axis": "Z",
}
_WN_LONG_NAME = "wind component normal to the cross-section, positive to the left of the direction of travel"
_WP_LONG_NAME = "wind component parallel to the cross-section, positive along the direction of travel"

# scalar coordinates of the forecast time added by cross_section() for a fieldlist
_TIME_COORDS = ("forecast_reference_time", "step", "valid_time")


def _check_points(lats, lons):
    lats = np.asarray(lats, dtype=float)
    lons = np.asarray(lons, dtype=float)
    if lats.ndim != 1 or lons.ndim != 1:
        raise ValueError(f"lats and lons must be 1-D arrays, got shapes {lats.shape} and {lons.shape}")
    if lats.shape != lons.shape:
        raise ValueError(f"lats and lons must have the same length, got {lats.size} and {lons.size}")
    if lats.size == 0:
        raise ValueError("lats and lons must not be empty")
    return lats, lons


def _cumulative_distance(lats, lons):
    """Return the distance (km) along the points, starting from 0 at the first point."""
    steps = [float(haversine_distance((lats[i], lons[i]), (lats[i + 1], lons[i + 1]))) for i in range(lats.size - 1)]
    return np.concatenate([[0.0], np.cumsum(steps)]) / 1000.0


def cross_section(data, lats, lons, *, levels=None, interpolation="nn"):
    """Build a cross-section from data and the points of a line.

    A fieldlist is converted to xarray with ``to_xarray()``. The levels are then
    selected and the xarray object is passed unchanged to
    :func:`earthkit.geo.regrid`, which determines the grid from the data. The
    result follows the CF conventions as far as possible.

    Parameters
    ----------
    data: earthkit.data.FieldList, xarray.Dataset or xarray.DataArray
        Data to use. A fieldlist is converted with a single ``to_xarray()`` call
        (with the forecast reference time and the step as dimensions and the valid
        time as a coordinate), so all its fields must be on the same grid.
        Variables on a vertical coordinate must have a ``level`` dimension and
        become variables on (``level``, ``distance``); variables without ``level``
        (e.g. surface pressure) become variables on ``distance``. Other dimensions
        (e.g. ``step``) are kept in front of ``level`` and ``distance``.
    lats: array-like
        1-D latitudes (degrees) of the points of the cross-section.
    lons: array-like
        1-D longitudes (degrees) of the points of the cross-section. Must have
        the same length as ``lats``.
    levels: list of int, optional
        Levels to keep on the ``level`` dimension. Variables without ``level`` are
        not affected. By default all levels are kept.
    interpolation: str, optional
        Interpolation method passed to :func:`earthkit.geo.regrid`. The default is
        "nn" (nearest neighbour).

    Returns
    -------
    xarray.Dataset or xarray.DataArray
        A DataArray when ``data`` is a DataArray, otherwise a Dataset. The result
        has the coordinates ``level`` (sorted ascending, if present; with
        ``axis="Z"``), ``distance`` (km, cumulative along the points, 0 at the
        first point; ``long_name`` and ``units``), and the auxiliary coordinates
        ``latitude`` and ``longitude`` defined on ``distance`` (with
        ``standard_name``, ``long_name`` and ``units``). When ``data`` is a
        fieldlist, the forecast time is kept in the coordinates
        ``forecast_reference_time``, ``step`` (``standard_name="forecast_period"``)
        and ``valid_time`` (``standard_name="time"``). They are scalar when the
        fieldlist has a single forecast time and step; with several steps ``step``
        stays a dimension and ``valid_time`` is defined on it. The variable
        attributes are those returned by regrid (e.g. ``standard_name``,
        ``units`` and ``long_name``); no unit conversion is done. The global
        attributes of a Dataset (e.g. ``Conventions``) are kept, but those set by
        regrid are not replaced and ``_earthkit`` is not copied. The input is not
        modified.

    Raises
    ------
    ValueError
        If ``lats`` and ``lons`` are not 1-D arrays of equal length, if a fieldlist
        cannot be converted to xarray (e.g. fields on different grids or at different
        steps; convert such fields, e.g. the orography at step 0, in a separate call), or if
        ``levels`` is given and the data has no ``level`` dimension or a requested
        level is missing.
    TypeError
        If ``data`` is not a fieldlist or xarray data.

    Notes
    -----
    While regridding, earthkit may log an "Error setting gridSpec" message with a
    traceback. It is harmless: the result is not affected.

    Examples
    --------
    >>> fl = ekd.from_source("sample", "xs_pl_input.grib1").to_fieldlist()
    >>> fl = fl.sel({"parameter.variable": ["t", "sp"], "time.step": timedelta(hours=12)})
    >>> lats, lons = sample_polyline([40, 56], [-10, 10], n=200)
    >>> xs = cross_section(fl, lats, lons)
    >>> xs = cross_section(fl.to_xarray(), lats, lons, levels=[500, 850])
    """
    lats, lons = _check_points(lats, lons)

    # convert the input to an xarray Dataset
    is_dataarray = isinstance(data, xr.DataArray)
    is_fieldlist = False
    if is_dataarray or isinstance(data, xr.Dataset):
        source = data
    elif hasattr(data, "to_xarray"):
        is_fieldlist = True
        try:
            source = data.to_xarray(ensure_dims=list(_TIME_DIMS), add_valid_time_coord=True)
        except Exception as exc:
            raise ValueError(
                f"cannot convert data to xarray ({exc}). All the fields must be on the same grid and share the "
                "same time dimensions (forecast reference time and step). Fields at a different step (e.g. the "
                "orography at step 0) must be converted in a separate call."
            ) from exc
    else:
        raise TypeError(f"data must be a fieldlist, an xarray.Dataset or an xarray.DataArray, got {type(data)}")

    # the global attributes of the input are added to the result later
    global_attrs = {} if is_dataarray else dict(source.attrs)

    if is_dataarray:
        name = source.name
        ds = source.to_dataset(name="__data__")
    else:
        ds = source

    # select the levels
    if levels is not None:
        requested = list(levels)
        if "level" not in ds.dims:
            raise ValueError("levels cannot be selected: data has no 'level' dimension")
        missing = sorted(set(requested) - set(ds["level"].values.tolist()))
        if missing:
            raise ValueError(f"levels {missing} are missing in data")
        ds = ds.sel(level=requested)
    if "level" in ds.dims:
        ds = ds.sortby("level")

    # regrid to the points of the line
    out_grid = {"latitudes": lats.tolist(), "longitudes": lons.tolist()}
    res = regrid(ds, out_grid=out_grid, interpolation=interpolation)
    if "values" not in res.dims:
        raise ValueError(f"regridding did not produce a 'values' dimension, got {list(res.dims)}")

    # a single forecast time and step become scalar coordinates (only for the dims added by the fieldlist conversion)
    if is_fieldlist:
        for dim in _TIME_DIMS:
            if res.sizes.get(dim) == 1:
                res = res.squeeze(dim)

    # build the cross-section: "distance" last, "level" just before it
    res = res.rename_dims({"values": "distance"})
    res = res.assign_coords(
        distance=("distance", _cumulative_distance(lats, lons), _DISTANCE_ATTRS),
        latitude=("distance", lats, _LATITUDE_ATTRS),
        longitude=("distance", lons, _LONGITUDE_ATTRS),
    )
    if "level" in res.coords:
        res["level"].attrs = {**res["level"].attrs, "axis": "Z"}
    res = res.transpose(..., *(["level"] if "level" in res.dims else []), "distance")

    # keep the global attributes (e.g. Conventions) of the input, but never replace those set by regrid()
    res.attrs = {**{k: v for k, v in global_attrs.items() if k != "_earthkit"}, **res.attrs}

    if is_dataarray:
        res = res["__data__"].rename(name)
    return res


def _get_variable(xs, name):
    if name not in xs.data_vars:
        raise ValueError(f"variable '{name}' not found in the cross-section, got {list(xs.data_vars)}")
    return xs[name]


def wind_components(xs, *, method="great_circle", u="u", v="v"):
    """Add the wind components normal to and parallel with the cross-section.

    With ``east, north = polyline_normals(latitude, longitude, method)`` the unit
    normal pointing to the left of the direction of travel, the components are::

        wn = u * east + v * north     (normal, positive to the left of the direction of travel)
        wp = u * north - v * east     (parallel, positive along the direction of travel)

    Parameters
    ----------
    xs: xarray.Dataset
        Cross-section as returned by :func:`cross_section`, with the wind
        components on (..., ``distance``) and the coordinates ``latitude`` and
        ``longitude`` on ``distance``. Extra leading dimensions (e.g. ``step``,
        ``level``) are kept.
    method: str, optional
        Interpolation method for the segments of the line, passed to
        :func:`earthkit.geo.polyline.polyline_normals`. It **must be the same**
        as the one used in :func:`earthkit.geo.polyline.sample_polyline` to
        create the points of the cross-section.
    u: str, optional
        Name of the eastward wind component in ``xs``.
    v: str, optional
        Name of the northward wind component in ``xs``.

    Returns
    -------
    xarray.Dataset
        A copy of ``xs`` with the additional variables ``wn`` and ``wp`` on the
        dimensions of ``u``. Their ``units`` are those of ``u``. ``xs`` is not
        modified.

    Raises
    ------
    ValueError
        If ``u`` or ``v`` are missing, do not have ``distance`` as last
        dimension, if ``xs`` has no ``latitude``/``longitude`` coordinates, or if
        the normals cannot be computed (e.g. a point of the line is at a pole).
    """
    u_da = _get_variable(xs, u)
    v_da = _get_variable(xs, v)
    for name, da in ((u, u_da), (v, v_da)):
        if da.dims[-1:] != ("distance",):
            raise ValueError(f"variable '{name}' must have 'distance' as its last dimension, got {da.dims}")
    if u_da.dims != v_da.dims:
        raise ValueError(f"'{u}' and '{v}' must have the same dimensions, got {u_da.dims} and {v_da.dims}")
    for name in ("latitude", "longitude"):
        if name not in xs.coords or xs[name].dims != ("distance",):
            raise ValueError(f"the cross-section needs a '{name}' coordinate on 'distance'")

    east, north = polyline_normals(xs["latitude"].values, xs["longitude"].values, method=method)
    east = xr.DataArray(east, dims="distance")
    north = xr.DataArray(north, dims="distance")

    units = u_da.attrs.get("units")
    out = xs.copy()
    for name, values, long_name in (
        ("wn", u_da * east + v_da * north, _WN_LONG_NAME),
        ("wp", u_da * north - v_da * east, _WP_LONG_NAME),
    ):
        attrs = {"long_name": long_name}
        if units is not None:
            attrs["units"] = units
        out[name] = values.assign_attrs(attrs)
    return out


def geometric_height(z):
    """Return the geometric height (m) from the geopotential.

    Uses :func:`earthkit.meteo.vertical.geometric_height_from_geopotential`.

    Parameters
    ----------
    z: xarray.DataArray
        Geopotential (m2 s-2), e.g. ``xs["z"]``.

    Returns
    -------
    xarray.DataArray
        Geometric height in m with the dimensions and coordinates of ``z``. Its
        attributes are ``standard_name="altitude"``, ``long_name="geometric height"``
        and ``units="m"``. ``z`` is not modified.
    """
    res = vertical.geometric_height_from_geopotential(z)
    res.attrs = dict(_HEIGHT_ATTRS)
    return res


def orography(zs):
    """Return the orography (m) from the surface geopotential.

    Parameters
    ----------
    zs: xarray.DataArray
        Surface geopotential (m2 s-2) on ``distance``, e.g. ``cross_section(fl_zs,
        lats, lons)["z"]``. The surface geopotential is usually at a different
        step than the other fields and must be converted in a separate
        :func:`cross_section` call.

    Returns
    -------
    xarray.DataArray
        Orography in m, named ``orography``, with the dimensions and coordinates
        of ``zs`` except the scalar time coordinates (``forecast_reference_time``,
        ``step`` and ``valid_time``), which are dropped. Its attributes are
        ``standard_name="surface_altitude"``, ``long_name="orography"`` and
        ``units="m"``. ``zs`` is not modified.
    """
    res = vertical.geometric_height_from_geopotential(zs)
    res = res.drop_vars([c for c in _TIME_COORDS if c in res.coords and res[c].ndim == 0])
    res.attrs = dict(_OROGRAPHY_ATTRS)
    return res.rename("orography")


def pressure_to_height(xs, target_h, *, z="z", names=None, zs=None):
    """Interpolate the variables of a pressure-level cross-section to height levels.

    The height of the pressure levels is the geometric height computed from the
    geopotential ``z`` (see :func:`geometric_height`) and the interpolation is
    linear in height, with
    :func:`earthkit.meteo.vertical.interpolate_pressure_to_height_levels`. Heights
    below the lowest or above the highest pressure level are NaN. Values between
    the height of the lowest level and the orography are not masked.

    Parameters
    ----------
    xs: xarray.Dataset
        Cross-section as returned by :func:`cross_section`, on ``level`` (monotonic)
        and ``distance``. The variables to interpolate and ``z`` must have exactly
        the dimensions (``level``, ``distance``).
    target_h: array-like
        1-D heights (m above sea level) to interpolate to.
    z: str, optional
        Name of the geopotential in ``xs``.
    names: list of str, optional
        Variables to interpolate. By default all the variables with a ``level``
        dimension except ``z``.
    zs: xarray.DataArray, optional
        Surface geopotential on ``distance`` (from a separate
        :func:`cross_section` call). When given, the result has the variable
        ``orography`` (see :func:`orography`).

    Returns
    -------
    xarray.Dataset
        The interpolated variables (in their original units and with their
        attributes, except ``level_type``) on (``height``, ``distance``), plus
        ``orography`` on ``distance`` when ``zs`` is given. The coordinates
        ``distance``, ``latitude``, ``longitude`` and the time coordinates of
        ``xs`` are kept. The ``height`` coordinate has the attributes
        ``standard_name="altitude"``, ``long_name="height above sea level"``,
        ``units="m"``, ``positive="up"`` and ``axis="Z"``. ``xs`` is not modified.

    Raises
    ------
    ValueError
        If ``xs`` has no ``level`` dimension, ``z`` or a variable in ``names`` is
        missing or does not have exactly the dimensions (``level``, ``distance``),
        ``target_h`` is not a non-empty 1-D array, or ``zs`` is not on ``distance``.
    """
    target_h = np.asarray(target_h)
    if target_h.ndim != 1 or target_h.size == 0:
        raise ValueError(f"target_h must be a non-empty 1-D array, got shape {target_h.shape}")
    if "level" not in xs.dims:
        raise ValueError("the cross-section has no 'level' dimension")

    if names is None:
        names = [n for n in xs.data_vars if "level" in xs[n].dims and n != z]
    else:
        names = [names] if isinstance(names, str) else list(names)
    if not names:
        raise ValueError("no variable to interpolate")

    zda = _get_variable(xs, z)
    for name in [z, *names]:
        dims = _get_variable(xs, name).dims
        if dims != ("level", "distance"):
            raise ValueError(f"variable '{name}' must have the dimensions ('level', 'distance'), got {dims}")

    # the numpy implementation of earthkit-meteo is used, with the level as first axis
    zvalues = zda.values
    data_vars = {}
    for name in names:
        values = vertical.interpolate_pressure_to_height_levels(
            xs[name].values,
            target_h,
            zvalues,
            h_type="geometric",
            h_reference="sea",
            interpolation="linear",
            vertical_dim=0,
        )
        attrs = {k: v for k, v in xs[name].attrs.items() if k != "level_type"}
        data_vars[name] = (("height", "distance"), values, attrs)

    coords = {k: c for k, c in xs.coords.items() if "level" not in c.dims and k != "level"}
    res = xr.Dataset(data_vars, coords=coords, attrs=dict(xs.attrs))
    res = res.assign_coords(height=("height", target_h, _HEIGHT_COORD_ATTRS))
    res = res.transpose("height", "distance", ...)

    if zs is not None:
        if zs.dims != ("distance",) or zs.sizes["distance"] != xs.sizes["distance"]:
            raise ValueError(f"zs must be on the dimension 'distance' of the cross-section, got {zs.dims}")
        orog = orography(zs)
        res["orography"] = ("distance", orog.values, orog.attrs)
    return res


# CF attributes of the results of the model-level helpers
_SURFACE_PRESSURE_ATTRS = {"standard_name": "surface_air_pressure", "long_name": "surface pressure", "units": "Pa"}
_PRESSURE_ATTRS = {"standard_name": "air_pressure", "long_name": "pressure", "units": "Pa"}
_PRESSURE_COORD_ATTRS = {
    "standard_name": "air_pressure",
    "long_name": "pressure",
    "units": "hPa",
    "positive": "down",
    "axis": "Z",
}


def hybrid_coefficients(data):
    """Return the hybrid level coefficients (A, B) of the model levels of the data.

    The coefficients are read from the GRIB key ``metadata.pv`` of the first field.
    They are always those of the **full** column of the model (e.g. 138 values of A
    and B for 137 levels), even when the data has only some of the levels.

    Parameters
    ----------
    data: earthkit.data.FieldList, earthkit.data.Field, xarray.Dataset or xarray.DataArray
        A fieldlist (or field) with model-level fields, or xarray data created from
        such a fieldlist with ``to_xarray()``. The result of :func:`cross_section`
        cannot be used because it does not keep the GRIB metadata: call this
        function on the input of :func:`cross_section`.

    Returns
    -------
    tuple of numpy.ndarray
        The coefficients ``A`` (Pa) and ``B`` (dimensionless) of the half levels,
        both with ``n + 1`` values for a model with ``n`` levels.

    Raises
    ------
    ValueError
        If the coefficients cannot be found, e.g. when the data is the result of
        :func:`cross_section` or the fields are not on model levels.
    TypeError
        If ``data`` is not a fieldlist, a field or xarray data.
    """
    if isinstance(data, xr.Dataset):
        das = [da for da in data.data_vars.values() if "_earthkit" in da.attrs]
        if not das:
            raise ValueError(
                "cannot find the hybrid level coefficients: the dataset does not keep the GRIB metadata "
                "(use the data returned by to_xarray() or the fieldlist, not the result of cross_section())"
            )
        data = das[0]
    if isinstance(data, xr.DataArray):
        if "_earthkit" not in data.attrs:
            raise ValueError(
                "cannot find the hybrid level coefficients: the data does not keep the GRIB metadata "
                "(use the data returned by to_xarray() or the fieldlist, not the result of cross_section())"
            )
        field = data.earthkit.reference_field
    elif hasattr(data, "to_xarray") and hasattr(data, "__len__"):  # fieldlist
        if len(data) == 0:
            raise ValueError("cannot find the hybrid level coefficients: the fieldlist is empty")
        field = data[0]
    elif hasattr(data, "get"):  # field
        field = data
    else:
        raise TypeError(f"data must be a fieldlist, a field or xarray data, got {type(data)}")

    pv = field.get("metadata.pv")
    pv = np.asarray([] if pv is None else pv, dtype=float)
    if pv.size == 0 or pv.size % 2:
        raise ValueError("cannot find the hybrid level coefficients: the field has no valid 'pv' array")
    n = pv.size // 2
    return pv[:n].copy(), pv[n:].copy()


def _half_levels(xs, A, B):
    """Return the coefficients of the half levels enclosing the full model levels of ``xs``."""
    if "level" not in xs.dims:
        raise ValueError("the cross-section has no 'level' dimension")
    levels = xs["level"].values
    if (
        levels.ndim != 1
        or levels.size == 0
        or not np.array_equal(levels, np.arange(levels[0], levels[0] + levels.size))
    ):
        raise ValueError(f"the model levels must be ascending and contiguous (e.g. 60..137), got {levels.tolist()}")
    first, last = int(levels[0]), int(levels[-1])
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    if A.ndim != 1 or A.shape != B.shape:
        raise ValueError(f"A and B must be 1-D arrays of the same length, got shapes {A.shape} and {B.shape}")
    if first < 1 or A.size < last + 1:
        raise ValueError(f"A and B (length {A.size}) do not cover the half levels of the model levels {first}..{last}")
    return A[first - 1 : last + 1], B[first - 1 : last + 1]


def _check_reaches_surface(xs, A):
    """Raise if the model levels of ``xs`` do not include the lowest model level (the one at the surface)."""
    last = int(xs["level"].values[-1])
    n_full = np.asarray(A).size - 1
    if last != n_full:
        raise ValueError(
            f"the heights need the whole column down to the lowest model level ({n_full}), "
            f"but the model levels end at {last}"
        )


def _check_on_distance(xs, name, da, dims):
    if da.dims != dims or da.sizes["distance"] != xs.sizes["distance"]:
        raise ValueError(f"variable '{name}' must have the dimensions {dims} of the cross-section, got {da.dims}")


def _on_model_levels(xs, values, name, attrs):
    coords = {k: c for k, c in xs.coords.items() if set(c.dims) <= {"level", "distance"}}
    return xr.DataArray(values, dims=("level", "distance"), coords=coords, name=name, attrs=dict(attrs))


def surface_pressure(xs, lnsp="lnsp"):
    """Return the surface pressure (Pa) from its logarithm.

    Parameters
    ----------
    xs: xarray.Dataset
        Cross-section as returned by :func:`cross_section`, with the logarithm of the
        surface pressure on ``distance``.
    lnsp: str, optional
        Name of the logarithm of the surface pressure in ``xs``.

    Returns
    -------
    xarray.DataArray
        ``exp(lnsp)`` named ``sp`` on ``distance``, with the coordinates of ``lnsp``
        and the attributes ``standard_name="surface_air_pressure"``,
        ``long_name="surface pressure"`` and ``units="Pa"``. ``xs`` is not modified.

    Raises
    ------
    ValueError
        If ``lnsp`` is missing or is not on ``distance`` only.
    """
    da = _get_variable(xs, lnsp)
    if da.dims != ("distance",):
        raise ValueError(f"variable '{lnsp}' must have the dimension ('distance',), got {da.dims}")
    res = np.exp(da)
    res.attrs = dict(_SURFACE_PRESSURE_ATTRS)
    return res.rename("sp")


def pressure_on_model_levels(xs, A, B, sp):
    """Return the pressure (Pa) on the model levels of a cross-section.

    Uses :func:`earthkit.meteo.vertical.pressure_on_hybrid_levels` (numpy). The
    model levels of ``xs`` can be a part of the model column (e.g. 60..137 of 137):
    the half levels needed are taken from ``A`` and ``B`` according to ``xs.level``.

    Parameters
    ----------
    xs: xarray.Dataset
        Cross-section as returned by :func:`cross_section`, with ``level`` the model
        level numbers, ascending and contiguous, and ``distance``.
    A: array-like
        Coefficient A (Pa) of all the half levels of the model, as returned by
        :func:`hybrid_coefficients`.
    B: array-like
        Coefficient B of all the half levels of the model.
    sp: xarray.DataArray
        Surface pressure (Pa) on ``distance``, see :func:`surface_pressure`.

    Returns
    -------
    xarray.DataArray
        Pressure in Pa, named ``p``, on (``level``, ``distance``), with the
        coordinates of ``xs`` and the attributes ``standard_name="air_pressure"``,
        ``long_name="pressure"`` and ``units="Pa"``. The inputs are not modified.

    Raises
    ------
    ValueError
        If ``xs`` has no ``level`` dimension, the levels are not ascending and
        contiguous, ``A`` and ``B`` do not cover them, or ``sp`` is not on
        ``distance`` only.
    """
    Ah, Bh = _half_levels(xs, A, B)
    _check_on_distance(xs, "sp", sp, ("distance",))
    values = vertical.pressure_on_hybrid_levels(sp.values, Ah, Bh, output="full")
    return _on_model_levels(xs, values, "p", _PRESSURE_ATTRS)


def height_on_model_levels(xs, A, B, sp, zs, *, t="t", q="q"):
    """Return the geometric height (m above sea level) on the model levels of a cross-section.

    Uses :func:`earthkit.meteo.vertical.height_on_hybrid_levels` (numpy) with the
    temperature and the specific humidity of ``xs``. See
    :func:`pressure_on_model_levels` for the model levels.

    The heights are integrated upwards from the ground, so the model levels of ``xs``
    must reach the surface: they can be a part of the column (e.g. 60..137 of 137)
    only if the last one is the lowest model level, ``len(A) - 1``. A column that
    stops higher (e.g. 60..100) is rejected, as the heights would be wrong.

    Parameters
    ----------
    xs: xarray.Dataset
        Cross-section as returned by :func:`cross_section`, with ``level`` the model
        level numbers, ascending and contiguous, ending at the lowest model level,
        and ``distance``. The temperature and the specific humidity must be on
        exactly (``level``, ``distance``).
    A: array-like
        Coefficient A (Pa) of all the half levels of the model.
    B: array-like
        Coefficient B of all the half levels of the model.
    sp: xarray.DataArray
        Surface pressure (Pa) on ``distance``, see :func:`surface_pressure`.
    zs: xarray.DataArray
        Surface geopotential (m2 s-2) on ``distance``, from a separate
        :func:`cross_section` call (it is usually at a different step).
    t: str, optional
        Name of the temperature in ``xs``.
    q: str, optional
        Name of the specific humidity in ``xs``.

    Returns
    -------
    xarray.DataArray
        Height in m, named ``h``, on (``level``, ``distance``), with the coordinates
        of ``xs`` and the attributes ``standard_name="altitude"``,
        ``long_name="geometric height"`` and ``units="m"``. The inputs are not
        modified.

    Raises
    ------
    ValueError
        If the levels or ``A`` and ``B`` are not valid (see
        :func:`pressure_on_model_levels`), the levels do not end at the lowest model
        level, ``t`` or ``q`` is missing or is not on (``level``, ``distance``), or
        ``sp`` or ``zs`` are not on ``distance`` only.
    """
    Ah, Bh = _half_levels(xs, A, B)
    _check_reaches_surface(xs, A)
    _check_on_distance(xs, "sp", sp, ("distance",))
    _check_on_distance(xs, "zs", zs, ("distance",))
    for name in (t, q):
        _check_on_distance(xs, name, _get_variable(xs, name), ("level", "distance"))
    values = vertical.height_on_hybrid_levels(
        xs[t].values, xs[q].values, zs.values, sp.values, Ah, Bh, h_type="geometric", h_reference="sea"
    )
    return _on_model_levels(xs, values, "h", _HEIGHT_ATTRS)


def _model_level_names(xs, names):
    """Return the names of the variables to interpolate and check their dimensions."""
    if names is None:
        names = [n for n in xs.data_vars if "level" in xs[n].dims and n != "lnsp"]
    else:
        names = [names] if isinstance(names, str) else list(names)
    if not names:
        raise ValueError("no variable to interpolate")
    for name in names:
        _check_on_distance(xs, name, _get_variable(xs, name), ("level", "distance"))
    return names


def _on_new_levels(xs, data_vars, dim, values, attrs):
    coords = {k: c for k, c in xs.coords.items() if "level" not in c.dims and k != "level"}
    res = xr.Dataset(data_vars, coords=coords, attrs=dict(xs.attrs))
    res = res.assign_coords({dim: (dim, values, attrs)})
    return res.transpose(dim, "distance", ...)


def model_to_pressure(xs, A, B, sp, target_hpa, *, names=None):
    """Interpolate the variables of a model-level cross-section to pressure levels.

    The interpolation is linear in the pressure (not in its logarithm), with
    :func:`earthkit.meteo.vertical.interpolate_hybrid_to_pressure_levels`. Values
    below the ground and below the lowest model level are NaN.

    Parameters
    ----------
    xs: xarray.Dataset
        Cross-section as returned by :func:`cross_section`, with ``level`` the model
        level numbers, ascending and contiguous (e.g. 60..137), and ``distance``. The
        variables to interpolate must have exactly the dimensions (``level``,
        ``distance``).
    A: array-like
        Coefficient A (Pa) of all the half levels of the model, see
        :func:`hybrid_coefficients`.
    B: array-like
        Coefficient B of all the half levels of the model.
    sp: xarray.DataArray
        Surface pressure (Pa) on ``distance``, see :func:`surface_pressure`.
    target_hpa: array-like
        1-D pressures (hPa) to interpolate to.
    names: list of str, optional
        Variables to interpolate. By default all the variables with a ``level``
        dimension except ``lnsp``.

    Returns
    -------
    xarray.Dataset
        The interpolated variables (in their original units and with their
        attributes, except ``level_type``) on (``pressure``, ``distance``). The
        coordinates ``distance``, ``latitude``, ``longitude`` and the time
        coordinates of ``xs`` are kept. The ``pressure`` coordinate (hPa) has the
        attributes ``standard_name="air_pressure"``, ``units="hPa"``,
        ``positive="down"`` and ``axis="Z"``. ``xs`` is not modified.

    Raises
    ------
    ValueError
        If the levels or ``A`` and ``B`` are not valid (see
        :func:`pressure_on_model_levels`), a variable is missing or does not have
        exactly the dimensions (``level``, ``distance``), ``sp`` is not on
        ``distance`` only or ``target_hpa`` is not a non-empty 1-D array.
    """
    target_hpa = np.asarray(target_hpa)
    if target_hpa.ndim != 1 or target_hpa.size == 0:
        raise ValueError(f"target_hpa must be a non-empty 1-D array, got shape {target_hpa.shape}")
    Ah, Bh = _half_levels(xs, A, B)
    _check_on_distance(xs, "sp", sp, ("distance",))
    names = _model_level_names(xs, names)

    data_vars = {}
    for name in names:
        values = vertical.interpolate_hybrid_to_pressure_levels(
            xs[name].values,
            target_hpa * 100.0,
            sp.values,
            Ah,
            Bh,
            interpolation="linear",
            vertical_dim=0,
        )
        attrs = {k: v for k, v in xs[name].attrs.items() if k != "level_type"}
        data_vars[name] = (("pressure", "distance"), values, attrs)
    return _on_new_levels(xs, data_vars, "pressure", target_hpa, _PRESSURE_COORD_ATTRS)


def model_to_height(xs, A, B, sp, zs, target_h, *, names=None, t="t", q="q"):
    """Interpolate the variables of a model-level cross-section to height levels.

    The height of the model levels is the geometric height above sea level (see
    :func:`height_on_model_levels`). The interpolation is linear in height, with
    :func:`earthkit.meteo.vertical.interpolate_hybrid_to_height_levels`. Between the
    lowest model level and the ground the values of the lowest model level are used
    (as in the raw notebooks); heights below the orography, and above the highest
    model level, are NaN.

    The heights are integrated upwards from the ground, so the model levels of ``xs``
    must reach the surface: they can be a part of the column (e.g. 60..137 of 137)
    only if the last one is the lowest model level, ``len(A) - 1``. A column that
    stops higher (e.g. 60..100) is rejected, as the heights would be wrong.

    Parameters
    ----------
    xs: xarray.Dataset
        Cross-section as returned by :func:`cross_section`, with ``level`` the model
        level numbers, ascending and contiguous (e.g. 60..137), ending at the lowest
        model level, and ``distance``. The variables to interpolate, the temperature
        and the specific humidity must have exactly the dimensions (``level``,
        ``distance``).
    A: array-like
        Coefficient A (Pa) of all the half levels of the model, see
        :func:`hybrid_coefficients`.
    B: array-like
        Coefficient B of all the half levels of the model.
    sp: xarray.DataArray
        Surface pressure (Pa) on ``distance``, see :func:`surface_pressure`.
    zs: xarray.DataArray
        Surface geopotential (m2 s-2) on ``distance``, from a separate
        :func:`cross_section` call (it is usually at a different step).
    target_h: array-like
        1-D heights (m above sea level) to interpolate to.
    names: list of str, optional
        Variables to interpolate. By default all the variables with a ``level``
        dimension except ``lnsp`` (so including the temperature and the specific
        humidity).
    t: str, optional
        Name of the temperature in ``xs``.
    q: str, optional
        Name of the specific humidity in ``xs``.

    Returns
    -------
    xarray.Dataset
        The interpolated variables (in their original units and with their
        attributes, except ``level_type``) on (``height``, ``distance``), plus
        ``orography`` on ``distance`` (see :func:`orography`). The coordinates
        ``distance``, ``latitude``, ``longitude`` and the time coordinates of ``xs``
        are kept. The ``height`` coordinate has the attributes
        ``standard_name="altitude"``, ``long_name="height above sea level"``,
        ``units="m"``, ``positive="up"`` and ``axis="Z"``. ``xs`` is not modified.

    Raises
    ------
    ValueError
        If the levels or ``A`` and ``B`` are not valid (see
        :func:`pressure_on_model_levels`), the levels do not end at the lowest model
        level, a variable (including ``t`` and ``q``) is missing or does not have
        exactly the dimensions (``level``, ``distance``), ``sp`` or ``zs`` are not on
        ``distance`` only, or ``target_h`` is not a non-empty 1-D array.
    """
    target_h = np.asarray(target_h)
    if target_h.ndim != 1 or target_h.size == 0:
        raise ValueError(f"target_h must be a non-empty 1-D array, got shape {target_h.shape}")
    Ah, Bh = _half_levels(xs, A, B)
    _check_reaches_surface(xs, A)
    _check_on_distance(xs, "sp", sp, ("distance",))
    _check_on_distance(xs, "zs", zs, ("distance",))
    for name in (t, q):
        _check_on_distance(xs, name, _get_variable(xs, name), ("level", "distance"))
    names = _model_level_names(xs, names)

    orog = orography(zs)
    data_vars = {}
    for name in names:
        x = xs[name].values
        values = vertical.interpolate_hybrid_to_height_levels(
            x,
            target_h,
            xs[t].values,
            xs[q].values,
            zs.values,
            sp.values,
            Ah,
            Bh,
            h_type="geometric",
            h_reference="sea",
            interpolation="linear",
            aux_bottom_data=x[-1],
            aux_bottom_h=orog.values,
            vertical_dim=0,
        )
        attrs = {k: v for k, v in xs[name].attrs.items() if k != "level_type"}
        data_vars[name] = (("height", "distance"), values, attrs)

    res = _on_new_levels(xs, data_vars, "height", target_h, _HEIGHT_COORD_ATTRS)
    res["orography"] = ("distance", orog.values, orog.attrs)
    return res
