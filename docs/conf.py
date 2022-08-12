# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# pylint: disable=invalid-name,redefined-builtin,wrong-import-position

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent.parent)

from autohooks.version import get_version

project = "autohooks"
copyright = "2018 - 2022, Greenbone Networks GmbH"
author = "Greenbone Networks GmbH"
release = get_version()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "myst_parser",
    "sphinx_tabs.tabs",
]

templates_path = ["_templates"]
exclude_patterns = [
    "build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    ".vscode",
    "dist",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

html_title = "Autohooks Documentation"

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "_static/logo.svg"
html_favicon = "favicon.png"

repo_url = "https://github.com/greenbone/autohooks/"
html_theme_options = {
    "source_repository": repo_url,
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-content-foreground": "#4C4C4C",
        "color-foreground-primary": "4C4C4C",
        "color-foreground-secondary": "#7F7F7F",
        "color-code-background": "#333333",
        "color-code-foreground": "#E5E5E5",
        "color-admonition-title--note": "#11AB51",
        "admonition-font-size": "0.9rem",
        "color-background-primary": "#FFFFFF",
        "color-background-secondary": "#F3F3F3",
        "color-sidebar-background": "#F3F3F3",
    },
    "dark_css_variables": {
        "color-content-foreground": "#F3F3F3",
        "color-foreground-primary": "F3F3F3",
        "color-foreground-secondary": "#E5E5E5",
        "color-code-background": "#333333",
        "color-code-foreground": "#E5E5E5",
        "color-admonition-title--note": "#11AB51",
        "admonition-font-size": "0.9rem",
        "color-background-primary": "#171717",
        "color-background-secondary": "#4C4C4C",
        "color-sidebar-background": "#333333",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": repo_url,
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

pygments_style = "zenburn"
pygments_dark_style = "monokai"

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

autodoc_class_signature = "separated"

myst_heading_anchors = 2
