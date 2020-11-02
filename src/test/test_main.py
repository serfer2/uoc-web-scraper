import os
from collections import OrderedDict
from unittest import (
    TestCase,
    mock
)

from expects import (
    equal,
    expect
)
from freezegun import freeze_time

from main import main as run_scrapper
from shared.tools import clean_html
from test.utils import FakeHtmlReader


scraping_service_mock_calls = []


class AnotherFakeHtmlReader(FakeHtmlReader):
    pass


class ScrapingServiceMock:

    def __init__(self, reader, initial_url):
        self.__reader = reader
        self.__initial_url = initial_url

    def scrape(self):
        scraping_service_mock_calls.append(
            (type(self), type(self.__reader), self.__initial_url)
        )
        return []


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

FAKE_RESOURCE_TYPES_CONFIGURATION_FOR_MASTER = {
    'Máster': {
        'scraper': 'application.MasterScrapingService',
        'reader': 'infrastructure.HtmlReader',
        'initial_url': 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/master'
    }
}


class MainTestCase(TestCase):

    def setUp(self):
        scraping_service_mock_calls = []

    @classmethod
    def tearDownClass(cls):
        try:
            os.unlink(f'{os.path.dirname(__file__)}/../store/uoc_educational_offer__2020-11-01_212325.csv')
        except:
            pass
        try:
            os.unlink(f'{os.path.dirname(__file__)}/../store/uoc_educational_offer__2020-11-01_212326.csv')
        except:
            pass

    @freeze_time("2020-11-01 21:23:25")
    @mock.patch.dict('main.resource_types_configuration', OrderedDict(FAKE_RESOURCE_TYPES_CONFIGURATION), clear=True)
    def test_it_uses_a_scrapping_service_per_each_resource_type_defined_in_settings(self):
        run_scrapper()

        expect(len(scraping_service_mock_calls)).to(equal(2))
        expect(scraping_service_mock_calls[0]).to(equal((
            ScrapingServiceMock,
            FakeHtmlReader,
            'http://some.url.com'
        )))
        expect(scraping_service_mock_calls[1]).to(equal((
            AnotherScrapingServiceMock,
            AnotherFakeHtmlReader,
            'http://another.url.com'
        )))

    @freeze_time("2020-11-01 21:23:26")
    @mock.patch.dict('main.resource_types_configuration', FAKE_RESOURCE_TYPES_CONFIGURATION_FOR_MASTER, clear=True)
    @mock.patch('infrastructure.html_reader.HtmlReader.read')
    @mock.patch('application.scraping_service.ScrapingService.get_resources_urls')
    def test_it_stores_resources_in_csv_repository(self, get_resources_urls, html_reader_read):
        with open(f'{os.path.dirname(__file__)}/fixtures/master01.html', 'r') as f:
            html_master = clean_html(f.read())
        get_resources_urls.return_value = ['http://some_fake_url.com/01']
        html_reader_read.return_value = html_master

        run_scrapper()

        with open(f'{os.path.dirname(__file__)}/../store/uoc_educational_offer__2020-11-01_212326.csv', 'r') as f:
            lines = f.readlines()

        expect(len(lines)).to(equal(2))
        expect(lines[0]).to(equal(
            'type;name;description;duration;title;ects;price;url;date_init\n'
        ))
        expect(lines[1]).to(equal('master;Máster de Edición Digital;El máster en línea de Edición digital de la UOC proporciona al estudiante una formación integral en el mundo del libro, tanto en papel como en formato electrónico, y estimula su capacidad de adaptación y de innovación tecnológica en el contexto del sector editorial, una industria en constante evolución.;;Edición Digital;;;http://some_fake_url.com/01;17 marzo 2021\n'))
