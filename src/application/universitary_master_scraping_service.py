import lxml.html

from application.scraping_service import ScrapingService
from domain.models import Resource


class UniversitaryMasterScrapingService(ScrapingService):

    def __init__(self, *args, **kwargs):
        super(UniversitaryMasterScrapingService, self).__init__(*args, **kwargs)

        self._resource_type = Resource.TYPE_MASTER_UNIVERSITARIO
        self._urls_xpath = '//div[@data-type="product"]//a[@class="card-absolute-link"]/@href'

    def resource_data(self, html):
        doc = lxml.html.fromstring(html)

        name = doc.xpath('//h1')[0].text_content().strip()
        desc = doc.xpath('//section[@class="flexbox-layout m-bottom-2y uc227 is-first-unfolded"]')[0].text_content().strip()

        ects, date_init, title = self.get_ects_date_init_title(html)

        return {
            'name': name,
            'description': desc,
            'ects': ects,
            'date_init': date_init,
            'title': title
        }
