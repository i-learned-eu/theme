from pelican import signals
from bs4 import BeautifulSoup


def wrap_image_tags(p):
    if p._content is not None:
        content = p._content
        soup = BeautifulSoup(content)

        # Wrap each image tag in an anchor with a link.  Add the
        # attribute for the lightbox set to activate.
        if 'img' in content:
            for tag in soup('img'):
                tag['class'] = "card"
            p._content = soup.decode()


def register():
    signals.content_object_init.connect(wrap_image_tags)
