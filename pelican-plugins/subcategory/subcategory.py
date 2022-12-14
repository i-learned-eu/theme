# -*- coding: utf-8 -*-
"""
@Author: Alistair Magee
Adds support for subcategories on pelican articles
"""
import os
from operator import attrgetter
from functools import partial

from pelican import signals
from pelican.urlwrappers import URLWrapper, Category
from pelican.utils import slugify

from six import text_type

class SubCategory(URLWrapper):
    def __init__(self, name, parent, settings):
        super(SubCategory, self).__init__(name, settings)
        self.parent = parent
        self.shortname = name.split('/')
        self.shortname = self.shortname.pop()
        self.slug = slugify(self.shortname, settings.get('SLUG_SUBSTITUIONS', ()))
        if isinstance(self.parent, SubCategory):
            self.savepath = os.path.join(self.parent.savepath, self.slug)
            self.fullurl = '{}/{}'.format(self.parent.fullurl, self.slug)
        else: #parent is a category
            self.savepath = os.path.join(self.parent.slug, self.slug)
            self.fullurl = '{}/{}'.format(self.parent.slug, self.slug)

    def as_dict(self):
        d = self.__dict__
        d['shortname'] = self.shortname
        d['savepath'] = self.savepath
        d['fullurl'] = self.fullurl
        d['parent'] = self.parent
        return d

    def __hash__(self):
        return hash(self.fullurl)

    def _key(self):
        return self.fullurl

def get_subcategories(generator, metadata):
    if 'SUBCATEGORY_SAVE_AS' not in generator.settings:
        generator.settings['SUBCATEGORY_SAVE_AS'] = os.path.join(
                'subcategory', '{savepath}.html')
    if 'SUBCATEGORY_URL' not in generator.settings:
        generator.settings['SUBCATEGORY_URL'] = 'subcategory/{fullurl}.html'
    if ('PAGINATED_TEMPLATES' in generator.settings and
        'subcategory' not in generator.settings['PAGINATED_TEMPLATES']):
        generator.settings['PAGINATED_TEMPLATES']['subcategory'] = None

    if 'subcategory_path' in metadata:
        category_list = text_type(metadata.get('subcategory_path')).split('/')
    else:
        category_list = text_type(metadata.get('category')).split('/')

    category = (category_list.pop(0)).strip()
    category = Category(category, generator.settings)
    metadata['category'] = category
    #generate a list of subcategories with their parents
    sub_list = []
    parent = category.name
    for subcategory in category_list:
        subcategory = parent + '/' + subcategory.strip()
        sub_list.append(subcategory)
        parent = subcategory
    metadata['subcategories'] = sub_list

def create_subcategories(generator):
    generator.subcategories = []
    for article in generator.articles:
        parent = article.category
        actual_subcategories = []
        for subcategory in article.subcategories:
            #following line returns a list of items, tuples in this case
            sub_cat = [item for item in generator.subcategories
                    if item[0].name == subcategory]
            if sub_cat:
                sub_cat[0][1].append(article)
                parent = sub_cat[0][0]
                actual_subcategories.append(parent)
            else:
                new_sub = SubCategory(subcategory, parent, generator.settings)
                generator.subcategories.append((new_sub, [article,]))
                parent = new_sub
                actual_subcategories.append(parent)
        article.subcategories = actual_subcategories
        """Add subpath and suburl to the article metadata. This allows the
        the last subcategory's fullurl and savepath to be used when definining
        Article URL's. If an article has no subcategories, the Category slug
        is used instead
        """
        try:
            last_subcat = article.subcategories[-1]
            article.metadata['subpath'] = last_subcat.savepath
            article.metadata['suburl'] = last_subcat.fullurl
        except IndexError: #No Subcategory
            article.metadata['subpath'] = article.category.slug
            article.metadata['suburl'] = article.category.slug

def generate_subcategories(generator, writer):
    write = partial(writer.write_file,
            relative_urls=generator.settings['RELATIVE_URLS'])
    subcategory_template = generator.get_template('subcategory')
    for subcat, articles in generator.subcategories:
        articles.sort(key=attrgetter('date'), reverse=True)
        dates = [article for article in generator.dates if article in articles]
        write(subcat.save_as, subcategory_template, generator.context,
                subcategory=subcat, articles=articles, dates=dates,
                template_name='subcategory', page_name=subcat.page_name,
                all_articles=generator.articles)

def generate_subcategory_feeds(generator, writer):
    for subcat, articles in generator.subcategories:
        articles.sort(key=attrgetter('date'), reverse=True)
        if generator.settings.get('SUBCATEGORY_FEED_ATOM'):
            writer.write_feed(articles, generator.context,
                    generator.settings['SUBCATEGORY_FEED_ATOM']
                    % subcat.fullurl)
        if generator.settings.get('SUBCATEGORY_FEED_RSS'):
            writer.write_feed(articles, generator.context,
                    generator.settings['SUBCATEGORY_FEED_RSS']
                    % subcat.fullurl, feed_type='rss')

def generate(generator, writer):
    generate_subcategory_feeds(generator, writer)
    generate_subcategories(generator, writer)

def register():
    signals.article_generator_context.connect(get_subcategories)
    signals.article_generator_finalized.connect(create_subcategories)
    signals.article_writer_finalized.connect(generate)
