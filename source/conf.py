# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import django

project = 'Videoflix'
copyright = '2024, Jan Horstmann'
author = 'Jan Horstmann'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


sys.path.insert(0, os.path.abspath('../videoflix'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'videoflix.settings'

extensions = [
    'sphinx.ext.autodoc',           # Generiert Dokumentation aus Docstrings
    'sphinx.ext.viewcode',          # Fügt Links zum Quellcode hinzu
    'sphinx.ext.napoleon',          # Unterstützung für Google- und NumPy-Stil-Dokumentation
    'sphinx_autodoc_typehints',     # Typannotationen in der Dokumentation
]

autodoc_typehints = "description"


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

django.setup()