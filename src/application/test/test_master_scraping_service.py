import os
from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
    have_keys
)

from application import MasterScrapingService
from test.utils import FakeHtmlReader


class DiplomaScrapingServiceTestCase(TestCase):

    def test_it_gets_all_diploma_detail_urls(self):
        html = ''
        # 20 masters
        filepath = f'{os.path.dirname(__file__)}/fixtures/masters.html'
        with open(filepath, 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        url = 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/master'
        scraper = MasterScrapingService(reader, url)

        urls = scraper.get_resources_urls()

        expect(len(urls)).to(equal(20))
        expect(urls[0]).to(equal('https://estudios.uoc.edu/es/masters-posgrados-especializaciones/master/artes-humanidades/edicion-digital/presentacion'))
        expect(urls[19]).to(equal('https://estudios.uoc.edu/es/masters-posgrados-especializaciones/master/turismo/destinaciones-turisticas-estrategia-gestion-sostenible/presentacion'))

    def test_it_extracts_resource_data_from_detail_page(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/master02.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        scraper = MasterScrapingService(reader, 'any_url')

        data = scraper.resource_data(reader.read('any_url'))

        expect(data).to(have_keys({
            'name': 'Máster de Industria 4.0 (interuniversitario: UOC, ESUPT)',
            'description': 'El máster de Industria 4.0 Online es un programa de ámbito tecnológico y de carácter profesionalizador diseñado para proporcionar una formación exhaustiva y práctica orientada a profesionales y directivos del ámbito de la industria que quieran actualizar sus conocimientos en el marco de la Industria 4.0, a partir del estudio de casos reales de empresas del sector.',
            'date_init': '20 octubre 2021',
            'title': 'Industria 4.0 (interuniversitario: UOC, ESUPT)',
            'ects': '60'
        }))

    @patch('application.scraping_service.ScrapingService.get_resources_urls')
    def test_it_retruns_a_resources_list(self, get_resources_urls):
        html_master01 = ''
        html_master02 = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/master01.html', 'r') as fin:
            html_master01 = fin.read()
        with open(f'{os.path.dirname(__file__)}/fixtures/master02.html', 'r') as fin:
            html_master02 = fin.read()
        reader = FakeHtmlReader(htmls=[html_master01, html_master02])
        scraper = MasterScrapingService(reader, 'any_url')
        get_resources_urls.return_value = [
            'http://some_fake_url.com/01',
            'http://some_fake_url.com/02'
        ]

        resources = scraper.scrape()

        expect(len(resources)).to(equal(2))
        expect(resources[0].as_dict()).to(have_keys({
            'type': 'master',
            'name': 'Máster de Edición Digital',
            'description': 'El máster en línea de Edición digital de la UOC proporciona al estudiante una formación integral en el mundo del libro, tanto en papel como en formato electrónico, y estimula su capacidad de adaptación y de innovación tecnológica en el contexto del sector editorial, una industria en constante evolución.',
            'duration': '',
            'title': 'Edición Digital',
            'ects': None,
            'price': None,
            'url': 'http://some_fake_url.com/01',
            'date_init': '17 marzo 2021'
        }))
        expect(resources[1].as_dict()).to(have_keys({
            'type': 'master',
            'name': 'Máster de Industria 4.0 (interuniversitario: UOC, ESUPT)',
            'description': 'El máster de Industria 4.0 Online es un programa de ámbito tecnológico y de carácter profesionalizador diseñado para proporcionar una formación exhaustiva y práctica orientada a profesionales y directivos del ámbito de la industria que quieran actualizar sus conocimientos en el marco de la Industria 4.0, a partir del estudio de casos reales de empresas del sector.',
            'duration': '',
            'title': 'Industria 4.0 (interuniversitario: UOC, ESUPT)',
            'ects': '60',
            'price': None,
            'url': 'http://some_fake_url.com/02',
            'date_init': '20 octubre 2021'
        }))
