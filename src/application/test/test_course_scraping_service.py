import os
from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
    have_keys
)

from application import CourseScrapingService
from test.utils import FakeHtmlReader


class CourseScrapingServiceTestCase(TestCase):

    def test_it_gets_all_course_detail_urls(self):
        html = ''
        # 77 courses
        with open(f'{os.path.dirname(__file__)}/fixtures/cursos.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        url = 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/curso'
        scraper = CourseScrapingService(reader, url)

        urls_xpath = '//div[@data-type="product"]//a[@class="card-absolute-link"]/@href'
        urls = scraper.get_resources_urls(urls_xpath)

        expect(len(urls)).to(equal(77))
        expect(urls[0]).to(equal('https://estudios.uoc.edu/es/masters-posgrados-especializaciones/curso/comunicacion-informacion/acontecimientos-virtuales/presentacion'))
        expect(urls[76]).to(equal('https://estudios.uoc.edu/es/masters-posgrados-especializaciones/curso/psicologia-ciencias-educacion/tecnicas-neuroimagen/presentacion'))

    def test_it_extracts_resource_data_from_detail_page(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/curso01.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        scraper = CourseScrapingService(reader, 'any_url')

        data = scraper.resource_data(reader.read('any_url'))

        expect(data).to(have_keys({
            'name': 'Curso de Diseño de Interacción: Procesos, Métodos y Técnicas',
            'description': 'El curso en Diseño de Interacción. Procesos, Métodos y Técnicas ofrece una introducción a cómo diseñar un producto accesible y fácil para el usuario.',
            'date_init': '17 febrero 2021',
            'title': 'Diseño de Interacción: Procesos, Métodos y Técnicas'
        }))

    @patch('application.scraping_service.ScrapingService.get_resources_urls')
    def test_it_retruns_a_resources_list(self, get_resources_urls):
        html_course01 = ''
        html_course02 = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/curso01.html', 'r') as fin:
            html_course01 = fin.read()
        with open(f'{os.path.dirname(__file__)}/fixtures/curso02.html', 'r') as fin:
            html_course02 = fin.read()
        reader = FakeHtmlReader(htmls=[html_course01, html_course02])
        scraper = CourseScrapingService(reader, 'any_url')
        get_resources_urls.return_value = [
            'http://some_fake_url.com/course01',
            'http://some_fake_url.com/course02'
        ]

        resources = scraper.scrape()

        expect(len(resources)).to(equal(2))
        expect(resources[0].as_dict()).to(have_keys({
            'type': 'curso',
            'name': 'Curso de Diseño de Interacción: Procesos, Métodos y Técnicas',
            'description': 'El curso en Diseño de Interacción. Procesos, Métodos y Técnicas ofrece una introducción a cómo diseñar un producto accesible y fácil para el usuario.',
            'duration': '',
            'title': 'Diseño de Interacción: Procesos, Métodos y Técnicas',
            'ects': None,
            'price': None,
            'url': 'http://some_fake_url.com/course01',
            'date_init': '17 febrero 2021'
        }))
        expect(resources[1].as_dict()).to(have_keys({
            'type': 'curso',
            'name': 'Curso de Técnicas de neuroimagen',
            'description': 'Las técnicas de neuroimagen se han convertido hoy en las herramientas por excelencia para el estudio del cerebro humano y el número de publicaciones científicas en las que se emplean estas técnicas no ha parado de crecer en las últimas décadas.',
            'duration': '',
            'title': 'Técnicas de neuroimagen',
            'ects': None,
            'price': None,
            'url': 'http://some_fake_url.com/course02',
            'date_init': '17 marzo 2021'
        }))
