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
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['sitemap', 'post_stats', 'feed_summary', 'neighbors',
           'readtime', 'seo', 'tipue_search', 'render_math']
STATIC_PATHS = ['static/']

SEO_ENHANCER = True  # To disable this feature
SEO_ENHANCER_OPEN_GRAPH = True  # The default value for this feature
SEO_ENHANCER_TWITTER_CARDS = True  # The default value for this feature

DIRECT_TEMPLATES = ['index', 'archives', 'authors', 'search']

TIPUE_SEARCH = True

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
        "Image": "/static/img/ramle.png",
        "Website": "https://ramle.be/",
        "Mastodon": "https://toot.gnous.eu/web/accounts/15628",
    },

    "Eban": {
        "Image": "/static/img/eban.png",
        "Website": "https://eban.bzh/",
        "Mastodon": "https://toot.gnous.eu/web/accounts/11793",
        "Twitter": "https://twitter.com/eban_non",
    },

    "Lancelot": {
        "Image": "/static/img/lancelot.png",
        "Website": "https://theredwindows.net/",
        "Twitter": "https://twitter.com/lancelot_ps1",
        "Github": "https://github.com/rootSySdk",
    },

    "MorpheusH3x": {
        "Image": "/static/img/morpheush3x.png",
        "Twitter": "https://twitter.com/MorpheusH3x",
        "Github": "https://github.com/MorpheusH3x",
    },

    "Ownesis": {
        "Image": "/static/img/ownesis.png",
        "Github": "https://github.com/ownesis",
    },

    "Immae": {
        "Image": "https://cdn.discordapp.com/avatars/379693828535222272/f2d7b385da484d404b2de6fd190acb30.png",
        "Website": "https://www.immae.eu/",
    },

    "Outout": {
        "Image": "https://cdn.discordapp.com/avatars/171685542553976832/a72faa4cfaa003681b91214e069c0aad.png",
        "Website": "https://enpls.org",
        "Twitter": "https://twitter.com/outoutxyz",
        "Github": "https://github.com/outout14",
    },
}
