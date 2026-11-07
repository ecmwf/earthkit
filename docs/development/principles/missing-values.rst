Missing Value Handling
======================

The default policy for missing values should be to propagate i.e. not to omit.
Note in particular that this is the opposite of xarray conventions.
If missing value handling needs to be configurable, it should follow scipy conventions.

    nan_policy: {‘propagate’, ‘omit’, ‘raise’}
    Defines how to handle input NaNs.
    * propagate: if a NaN is present in the axis slice (e.g. row) along which the statistic is computed, the corresponding entry of the output will be NaN.
    * omit: NaNs will be omitted when performing the calculation. If insufficient data remains in the axis slice along which the statistic is computed, the corresponding entry of the output will be NaN.
    * raise: if a NaN is present, a ValueError will be raised.

In complex multidimensional-data cases, it may be unclear to what axes propagation/omission etc. should apply to. Such cases warrant wider discussion.
