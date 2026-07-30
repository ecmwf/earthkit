Documentation Guidelines
========================

earthkit uses the Diátaxis framework, which organises documentation into four complementary types:

- Tutorials — learning-oriented, step-by-step examples for newcomers.
- How-to Guides — short recipes that solve a specific problem.
- Concepts — conceptual background and rationale.
- API Reference — factual API documentation and exhaustively-listed behaviour.

In addition to these standard Diátaxis types, earthkit also two additional sections in the User Guide.

- Installation and Getting Started - a quick way to get up and running.
- Frequently Asked Questions - common questions with short answers

Where to place content
----------------------

- Frequently Asked Questions: only for questions that often come up and have short answers (1-5 lines). If the answer is longer, it should be written elsewhere and linked to from the Frequently Asked Questions.

- Tutorials: put hands-on, example-driven content.
  Preface with a clear goal, required inputs, and a short worked example.

- How-to Guides: add focused recipes`. Keep them
  concise and task-oriented; show the recipe first, then explain options.

- Concepts: add design rationale and conceptual material. These pages are for readers who want
  "why" and "how it works" rather than "what to click".

- API Reference: API docs should be
  generated from docstrings as much as possible. Keep docstrings authoritative and minimal
  narrative in the reference pages.

Writing tips
------------

- Title your pages for intent (e.g. "Delineating catchments", not "Notes").
- Start tutorials with "What you will learn" and a short, copy-pastable
  example that runs quickly.
- For how-to guides, lead with the exact commands or code that solves the
  task; follow with explanation of options and common pitfalls.
- Use short paragraphs and clear headings; aim for a single idea per
  paragraph.
- Prefer concrete examples over abstract descriptions in tutorials and
  how-tos. Put conceptual material in Concepts pages.

Writing examples
----------------

- Tutorial (first lines):

  "This tutorial shows how to load a precomputed EFAS river network and
  compute catchment areas. By the end you'll have a CSV of catchment stats."

- How-to (first lines):

  "How to compute upstream accumulation for a field of ones to get upstream
  cell counts. Code:

  .. code-block:: python

     import numpy as np
     import earthkit.hydro as ekh

     network = ekh.river_network.load('efas', '5')
     counts = ekh.upstream.sum(network, np.ones(network.n_nodes))"

- Concepts (first lines):

  "Distance vs length: distances are edge costs; lengths are node extents.
  This difference matters at confluences where multiple edges meet a node."

Keeping documentation high quality
----------------------------------

- Link to a single canonical location for each topic. Avoid duplicate
  content across pages.
- When adding API examples, keep them small and runnable and prefer
  example snippets that do not require external datasets.
- Submit documentation changes via pull requests and include a short
  description that states what changed and why.

For more detail, read the Diátaxis guide: https://diataxis.fr/

Notebooks
---------

Ensure the title and the subchapter headings have the same size as in the other notebooks and are recognised and navigable in the documentation.
