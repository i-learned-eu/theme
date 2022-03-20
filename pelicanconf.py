#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from blinker import signal
AUTHOR = 'I Learned'
SITENAME = 'I Learned'
SITEURL = 'https://ilearned.eu'

PATH = 'content/'
ARTICLE_SAVE_AS = '{slug}.html'
ARTICLE_URL = '{slug}.html'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'
LOCALE = 'fr_FR.UTF-8'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_RSS = 'rss.xml'
RSS_FEED_SUMMARY_ONLY = False

DEFAULT_PAGINATION = 100000000

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

DISPLAY_CATEGORIES_ON_MENU = True
OUTPUT_SOURCES = False
SUMMARY_MAX_LENGTH = 50
THEME = 'theme/'
THEME_STATIC_PATHS = ['static']
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['sitemap', 'neighbors', 'minify', 'readtime',
           'i18n_subsites', 'tipue_search', 'pelican_katex']
STATIC_PATHS = ['content-fr/static/', 'content-en/static/']

DIRECT_TEMPLATES = ['index', 'archives', 'authors', 'search']

TIPUE_SEARCH = True

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

tmpsig = signal('tmpsig')
I18N_FILTER_SIGNALS = [tmpsig]


I18N_SUBSITES = {
    'fr': {
        'SITEURL': 'https://ilearned.eu',
        'OUTPUT_PATH': 'output/'
    },
    'en': {
        'SITENAME': 'I Learned',
        'I18N_UNTRANSLATED_PAGES': 'remove',
        'I18N_UNTRANSLATED_ARTICLES': 'remove',
        'SITEURL': 'https://en.ilearned.eu',
        'OUTPUT_PATH': 'en/'
        }
    }

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
        "Mastodon": "https://toot.gnous.eu/@rml",
    },

    "Eban": {
        "Image": "/theme/img/authors/eban.webp",
        "Website": "https://eban.eu.org/",
        "Mastodon": "https://toot.gnous.eu/@eban",
        "Twitter": "https://twitter.com/eban_non",
        "Github": "https://github.com/ebanDev/",
    },

    "Lancelot": {
        "Image": "/theme/img/authors/lancelot.webp",
        "Website": "https://theredwindows.net/",
        "Twitter": "https://twitter.com/lancelot_ps1",
        "Github": "https://github.com/rootSySdk",
    },

    "MorpheusH3x": {
        "Image": "/theme/img/authors/morpheush3x.webp",
        "Twitter": "https://twitter.com/MorpheusH3x",
        "Github": "https://github.com/MorpheusH3x",
    },

    "Ownesis": {
        "Image": "/theme/img/authors/ownesis.webp",
        "Github": "https://github.com/ownesis",
    },

    "Immae": {
        "Image": "/theme/img/authors/immae.webp",
        "Website": "https://www.immae.eu/",
    },

    "Outout": {
        "Image": "/theme/img/authors/outout.webp",
        "Website": "https://enpls.org",
        "Twitter": "https://twitter.com/outoutxyz",
        "Github": "https://github.com/outout14",
    },

    "Rick": {
        "Image": "/theme/img/authors/rick.webp",
        "Twitter": "https://twitter.com/GnousRick",
        "Github": "https://git.gnous.eu/Rick",
        "Mastodon": "https://toot.gnous.eu/@rick",
    },

    "Akinimaginable": {
        "Image": "/theme/img/authors/akinimaginable.webp",
        "Twitter": "https://twitter.com/akinimaginable",
        "Github": "https://github.com/Akinimaginable",
    },
}
