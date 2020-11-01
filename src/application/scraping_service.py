import time

import lxml.html

from shared.tools import full_url
from domain.models import Resource


class ScrapingService:

    def __init__(self, reader, initial_url, delay_secs=1):
        self._reader = reader
        self._initial_url = initial_url
        self._delay_secs = delay_secs
        self._urls_xpath = ''
        self._resource_type = None

    def scrape(self):
        resources = []

        for url in self.get_resources_urls():
            self.delay()

            data = self.resource_data(self._reader.read(url))
            data.update({'type': self._resource_type, 'url': url})

            resources.append(Resource(**data))

        return resources

    def get_resources_urls(self):
        if not self._urls_xpath:
            return []

        html = self._reader.read(self._initial_url)
        doc = lxml.html.fromstring(html)

        return [full_url(self._initial_url, url) for url in doc.xpath(self._urls_xpath)]

    def delay(self):
        if self._delay_secs:
            time.sleep(self._delay_secs)
