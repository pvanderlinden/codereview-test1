from functools import partial
import logging

from dateutil.parser import parse

logger = logging.getLogger(__name__)


def node_attribute(doc, attrs, attr='content'):
    attrs[attr] = True
    node = doc.find(**attrs)
    if node:
        return node.attrs[attr]


def get_publish_date(doc):
    for extract in PUBLISH_DATE_EXTRACTORS:
        value = extract(doc)
        if value:
            try:
                return parse(value)
            except Exception:
                pass


PUBLISH_DATE_EXTRACTORS = (
    partial(node_attribute, attrs={'property': 'article:published_time'}),
    partial(node_attribute, attrs={'itemprop': 'datePublished'}, attr='datetime'),
    partial(node_attribute, attrs={'itemprop': 'datePublished'}, attr='content'),
    partial(node_attribute, attrs={'property': 'og:published_time'}),
    partial(node_attribute, attrs={'name': 'publication_date'}),
    partial(node_attribute, attrs={'name': 'PublishDate'}),
)
