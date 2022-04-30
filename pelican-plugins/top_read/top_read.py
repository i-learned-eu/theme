from pelican import signals
import requests


def init(generator):
    data = requests.get(generator.settings.get('GOACCESS_JSON_URI')).json()
    top_read = []
    for article in generator.articles:
        i = 0
        while article.slug != data['requests']['data'][i]['data']:
            if i + 1 < data['requests']['metadata']['data']['total']['value']:
                i += 1
            else:
                break

        article = {
            'url': '/' + data['requests']['data'][i]['data'] + '.html',
            'title': article.title,
            'author': article.author,
            'locale_date': article.locale_date,
            'readtime': article.readtime['minutes'],
            'summary': article.summary,
            'views': data['requests']['data'][i]['visitors']['count']
        }
        top_read.append(article)
    top_read = sorted(top_read, key=lambda d: d['views'])
    top_read.reverse()
    generator.context['TOP_READ'] = top_read


def register():
    signals.article_generator_finalized.connect(init)
