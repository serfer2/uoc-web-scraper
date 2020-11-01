from unittest import TestCase

from expects import (
    equal,
    expect
)

from application import CourseScrapingService
from test.utils import FakeHtmlReader


class ScrapingServiceTestCase(TestCase):

    def test_it_retruns_an_empty_list_when_no_resources_found(self):
        reader = FakeHtmlReader(htmls=['<h1>anything</h1>'])
        scraper = CourseScrapingService(reader, 'any_url')

        resources = scraper.scrape()

        expect(resources).to(equal([]))
