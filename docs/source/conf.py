# Configuration file for the Sphinx documentation builder.
import os
import sys

# -- Project information -----------------------------------------------------
project = 'GameHub'
copyright = '2024, Gubanov, Khrol, Potapova'
author = 'Gubanov, Khrol, Potapova'
release = '1.0'

# -- Path setup --------------------------------------------------------------
# Добавляем все необходимые пути
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../store-service'))
sys.path.insert(0, os.path.abspath('../../bank-service'))
sys.path.insert(0, os.path.abspath('../../store-service/routes'))
sys.path.insert(0, os.path.abspath('../../store-service/app'))
sys.path.insert(0, os.path.abspath('../../store-service/utility'))
sys.path.insert(0, os.path.abspath('../../store-service/database'))
sys.path.insert(0, os.path.abspath('../../bank-service/routes'))
sys.path.insert(0, os.path.abspath('../../bank-service/database_bank'))


# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

# Мокаем только внешние зависимости
autodoc_mock_imports = [
    'flask',
    'psycopg2',
    'werkzeug',
    'jwt'
]

# Настройки autodoc
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Настройки шаблонов
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Язык документации
language = 'en'

# Дополнительные настройки
add_module_names = False
nitpicky = True

