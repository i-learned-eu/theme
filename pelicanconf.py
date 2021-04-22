#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Eban'
SITENAME = 'Blog - Eban'
SITEURL = 'https://blog.eban.bzh'

PATH = 'content'
ARTICLE_SAVE_AS = '{category}/{slug}.html'
ARTICLE_URL = '{category}/{slug}.html'

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

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

DISPLAY_CATEGORIES_ON_MENU = True
OUTPUT_SOURCES = False
SUMMARY_MAX_LENGTH = 50
THEME = 'theme/light'
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['sitemap', 'post_stats', 'feed_summary', 'neighbors', 'readtime', 'seo']
STATIC_PATHS = ['static/']

SEO_REPORT = True #To enable this feature
SEO_ENHANCER = True #To disable this feature
SEO_ENHANCER_OPEN_GRAPH = True # The default value for this feature
SEO_ENHANCER_TWITTER_CARDS = True # The default value for this feature

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
