from collections import OrderedDict
from unittest import (
    TestCase,
    mock
)

from expects import (
    equal,
    expect
)

from infrastructure import ResourceCsvRepository
from main import main as run_scrapper
from test.utils import FakeHtmlReader


scraping_service_mock_calls = []


class AnotherFakeHtmlReader(FakeHtmlReader):
    pass


class ScrapingServiceMock:

    def __init__(self, reader, repository, initial_url):
        self.__reader = reader
        self.__repository = repository
        self.__initial_url = initial_url

    def scrape(self):
        scraping_service_mock_calls.append(
            (type(self), type(self.__reader), type(self.__repository), self.__initial_url)
        )


class AnotherScrapingServiceMock(ScrapingServiceMock):
    pass


FAKE_RESOURCE_TYPES_CONFIGURATION = {
    'resource_type': {
        'scraper': 'test.test_main.ScrapingServiceMock',
        'reader': 'test.test_main.FakeHtmlReader',
        'initial_url': 'http://some.url.com'
    },
    'another_resource_type': {
        'scraper': 'test.test_main.AnotherScrapingServiceMock',
        'reader': 'test.test_main.AnotherFakeHtmlReader',
        'initial_url': 'http://another.url.com'
    }
}


class MainTestCase(TestCase):

    def setUp(self):
        scraping_service_mock_calls = []

    @mock.patch.dict('main.resource_types_configuration', OrderedDict(FAKE_RESOURCE_TYPES_CONFIGURATION), clear=True)
    def test_it_uses_a_scrapping_service_per_each_resource_type_defined_in_settings(self):
        run_scrapper()

        expect(len(scraping_service_mock_calls)).to(equal(2))
        expect(scraping_service_mock_calls[0]).to(equal((
            ScrapingServiceMock,
            FakeHtmlReader,
            ResourceCsvRepository,
            'http://some.url.com'
        )))
        expect(scraping_service_mock_calls[1]).to(equal((
            AnotherScrapingServiceMock,
            AnotherFakeHtmlReader,
            ResourceCsvRepository,
            'http://another.url.com'
        )))
