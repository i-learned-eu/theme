#!/usr/bin/env python
# -*- coding: utf-8 -*- #


AUTHOR = 'I Learned'
SITENAME = 'I Learned'
SITEURL = 'https://ilearned.eu'

PATH = 'content'
ARTICLE_SAVE_AS = '{slug}.html'
ARTICLE_URL = '{slug}.html'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'

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
PLUGINS = ['sitemap', 'post_stats', 'feed_summary', 'neighbors', 'minify', 'readtime', 'tipue_search', 'render_math', 'i18n_subsites']
STATIC_PATHS = ['static/']

DIRECT_TEMPLATES = ['index', 'archives', 'authors', 'search']

TIPUE_SEARCH = True

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

I18N_SUBSITES = {
    'en': {
        'SITENAME': 'I Learned',
	'OUTPUT_PATH': 'output-en',
        'I18N_UNTRANSLATED_PAGES': 'remove',
        'I18N_UNTRANSLATED_ARTICLES': 'keep'
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
        "markdown.extensions.toc",
        "markdown.extensions.smarty",
    ],
    "extension_configs": {
        "markdown.extensions.codehilite": {
            "css_class": "highlight"
        },
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {},
        "markdown.extensions.smarty": {},
    },
    "output_format": "html5",
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
}
