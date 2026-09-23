Dependencies
============

earthkit aims to be interoperable with a wide range of Python libraries.
This means that adding hard dependencies for every supported data type will lead to a growing list of dependencies, despite the fact that most users will have no need for most of them.


Each component should therefore keep its core dependencies to a minimum, depending only on libraries that are fundamental to its own functionality.
In particular, NumPy should be considered a core dependency, while other third-party libraries should be added to a component's default dependency set only when they are required by its core functionality.
Support for specific data formats, libraries, or integrations should generally be provided through optional dependencies.

At the top-level earthkit package, however, we should favour a convenient out-of-the-box experience and include dependencies needed to support the most common use cases.
Thus, while individual components should minimise their default dependencies, the top-level package may aggregate a broader set of optional functionality so that most users can install earthkit and have support for common use cases without installing additional dependencies.
