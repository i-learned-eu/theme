from pelican import signals
import json
import os


def init(generator):
    data = {
        "children": [],
        "name": "I Learned",
        "type": "folder"
    }
    for category in generator.categories:
        if "/" in str(category[0]):
            pass

        categoryData = {
            "children": [],
            "name": str(category[0]),
            "type": "folder"
        }
        for article in category[1]:
            articleData = {
                "name": article.title,
                "type": "url",
                "url": article.slug
            }
            if len(article.subcategories) > 0:
                if not any(d['name'] == article.subcategories[0].shortname for d in categoryData['children']):
                    pass
                    subCategoryData = {
                        "children": [],
                        "name": article.subcategories[0].shortname,
                        "type": "folder"
                    }
                    categoryData['children'].append(subCategoryData)
                i = 0
                while categoryData['children'][i]['name'] != article.subcategories[0].shortname:
                    i += 1

                categoryData['children'][i]['children'].append(articleData)
            else:
                categoryData['children'].append(articleData)
        data['children'].append(categoryData)
    os.makedirs("output/static/misc", exist_ok=True)
    text_file = open("output/static/misc/tree.json", "w")
    text_file.write(json.dumps(data))


def register():
    signals.article_generator_finalized.connect(init)
