Naming conventions
==================

Consistent naming is important for making earthkit APIs predictable and
easy to discover. Names should follow these principles:

* Use British English spelling.
* Prefer descriptive names that clearly communicate the purpose of a function,
  class, or module. Variables or function arguments can be shorted.
* Follow existing earthkit naming conventions rather than introducing new
  patterns. If a convention is problematic, suggest changing it.
* Use terminology that is consistent with the wider scientific Python
  ecosystem where appropriate/possible e.g. earthkit-plots follows closely
  matplotlib conventions.

Function names should favour clarity over brevity. Avoid abbreviations unless they are
well established and unambiguous.

Function arguments on the other hand can be shorter.

Before introducing a new name, check existing ``earthkit`` APIs and related
packages for similar concepts. Similar operations should use the same names
across modules.

earthkit vs Earthkit
--------------------

In general, earthkit is lower caps when mentioning the repositories and software packages.
It is capitalised when mentioning the project.
