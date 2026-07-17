# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "🧙 Spondan"
copyright = '2026, Spondan Bandyopadhyay'
author = 'Spondan Bandyopadhyay'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.mathjax", # This is the math renderer
]

myst_enable_extensions = [
    "colon_fence",    # This allows the ::: syntax
    "dollarmath",      # <--- REQUIRED for $ and $$ to work
    "smartquotes",
    "replacements",
]

html_theme_options = {
    "nav_links": [
        {"title": "Projects", "url": "projects/index",
        "children":[
            {"title": "🧬 Genetic Algorithm", "url": "projects/genetic-algorithm"},
            {"title": "🎮 Gesture Flappy Bird", "url": "projects/gesture-flappy-bird"},
            {"title": "📐 PCA Study",           "url": "projects/pca-study"},
            {"title": "More...",           "url": "projects/index"},
        ]
        },
        {"title": "About",    "url": "about"},
    ],
    "github_url": "https://github.com/SpondanB",
    "linkedin_url": "https://www.linkedin.com/in/spondan-bandyopadhyay/",

    # "globaltoc_expand_depth": 1,
    "navigation_with_keys": False,
    # "globaltoc_collapse": True,
}

templates_path = ['_templates']
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'shibuya'
html_static_path = ['_static']
html_title = "Spondan"
html_favicon = "_static/imgs/magician.svg"


# html_show_copyright = False
html_css_files = [
    'css/custom.css',
    'css/timeline.css'
]
