import sys,os

sys.path.append(os.path.abspath('../../dev'))

project = 'Horaire_refonte_2024'
copyright = '2024, jk'
author = 'jk'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

autodoc_mock_imports = ["xlsxwriter"]

extensions = ['sphinx.ext.autodoc',
'sphinx.ext.autosummary',
'sphinx.ext.napoleon',
'sphinx.ext.viewcode',
'sphinxcontrib.plantuml',
'sphinx.ext.graphviz',
'sphinx.ext.todo',
'sphinx_rtd_theme',
'sphinx.ext.intersphinx',
'sphinx_design',
]
#plantuml = ['java', '-jar', 'C:\\UML_tools\\plantuml.jar']
plantuml = ['java', '-jar', '/usr/share/umltools/plantuml.jar']

todo_include_todos = True

templates_path = ['_templates']

exclude_patterns = []

language = 'FR'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"

html_static_path = []
