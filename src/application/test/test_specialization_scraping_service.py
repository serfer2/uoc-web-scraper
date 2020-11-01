import os
from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
    have_keys
)

from application import SpecializationScrapingService
from test.utils import FakeHtmlReader


class SpecializationScrapingServiceTestCase(TestCase):

    def test_it_gets_all_diploma_detail_urls(self):
        html = ''
        # 97 specializations
        filepath = f'{os.path.dirname(__file__)}/fixtures/especializaciones.html'
        with open(filepath, 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        url = 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/especializacion'
        scraper = SpecializationScrapingService(reader, url)

        urls = scraper.get_resources_urls()

        expect(len(urls)).to(equal(97))
        expect(urls[0]).to(equal('https://estudios.uoc.edu/es/masters-posgrados-especializaciones/especializacion/artes-humanidades/aicle-clil-tecnologia-idiomas/presentacion'))
        expect(urls[96]).to(equal('https://estudios.uoc.edu/es/masters-posgrados-especializaciones/especializacion/economia-empresa/politica-turistica-destinaciones-turisticas/presentacion'))

    def test_it_extracts_resource_data_from_detail_page(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/especializacion02.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        scraper = SpecializationScrapingService(reader, 'any_url')

        data = scraper.resource_data(reader.read('any_url'))

        expect(data).to(have_keys({
            'name': 'Especialización de Política Turística para los Destinos Turísticos (OMT, UOC)',
            'description': 'La actividad turística en la actual sociedad del conocimiento y la información está sujeta a cambios profundos y complejos que obliga a un proceso sistemático de mejora continua en la adopción e implementación de las políticas y estrategias aplicables a la actividad turística.',
            'date_init': '20 octubre 2021',
            'title': 'Política Turística para los Destinos Turísticos (OMT, UOC)',
        }))

    @patch('application.scraping_service.ScrapingService.get_resources_urls')
    def test_it_retruns_a_resources_list(self, get_resources_urls):
        html_specialization01 = ''
        html_specialization02 = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/especializacion01.html', 'r') as fin:
            html_specialization01 = fin.read()
        with open(f'{os.path.dirname(__file__)}/fixtures/especializacion02.html', 'r') as fin:
            html_specialization02 = fin.read()
        reader = FakeHtmlReader(htmls=[html_specialization01, html_specialization02])
        scraper = SpecializationScrapingService(reader, 'any_url')
        get_resources_urls.return_value = [
            'http://some_fake_url.com/01',
            'http://some_fake_url.com/02'
        ]

        resources = scraper.scrape()

        expect(len(resources)).to(equal(2))
        expect(resources[0].as_dict()).to(have_keys({
            'type': 'especializacion',
            'name': 'Especialización de AICLE / CLIL y Enfoque por Tareas mediante Tecnología',
            'description': 'La especialización de AICLE / CLIL y el Enfoque por Tareas mediante la Tecnología capacita a los profesionales de la enseñanza de idiomas a aplicar la tecnología a programas de enseñanza AICLE y de enfoque por tareas.',
            'duration': '',
            'title': 'AICLE / CLIL y Enfoque por Tareas mediante Tecnología',
            'ects': None,
            'price': None,
            'url': 'http://some_fake_url.com/01',
            'date_init': '20 octubre 2021'
        }))
        expect(resources[1].as_dict()).to(have_keys({
            'type': 'especializacion',
            'name': 'Especialización de Política Turística para los Destinos Turísticos (OMT, UOC)',
            'description': 'La actividad turística en la actual sociedad del conocimiento y la información está sujeta a cambios profundos y complejos que obliga a un proceso sistemático de mejora continua en la adopción e implementación de las políticas y estrategias aplicables a la actividad turística.',
            'duration': '',
            'title': 'Política Turística para los Destinos Turísticos (OMT, UOC)',
            'ects': None,
            'price': None,
            'url': 'http://some_fake_url.com/02',
            'date_init': '20 octubre 2021'
        }))
