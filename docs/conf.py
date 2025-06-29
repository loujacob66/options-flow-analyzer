# Configuration file for Sphinx documentation builder
import os
import sys

# Add the parent directory to Python path for autodoc
sys.path.insert(0, os.path.abspath(".."))

project = "Options Flow Analyzer"
copyright = "2024, Options Flow Analyzer Team"
author = "Options Flow Analyzer Team"

# The full version, including alpha/beta/rc tags
release = "0.1.0"

# Add any Sphinx extension module names here
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# Mock imports for modules that might not be available
autodoc_mock_imports = []

# Add any paths that contain templates here
templates_path = ["_templates"]

# List of patterns to exclude when looking for source files
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The theme to use for HTML and HTML Help pages
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files here
html_static_path = ["_static"]
