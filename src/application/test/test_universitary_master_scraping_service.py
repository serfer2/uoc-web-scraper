import os
from unittest import TestCase
from unittest.mock import patch

from expects import (
    equal,
    expect,
    have_keys
)

from application import UniversitaryMasterScrapingService
from test.utils import FakeHtmlReader


class UniversitaryMasterScrapingServiceTestCase(TestCase):

    def test_it_gets_all_diploma_detail_urls(self):
        html = ''
        # 63 masters universitarios
        filepath = f'{os.path.dirname(__file__)}/fixtures/masters_universitarios.html'
        with open(filepath, 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        url = 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/master-universitario'
        scraper = UniversitaryMasterScrapingService(reader, url)

        urls = scraper.get_resources_urls()

        expect(len(urls)).to(equal(63))
        expect(urls[0]).to(equal('https://estudios.uoc.edu/es/masters-universitarios/ensenanza-idiomas-tecnologia/presentacion'))
        expect(urls[62]).to(equal('https://estudios.uoc.edu/es/masters-universitarios/turismo-sostenibilidad-tic/presentacion'))

    def test_it_extracts_resource_data_from_detail_page(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/master_universitario02.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        scraper = UniversitaryMasterScrapingService(reader, 'any_url')

        data = scraper.resource_data(reader.read('any_url'))

        expect(data).to(have_keys({
            'name': 'Máster universitario de Máster universitario de Formación del Profesorado de Educación Secundaria Obligatoria y Bachillerato, Formación Profesional y Enseñanza de Idiomas - Especialidad matemáticas(interuniversitario UAB-UB-UOC-UPC)',
            'description': 'Coordinadas por la Universitat Autònoma de Barcelona (UAB), cinco universidades catalanas ofrecen un máster de formación de profesorado que desarrolla las competencias profesionales teóricas y prácticas necesarias para ser un buen profesor de matemáticas. Las clases se realizarán en la Facultad de Matemáticas y Estadística de la Universitat Politècnica de Catalunya (UPC), en el Campus Diagonal Sur (Barcelona).',
            'date_init': '',
            'title': 'Máster universitario de Formación del Profesorado de Educación Secundaria Obligatoria y Bachillerato, Formación Profesional y Enseñanza de Idiomas - Especialidad matemáticas(interuniversitario UAB-UB-UOC-UPC)',
            'ects': '60'
        }))

    @patch('application.scraping_service.ScrapingService.get_resources_urls')
    def test_it_retruns_a_resources_list(self, get_resources_urls):
        html_master01 = ''
        html_master02 = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/master_universitario01.html', 'r') as fin:
            html_master01 = fin.read()
        with open(f'{os.path.dirname(__file__)}/fixtures/master_universitario02.html', 'r') as fin:
            html_master02 = fin.read()
        reader = FakeHtmlReader(htmls=[html_master01, html_master02])
        scraper = UniversitaryMasterScrapingService(reader, 'any_url')
        get_resources_urls.return_value = [
            'http://some_fake_url.com/01',
            'http://some_fake_url.com/02'
        ]

        resources = scraper.scrape()

        expect(len(resources)).to(equal(2))
        expect(resources[0].as_dict()).to(have_keys({
            'type': 'master_universitario',
            'name': 'Máster universitario de Enseñanza y Aprendizaje de Idiomas Mediante la Tecnología',
            'description': 'El máster online de Enseñanza y Aprendizaje de Idiomas Mediante la Tecnología proporciona una base teórica para entender como se aprenden los idiomas mediante la tecnología, pero con una amplia base práctica para aplicar la tecnología con finalidades pedagógicas, para la mejora del aprendizaje de los idiomas, siguiendo criterios conceptuales y metodológicos, dotando el máster de un carácter eminentemente práctico y profesionalizador.',
            'duration': '',
            'title': 'Enseñanza y Aprendizaje de Idiomas Mediante la Tecnología',
            'ects': '60',
            'price': None,
            'url': 'http://some_fake_url.com/01',
            'date_init': '20 octubre 2021'
        }))
        expect(resources[1].as_dict()).to(have_keys({
            'type': 'master_universitario',
            'name': 'Máster universitario de Máster universitario de Formación del Profesorado de Educación Secundaria Obligatoria y Bachillerato, Formación Profesional y Enseñanza de Idiomas - Especialidad matemáticas(interuniversitario UAB-UB-UOC-UPC)',
            'description': 'Coordinadas por la Universitat Autònoma de Barcelona (UAB), cinco universidades catalanas ofrecen un máster de formación de profesorado que desarrolla las competencias profesionales teóricas y prácticas necesarias para ser un buen profesor de matemáticas. Las clases se realizarán en la Facultad de Matemáticas y Estadística de la Universitat Politècnica de Catalunya (UPC), en el Campus Diagonal Sur (Barcelona).',
            'duration': '',
            'title': 'Máster universitario de Formación del Profesorado de Educación Secundaria Obligatoria y Bachillerato, Formación Profesional y Enseñanza de Idiomas - Especialidad matemáticas(interuniversitario UAB-UB-UOC-UPC)',
            'ects': '60',
            'price': None,
            'url': 'http://some_fake_url.com/02',
            'date_init': ''
        }))
