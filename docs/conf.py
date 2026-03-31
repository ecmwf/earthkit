# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime
import json
import os
import sys

import yaml

on_rtd = os.environ.get("READTHEDOCS") == "True"

if on_rtd:
    version = os.environ.get("READTHEDOCS_VERSION", "latest")
    release = version
else:
    version = "dev"
    release = "dev"

rtd_version = version if version != "latest" else "develop"
rtd_version_type = os.environ.get("READTHEDOCS_VERSION_TYPE", "branch")

if rtd_version_type in ("branch", "tag"):
    source_branch = rtd_version
else:
    source_branch = "main"

src_path = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
)
sys.path.insert(0, src_path)

# Adds path to the folder _ext, where extensions are stored
sys.path.insert(0, os.path.abspath("."))
sys.path.append(os.path.abspath("./_ext"))

project = "earthkit"
module_prefix = project.replace("-", ".")
autodocs_dir = "autodocs"

copyright = f"{datetime.datetime.now().year}, European Centre for Medium-Range Weather Forecasts (ECMWF)"
author = "European Centre for Medium-Range Weather Forecasts (ECMWF)"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Automatically extracts documentation from your Python docstrings
    "sphinx.ext.autodoc",
    # Supports Google-style and NumPy-style docstrings
    "sphinx.ext.napoleon",
    # Renders LaTeX math in HTML using MathJax
    "sphinx.ext.mathjax",
    # Option to click viewcode
    "sphinx.ext.viewcode",
    # Links to the documentation of other projects via cross-references (see list below)
    "sphinx.ext.intersphinx",
    # Generates summary tables for modules/classes/functions
    "sphinx.ext.autosummary",
    # Allows citing BibTeX bibliographic entries in reStructuredText
    # "sphinxcontrib.bibtex",
    # Tests snippets in documentation by running embedded Python examples
    # "sphinx.ext.doctest",
    # Checks documentation coverage of the codebase
    # "sphinx.ext.coverage",
    # Adds .nojekyll file and helps configure docs for GitHub Pages hosting
    # "sphinx.ext.githubpages",
    # Adds "Edit on GitHub" links to documentation pages
    # "edit_on_github",
    # Adds "Edit on GitHub" links to documentation pages
    # "sphinx_github_style",
    # Option to link to code
    # "sphinx.ext.linkcode",
    # Automatically includes type hints from function signatures into the documentation
    # "sphinx_autodoc_typehints",
    # Integrates Jupyter Notebooks into Sphinx
    "nbsphinx",
    # Simplifies linking to external resources with short aliases
    "sphinx.ext.extlinks",
    # Enables responsive grid layouts and card components
    "sphinx_design",
    # Custom extension for external cross-references
    "xref",
]

autodoc_inherit_docstrings = True
autodoc_default_options = {
    "members": True,
    "imported-members": True,
    "undoc-members": False,
    "show-inheritance": True,
}

autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_imported_members = False

# GitHub links configuration
extlinks = {
    "pr": ("https://github.com/ecmwf/earthkit/pull/%s", "PR #%s"),
    "issue": ("https://github.com/ecmwf/earthkit/issues/%s", "Issue #%s"),
}

# intersphinx configuration, to automatically link to upstream documentation.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "xarray": ("https://docs.xarray.dev/en/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "cartopy": ("https://cartopy.readthedocs.io/stable/", None),
    "earthkit-data": ("https://earthkit-data.readthedocs.io/en/latest/", None),
    "earthkit-plots": ("https://earthkit-plots.readthedocs.io/en/latest/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Modules to hide from autodocs (relative to earthkit.transforms)
# These modules will not appear in the API documentation sidebar
# autodocs_hidden_modules = ["aggregate", "version"]

# clean_autodocs.py feature flags
# Set to False/None to disable or soften the corresponding processing step.
autodocs_delete_hidden = True  # delete RST files for private/hidden modules
autodocs_replace_automodule = (
    True  # replace automodule directives with autosummary tables
)
autodocs_short_display_names = (
    True  # shorten toctree labels to the last module component
)
autodocs_top_level_maxdepth = (
    1  # :maxdepth: on top-level page (None = keep sphinx-apidoc value)
)
autodocs_rename_titles = False  # strip " package"/" module" from RST page headings
autodocs_top_level_title = (
    "API Reference"  # top-level page heading (used when rename_titles=True)
)
autodocs_titlesonly = False  # inject :titlesonly: into toctree directives

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"

html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]

html_js_files = [
    "earthkit-packages.js",  # generated from earthkit-packages.yml at build time
    "custom.js",
]

html_favicon = "./_static/earthkit-notext.svg"

d_thing = (
    "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1."
    "49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 "
    "1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59."
    "82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 "
    "1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25"
    ".54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"
)

html_theme_options = {
    "light_css_variables": {
        "color-sidebar-background": "#131320",
        # "color-background-primary": "", # leave as default to avoid overriding the light theme background
        "color-sidebar-link-text": "#ffffff",
        "color-sidebar-brand-text": "#ffffff",
        "color-sidebar-caption-text": "#ffffff",
        "color-brand-primary": "#FCE54B",
        "color-brand-content": "#5f8dd3",
        "color-sidebar-item-background--hover": "#001F3F",
        "color-sidebar-item-expander-background--hover": "#001F3F",
    },
    "dark_css_variables": {
        "color-sidebar-background": "#131320",
        "color-background-primary": "#131320",
        "color-sidebar-link-text": "#ffffff",
        "color-sidebar-brand-text": "#ffffff",
        "color-sidebar-caption-text": "#ffffff",
        "color-brand-primary": "#FCE54B",
        "color-brand-content": "#5f8dd3",
        "color-sidebar-item-background--hover": "#001F3F",
        "color-sidebar-item-expander-background--hover": "#001F3F",
    },
    "light_logo": "earthkit-dark.svg",
    "dark_logo": "earthkit-dark.svg",
    "source_repository": "https://github.com/ecmwf/earthkit/",
    "source_branch": source_branch,
    "source_directory": "docs/source",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/ecmwf/earthkit",
            "html": f"""
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="{d_thing}"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}


def _write_earthkit_packages_js(app):
    """Read earthkit-packages.yml and write a JS data file into the output _static dir."""
    config_path = os.path.join(os.path.dirname(__file__), "earthkit-packages.yml")
    with open(config_path, encoding="utf-8") as fh:
        config = yaml.safe_load(fh)
    packages = config.get("packages", [])
    static_dir = os.path.join(app.outdir, "_static")
    os.makedirs(static_dir, exist_ok=True)
    js_path = os.path.join(static_dir, "earthkit-packages.js")
    with open(js_path, "w", encoding="utf-8") as fh:
        fh.write(f"window.earthkitPackages = {json.dumps(packages)};\n")


# xref links configuration
xref_links = {
    "earthkit-data": (
        "earthkit-data",
        "https://earthkit-data.readthedocs.io",
    ),
    "earthkit-geo": (
        "earthkit-geo",
        "https://earthkit-geo.readthedocs.io",
    ),
    "earthkit-hydro": (
        "earthkit-hydro",
        "https://earthkit-hydro.readthedocs.io",
    ),
    "earthkit-meteo": (
        "earthkit-meteo",
        "https://earthkit-meteo.readthedocs.io",
    ),
    "earthkit-plots": (
        "earthkit-plots",
        "https://earthkit-plots.readthedocs.io",
    ),
    "earthkit-regrid": (
        "earthkit-regrid",
        "https://earthkit-regrid.readthedocs.io",
    ),
    "earthkit-time": (
        "earthkit-time",
        "https://earthkit-time.readthedocs.io",
    ),
    "earthkit-transforms": (
        "earthkit-transforms",
        "https://earthkit-transforms.readthedocs.io",
    ),
    "earthkit-workflows": (
        "earthkit-workflows",
        "https://github.com/ecmwf/earthkit-workflows/blob/develop/readme.md",
    ),
    "eccodes": (
        "ecCodes",
        "https://confluence.ecmwf.int/display/ECC/ecCodes+Home",
    ),
}


def setup(app):
    app.connect("builder-inited", _write_earthkit_packages_js)
