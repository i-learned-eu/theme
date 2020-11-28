#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Eban'
SITENAME = 'Blog - Eban'
SITEURL = 'http://10.0.0.11:8000'

PATH = 'content'
ARTICLE_SAVE_AS = '{category}/{slug}.html'
ARTICLE_URL = '{category}/{slug}.html'

TIMEZONE = 'Europe/Paris'
DEFAULT_DATE_FORMAT = '%a %d %B %Y'

DEFAULT_LANG = 'fr'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Accueil', 'https://blog.ramle.be'),
         ('ramle.be', 'https://ramle.be'),
         ('Contact', 'https:/ramle.be/contact/'),
         ('Plus sur ce site', 'https://blog.ramle.be/about/'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

DISPLAY_CATEGORIES_ON_MENU = True
OUTPUT_SOURCES = False
SUMMARY_MAX_LENGTH = 50
THEME = 'theme/light'
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['sitemap', 'post_stats', 'feed_summary', 'neighbors']
STATIC_PATHS = ['static/']
