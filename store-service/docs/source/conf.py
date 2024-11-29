# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GameHub'
copyright = '2024, Gubanov, Khrol, Potapova'
author = 'Gubanov, Khrol, Potapova'
release = '1.0'

import os
import sys

sys.path.insert(0, os.path.abspath('../../database'))
sys.path.insert(0, os.path.abspath('../../routes'))
sys.path.insert(0, os.path.abspath('../../templates'))
sys.path.insert(0, os.path.abspath('../../utility'))
sys.path.insert(0, os.path.abspath('../../utility/Game.py'))
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../../bank-service'))


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
              'sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'autodocsumm'
              ]

templates_path = ['_templates']
exclude_patterns = []




# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

latex_documents = [
 ('index', 'yourdoc.tex', u'DocName', u'YourName', 'manual'),
]
