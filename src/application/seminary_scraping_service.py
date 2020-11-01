from application.scraping_service import ScrapingService
from domain.models import Resource


class SeminaryScrapingService(ScrapingService):

    def __init__(self, *args, **kwargs):
        super(SeminaryScrapingService, self).__init__(*args, **kwargs)

        self._resource_type = Resource.TYPE_SEMINARIO
        self._urls_xpath = '//div[@class="col-md-4 prodFilter "]//a[@class="card-absolute-link"]/@href'

    def resource_data(self, html):
        return self.x_uoc_resource_data(html)
