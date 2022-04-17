# -*- coding: utf-8 -*- #

AUTHOR = 'I Learned'
SITENAME = 'I Learned Blog'
SITEURL = 'https://blog.ilearned.eu'

PATH = 'content'

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
PLUGINS = ['webassets', 'sitemap', 'readtime', 'pelican_katex', 'subcategory',
           'tipue_search', 'top_read', 'to_json']

CATEGORY_PRETTY_NAME = {"Cybersécurité": "🔒",
                        "Pensées du libre": "🔖", "Réseau": "📶", "Sysadmin": "🖥"}

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

CONTRIBUTORS_DATA = {
    "Ramle": {
        "Image": "/theme/img/authors/ramle.webp",
    },

    "Eban": {
        "Image": "/theme/img/authors/eban.webp",
    },

    "Lancelot": {
        "Image": "/theme/img/authors/lancelot.webp",
    },

    "MorpheusH3x": {
        "Image": "/theme/img/authors/morpheush3x.webp",
    },

    "Ownesis": {
        "Image": "/theme/img/authors/ownesis.webp",
    },

    "Immae": {
        "Image": "/theme/img/authors/immae.webp",
    },

    "Outout": {
        "Image": "/theme/img/authors/outout.webp",
    },

    "Rick": {
        "Image": "/theme/img/authors/rick.webp",
    },

    "Akinimaginable": {
        "Image": "/theme/img/authors/akinimaginable.webp",
    },
}
