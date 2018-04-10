import requests
import time
import logging
import bs4
from urllib.parse import urljoin

from .titles import get_title
from .dates import get_publish_date

logger = logging.getLogger(__name__)


def extract(result):
    doc = bs4.BeautifulSoup(result)
    return {
        'title': get_title(doc),
        'published': get_publish_date(doc),
    }


class StatusError(Exception):

    def __init__(self, status):
        self.status = status
        super().__init__('Unexpected status code: {}'.format(status))


def scrape(url, timeout=30, headers={'User-Agent': 'test agent'}, retry=(1, 2)):
    if 'Referer' not in headers:
        headers['Referer'] = urljoin(url, '/')

    for i in range(len(retry) + 1):
        try:
            result = requests.get(url, timeout=timeout)
        except requests.Timeout:
            logger.info('Timeout on url %s after %ss', url, timeout)
            if i < len(retry):
                time.sleep(retry[i])
                continue
            raise TimeoutError('Timeout scraping url {}'.format(url))
        except:
            logger.error('Unknown error scraping url %s', url)
            if i < len(retry):
                time.sleep(retry[i])
                continue
            raise

        if result.status_code != 200:
            if i < len(retry):
                time.sleep(retry[i])
                continue
            raise StatusError(result.status_code)
        break

    return extract(result.content)
