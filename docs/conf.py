# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Import and path setup ---------------------------------------------------

import datetime
import os
import sys

# Adds path to the folder _ext, where extensions are stored
sys.path.insert(0, os.path.abspath("."))
sys.path.append(os.path.abspath("./_ext"))

# -- Project information -----------------------------------------------------

project = "earthkit"
author = "European Centre for Medium Range Weather Forecasts"

year = datetime.datetime.now().year
years = "2022-%s" % (year,)
copyright = "%s, European Centre for Medium-Range Weather Forecasts (ECMWF)" % (years,)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "nbsphinx",
    "xref",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The suffix of source filenames.
source_suffix = ".rst"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["style.css"]

# html_logo = "https://github.com/ecmwf/logos/raw/refs/heads/main/logos/earthkit/earthkit-light.svg"


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
    # "source_branch": source_branch,
    "source_directory": "docs/source",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/ecmwf/earthkit",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}


xref_links = {
    "earthkit-data": (
        "earthkit-data",
        "https://earthkit-data.readthedocs.io",
    ),
    "earthkit-geo": (
        "earthkit-geo",
        "https://earthkit-geo.readthedocs.io",
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
    "earthkit-hydro": (
        "earthkit-hydro",
        "https://earthkit-hydro.readthedocs.io",
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
