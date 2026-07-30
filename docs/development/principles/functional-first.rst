Functional-first design
=======================

earthkit follows a functional-first design approach. Functionality should
primarily be expressed through functions operating on data, rather than through
object-oriented hierarchies with complex inheritance structures.

Prefer small, composable functions with clear inputs and outputs::

    result = earthkit.foo.bar(data, options)

over stateful objects that hide operations behind methods::

    result = data.bar(options)

Functions should:

* have explicit inputs and outputs
* avoid unnecessary mutable state
* be easy to compose with other functions
* work naturally with different supported data types

Object-oriented patterns may still be used where they provide a clear benefit,
for example for representing stateful resources, configuration, or complex
lifecycle management. However, new APIs should default to a functional design
unless there is a strong reason to introduce an object abstraction.

A functional design also supports interoperability by allowing the same
operation to be dispatched across different data backends while keeping the
public API consistent.
