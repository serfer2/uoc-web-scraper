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

    def get_ects_date_init_title(self, html):
        ects = None
        date_init = ''
        title = ''

        doc = lxml.html.fromstring(html)

        for p in doc.xpath('//p[@class="m-bottom-y2"]'):
            text = p.text_content().strip()
            if 'Créditos:' in text:
                ects = text.replace('Créditos:', '').strip().replace('ECTS', '').strip()
            elif 'Inicio:' in text:
                date_init = text.replace('Inicio:', '').strip()
            elif 'Título:' in text:
                title = text.replace('Título:', '').strip()

        return ects, date_init, title

    def x_uoc_resource_data(self, html):
        doc = lxml.html.fromstring(html)

        name = doc.xpath('//h1/text()')[0].strip()
        descriptions = doc.xpath('//span[@property="description"]//p')
        desc = ' '.join([d.text_content().strip() for d in descriptions])

        duration = doc.xpath('//div[@class="iconsProd bg-x"]//div/text()')[0].strip()
        date_init = doc.xpath('//div[@class="iconsProd bg-x"]//div/text()')[3].strip()
        price = doc.xpath('//div[@class="iconsProd bg-x"]//div/text()')[4].strip()

        title = doc.xpath('//div[@class="titulacion"]/text()')[0].strip()

        return {
            'name': name,
            'description': desc,
            'duration': duration,
            'date_init': date_init,
            'price': price,
            'title': title
        }
