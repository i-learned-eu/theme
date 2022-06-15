# -*- coding: utf-8 -*- #

AUTHOR = 'I Learned'
SITENAME = 'I Learned Blog'
SITEURL = 'https://blog.ilearned.eu'

PATH = 'content/fr/'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'
LOCALE = 'fr_FR.UTF-8'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_RSS = 'rss.xml'
RSS_FEED_SUMMARY_ONLY = False
DEFAULT_PAGINATION = False

THEME = 'theme/'

GOACCESS_JSON_URI = 'https://analytics.ilearned.eu/blog-french.json'

STATIC_PATHS = ['static']
THEME_STATIC_PATHS = ['static']

DIRECT_TEMPLATES = ['index', 'latest', 'most_read', 'search']

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['webassets', 'sitemap', 'readtime', 'pelican_katex', 'subcategory', 'tipue_search', 'top_read', 'to_json', 'add_class']

CATEGORY_PRETTY_NAME = {"Cybersécurité": "🔒",
                        "Pensées du libre": "🔖", "Réseau": "📶", "Sysadmin": "🖥", "Sciences": "🔬"}

DEFAULT_DATE_FORMAT = '%d %B %y'


SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.5,
        "indexes": 0.5,
        "pages": 0.5
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly"
    }
}

MARKDOWN = {
    "extensions": [
        "markdown.extensions.codehilite",
        "markdown.extensions.extra",
        "markdown.extensions.meta",
        "markdown.extensions.admonition",
    ],
    "extension_configs": {
        "markdown.extensions.codehilite": {
            "css_class": "highlight"
        },
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.admonition": {},
    },
    "output_format": "html5",
    'markdown.extensions.admonition': {},
}
