import os
from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
    have_keys
)

from application import SeminaryScrapingService
from test.utils import FakeHtmlReader


class SeminaryScrapingServiceTestCase(TestCase):

    def test_it_gets_all_seminary_detail_urls(self):
        html = ''
        # 34 seminaries
        filepath = f'{os.path.dirname(__file__)}/fixtures/seminarios.html'
        with open(filepath, 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        url = 'https://x.uoc.edu/es/que-quieres-estudiar/seminarios/'
        scraper = SeminaryScrapingService(reader, url)

        urls = scraper.get_resources_urls()

        expect(len(urls)).to(equal(34))
        expect(urls[0]).to(equal('https://x.uoc.edu/es/seminarios-desarrollo-continuo/coaching-introduccion/'))
        expect(urls[33]).to(equal('https://x.uoc.edu/es/seminarios-desarrollo-continuo/writing-skills-for-work-2/'))

    def test_it_extracts_resource_data_from_detail_page(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/seminary02.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        scraper = SeminaryScrapingService(reader, 'any_url')

        data = scraper.resource_data(reader.read('any_url'))

        expect(data).to(have_keys({
            'name': 'La cocina, la herramienta para comer bien (UOC, Fundación Alícia)',
            'description': 'En las generaciones jóvenes se observa, además de un incremento en el consumo de productos procesados y una pérdida de habilidades culinarias, una cierta desconexión o desconocimiento del origen de los alimentos y del impacto global sobre las decisiones alimentarias (repercusiones económicas, ambientales, sociales, de salud, etc.). Recuperar estas habilidades, el conocimiento sobre los productos locales y de temporada, y cómo las técnicas culinarias pueden contribuir a maximizar las propiedades nutricionales de algunos alimentos pueden ser buenas herramientas para conseguir una alimentación más saludable. Este curso está considerado como formación permanente del profesorado. Para que conste en el expediente, se deberá seguir el procedimiento habitual para este tipo de formaciones. En colaboración con: ',
            'duration': '1 mes',
            'date_init': 'Próximamente',
            'price': '297€',
            'title': 'Certificado de aprovechamiento de la UOC'
        }))

    @patch('application.scraping_service.ScrapingService.get_resources_urls')
    def test_it_retruns_a_resources_list(self, get_resources_urls):
        html_seminary01 = ''
        html_seminary02 = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/seminary01.html', 'r') as fin:
            html_seminary01 = fin.read()
        with open(f'{os.path.dirname(__file__)}/fixtures/seminary02.html', 'r') as fin:
            html_seminary02 = fin.read()
        reader = FakeHtmlReader(htmls=[html_seminary01, html_seminary02])
        scraper = SeminaryScrapingService(reader, 'any_url')
        get_resources_urls.return_value = [
            'http://some_fake_url.com/01',
            'http://some_fake_url.com/02'
        ]

        resources = scraper.scrape()

        expect(len(resources)).to(equal(2))
        expect(resources[0].as_dict()).to(have_keys({
            'type': 'seminario',
            'name': 'Introducción al coaching',
            'description': 'Visión general sobre los conceptos básicos del coaching (entrenamiento personal) y de su práctica. Este curso plantea herramientas básicas para iniciarse en la práctica del coaching y, sobre todo, en el autoconocimiento. La metodología del curso se fundamenta en la participación y escucha activa a las personas que nos rodean. También hace hincapié en la experimentación de las nuevas habilidades por parte de los participantes, que permitan un proceso permanente de revisión, remodelación y reformulación de sus necesidades y capacidades. El seminario forma parte de un proyecto de innovación, en el que se desarrollará una metodología específica para potenciar la capacitación profesional para el coaching con recursos tecnológicos innovadores.',
            'duration': '1 mes',
            'title': 'Certificado de aprovechamiento de la UOC',
            'ects': None,
            'price': '198€',
            'url': 'http://some_fake_url.com/01',
            'date_init': '16 Junio'
        }))
        expect(resources[1].as_dict()).to(have_keys({
            'type': 'seminario',
            'name': 'La cocina, la herramienta para comer bien (UOC, Fundación Alícia)',
            'description': 'En las generaciones jóvenes se observa, además de un incremento en el consumo de productos procesados y una pérdida de habilidades culinarias, una cierta desconexión o desconocimiento del origen de los alimentos y del impacto global sobre las decisiones alimentarias (repercusiones económicas, ambientales, sociales, de salud, etc.). Recuperar estas habilidades, el conocimiento sobre los productos locales y de temporada, y cómo las técnicas culinarias pueden contribuir a maximizar las propiedades nutricionales de algunos alimentos pueden ser buenas herramientas para conseguir una alimentación más saludable. Este curso está considerado como formación permanente del profesorado. Para que conste en el expediente, se deberá seguir el procedimiento habitual para este tipo de formaciones. En colaboración con: ',
            'duration': '1 mes',
            'title': 'Certificado de aprovechamiento de la UOC',
            'ects': None,
            'price': '297€',
            'url': 'http://some_fake_url.com/02',
            'date_init': 'Próximamente'
        }))
