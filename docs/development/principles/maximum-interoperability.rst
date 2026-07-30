Maximum Interoperability
========================

earthkit is not an attempt to reinvent the wheel and retaining interoperability is a key goal. This means both interoperability between earthkit packages, and interoperability with the rest of the Python ecosystem.

1. Interoperability with the Python ecosystem
---------------------------------------------

earthkit aims to integrate naturally with the wider Scientific Python ecosystem. The primary supported data types are:

- xarray
- Array API-compatible arrays (e.g. NumPy, CuPy, PyTorch)
- pandas
- earthkit-data objects

The public function should contain only dispatch logic. Each backend should
implement the same function with the same signature and semantics.

A minimal made-up example implementing MSE as a function earthkit.foo.bar with xarray and array implementations::

    # earthkit.foo

    from earthkit.utils.dispatch import dispatch

    def bar(a, b):
        """
        Doc for toplevel implementation.
        Links to backend implementations.
        """
        dispatched_function = dispatch(bar, fieldlist=False)
        return dispatched_function(a, b)

The backend implementations live in the corresponding submodules::

    # earthkit.foo.array

    from earthkit.utils.array import array_namespace

    def bar(a, b):
        """
        Doc for array implementation.
        """
        xp = array_namespace(a, b)
        # array-api compat logic
        return xp.vector_norm((a-b), ord=2)



    # earthkit.foo.xarray

    def bar(a, b):
        """
        Doc for xarray implementation.
        """
        # xarray logic
        return ((a-b)**2).mean(skipna=False)

This structure keeps the public API independent of the supported input types,
avoids unnecessary data conversion, and makes it straightforward to add support
for additional backends.

.. important::

    Dispatching and array-api compat both rely on being able to detect the desired backend from inputs. This is not always possible. Numpy is preferred when array-api compat is infeasible, and xarray is preferred for the toplevel function when dispatching is infeasible.

2. Interoperability between earthkit packages
---------------------------------------------

earthkit should work seamlessly as an ecosystem and therefore packages should be easily interoperable between each other by supporting the same data formats, APIs, naming etc. as much as possible.
