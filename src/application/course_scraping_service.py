import lxml.html

from application.scraping_service import ScrapingService
from domain.models import Resource


class CourseScrapingService(ScrapingService):

    def __init__(self, *args, **kwargs):
        super(CourseScrapingService, self).__init__(*args, **kwargs)

        self._resource_type = Resource.TYPE_CURSO
        self._urls_xpath = '//div[@data-type="product"]//a[@class="card-absolute-link"]/@href'

    def resource_data(self, html):
        doc = lxml.html.fromstring(html)

        name = doc.xpath('//h1')[0].text_content().strip()
        desc = doc.xpath('//section[@class="flexbox-layout m-bottom-2y uc227 is-first-unfolded"]//p')[0].text_content().strip()
        date_init = doc.xpath('//p[@class="m-bottom-y2"]/text()')[0].strip()
        title = doc.xpath('//p[@class="m-bottom-y2"]/text()')[1].strip()

        return {
            'name': name,
            'description': desc,
            'date_init': date_init,
            'title': title
        }
