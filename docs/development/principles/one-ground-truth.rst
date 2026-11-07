One Ground Truth
================

Where earthkit supports several data types for the same operation, that operation should
have a single canonical implementation. The other interfaces — xarray, FieldList, pandas
— are thin wrappers around it, not re-implementations of the same algorithm. This
complements :doc:`maximum-interoperability`: the maths should only be written once, or
the copies drift apart until their results diverge.

Choosing the ground truth
-------------------------

Implement at the lowest natural level so the other interfaces derive from it. For most
numerical operations this is the array implementation, written against the Array API (via
``earthkit.utils.array.array_namespace``) so it covers NumPy, CuPy and PyTorch. Where an
operation only makes sense with labelled dimensions, xarray is a more natural ground
truth and the others wrap that instead.

Wrapping outwards
-----------------

``earthkit-utils`` provides the wrappers, so this glue rarely needs writing by hand::

    from earthkit.utils.decorators import xarray_ufunc, fieldlist_ufunc

``xarray_ufunc`` runs the array function through ``xarray.apply_ufunc`` for the xarray
interface; ``fieldlist_ufunc`` applies it to ``Field``/``FieldList`` values and
reattaches metadata. Dispatch (see :doc:`maximum-interoperability`) routes each caller to
the right wrapper.

A separate backend implementation is warranted only when a backend needs genuinely
different logic, not merely a different container.
