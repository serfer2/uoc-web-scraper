import os
from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
    have_keys
)

from application import DiplomaScrapingService
from test.utils import FakeHtmlReader


class DiplomaScrapingServiceTestCase(TestCase):

    def test_it_gets_all_diploma_detail_urls(self):
        html = ''
        # 73 diplomas
        filepath = f'{os.path.dirname(__file__)}/fixtures/diplomas-posgrado.html'
        with open(filepath, 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        url = 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/diploma-posgrado'
        scraper = DiplomaScrapingService(reader, url)

        urls = scraper.get_resources_urls()

        expect(len(urls)).to(equal(73))
        expect(urls[0]).to(equal('https://estudios.uoc.edu/es/masters-posgrados-especializaciones/diploma-posgrado/artes-humanidades/arte-contemporaneo/presentacion'))
        expect(urls[72]).to(equal('https://estudios.uoc.edu/es/masters-posgrados-especializaciones/diploma-posgrado/economia-empresa/planificacion-gestion-destinaciones-turisticas/presentacion'))

    def test_it_extracts_resource_data_from_detail_page(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/diploma02.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        scraper = DiplomaScrapingService(reader, 'any_url')

        data = scraper.resource_data(reader.read('any_url'))

        expect(data).to(have_keys({
            'name': 'Diploma de Posgrado de Marketing y Comunicación de los Destinos Turísticos (OMT, UOC)',
            'description': 'La actividad turística en la actual sociedad del conocimiento y la información está sujeta a cambios profundos y complejos que obliga a un proceso sistemático de mejora continua en la adopción e implementación de las políticas y estrategias aplicables a la actividad turística.',
            'date_init': '20 octubre 2021',
            'title': 'Marketing y Comunicación de los Destinos Turísticos (OMT, UOC)'
        }))

    @patch('application.scraping_service.ScrapingService.get_resources_urls')
    def test_it_retruns_a_resources_list(self, get_resources_urls):
        html_diploma01 = ''
        html_diploma02 = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/diploma01.html', 'r') as fin:
            html_diploma01 = fin.read()
        with open(f'{os.path.dirname(__file__)}/fixtures/diploma02.html', 'r') as fin:
            html_diploma02 = fin.read()
        reader = FakeHtmlReader(htmls=[html_diploma01, html_diploma02])
        scraper = DiplomaScrapingService(reader, 'any_url')
        get_resources_urls.return_value = [
            'http://some_fake_url.com/01',
            'http://some_fake_url.com/02'
        ]

        resources = scraper.scrape()

        expect(len(resources)).to(equal(2))
        expect(resources[0].as_dict()).to(have_keys({
            'type': 'diploma_de_posgrado',
            'name': 'Diploma de Posgrado de Desarrollo de Aplicaciones Educativas',
            'description': 'El posgrado de Desarrollo de Aplicaciones Educativas de la UOC proporciona las herramientas y los conocimientos para entender las necesidades educativas y crear las aplicaciones necesarias para cubrirlas en un marco intuitivo y apto para personas no experimentadas.',
            'duration': '',
            'title': 'Desarrollo de Aplicaciones Educativas',
            'ects': None,
            'price': None,
            'url': 'http://some_fake_url.com/01',
            'date_init': '20 octubre 2021'
        }))
        expect(resources[1].as_dict()).to(have_keys({
            'type': 'diploma_de_posgrado',
            'name': 'Diploma de Posgrado de Marketing y Comunicación de los Destinos Turísticos (OMT, UOC)',
            'description': 'La actividad turística en la actual sociedad del conocimiento y la información está sujeta a cambios profundos y complejos que obliga a un proceso sistemático de mejora continua en la adopción e implementación de las políticas y estrategias aplicables a la actividad turística.',
            'duration': '',
            'title': 'Marketing y Comunicación de los Destinos Turísticos (OMT, UOC)',
            'ects': None,
            'price': None,
            'url': 'http://some_fake_url.com/02',
            'date_init': '20 octubre 2021'
        }))
