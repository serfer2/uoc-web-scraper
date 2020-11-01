import os
from unittest import TestCase
from unittest.mock import patch

from expects import (
    be_false,
    be_true,
    equal,
    expect,
    have_keys
)

from application import IdiomCourseScrapingService
from test.utils import FakeHtmlReader


class IdiomCourseScrapingServiceTestCase(TestCase):

    def test_it_gets_all_idiom_courses_detail_urls(self):
        html = ''
        # 10 courses
        filepath = f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas.html'
        with open(filepath, 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        url = 'https://x.uoc.edu/es/que-quieres-estudiar/cursos-idiomas/?ac=2535&src=2535'
        scraper = IdiomCourseScrapingService(reader, url)

        urls = scraper.get_resources_urls()

        expect(len(urls)).to(equal(10))
        expect(urls[0]).to(equal('https://x.uoc.edu/es/cursos-idiomas/curso-ingles-online/'))
        expect(urls[9]).to(equal('https://x.uoc.edu/es/seminarios-desarrollo-continuo/writing-skills-for-work-2/'))

    def test_it_recognizes_if_detail_page_is_for_seminary(self):
        html_seminary = ''
        html_idioms = ''
        filepath = f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas_seminario.html'
        with open(filepath, 'r') as fin:
            html_seminary = fin.read()
        filepath = f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas_ingles.html'
        with open(filepath, 'r') as fin:
            html_idioms = fin.read()

        scraper = IdiomCourseScrapingService(FakeHtmlReader(), 'something')

        expect(scraper.is_seminary_web(html_seminary)).to(be_true)
        expect(scraper.is_seminary_web(html_idioms)).to(be_false)

    def test_it_extracts_eminary_data_from_detail_page(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas_seminario.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        scraper = IdiomCourseScrapingService(reader, 'any_url')

        data = scraper.x_uoc_resource_data(reader.read('any_url'))

        expect(data).to(have_keys({
            'name': 'Speaking Skills for Work',
            'description': 'Curso multinivel totalmente en línea impartido en inglés. Se dirige a personas que quieran mejorar su capacidad de expresarse oralmente en inglés en un entorno profesional. El curso está diseñado para que los estudiantes le dediquen un total de 25 horas, aproximadamente, a lo largo de un mes. Hay que contar con un ordenador con conexión a internet de banda ancha, así como unos auriculares con micrófono y una cámara web. Este seminario se impartirá dentro del campus del Centro de Idiomas Modernos de la UOC.',
            'duration': '1 mes',
            'date_init': '16 Junio',
            'price': '140€',
            'title': 'Certificado de aprovechamiento de la UOC'
        }))

    def test_it_gets_html_snippets_for_idiom_courses(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas_ingles.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        first_snippet_html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas_ingles_snippet.html', 'r') as fin:
            first_snippet_html = fin.read()
        scraper = IdiomCourseScrapingService(reader, 'any_url')

        snippets = scraper.idiom_courses_html_snippets(html)

        expect(len(snippets)).to(equal(19))
        expect(snippets[0]).to(equal(first_snippet_html))

    def test_it_extracts_idiom_course_resource_data_from_html_snippet(self):
        html = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas_ingles_snippet.html', 'r') as fin:
            html = fin.read()
        reader = FakeHtmlReader(htmls=[html])
        scraper = IdiomCourseScrapingService(reader, 'any_url')

        data = scraper.idiom_course_resource_data(reader.read('any_url'))

        expect(data).to(have_keys({
            'name': 'Inglés A1.1',
            'description': 'Nivel: A1 - Beginner',
            'duration': 'Semestral',
            'date_init': '17-02-2021',
            'price': '265€',
            'ects': '4'
        }))

    @patch('application.scraping_service.ScrapingService.get_resources_urls')
    def test_it_retruns_a_resources_list_by_mixing_seminaries_and_idiom_courses(self, get_resources_urls):
        html_idiom_courses = ''
        html_seminary = ''
        with open(f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas_ingles.html', 'r') as fin:
            html_idiom_courses = fin.read()
        with open(f'{os.path.dirname(__file__)}/fixtures/cursos_idiomas_seminario.html', 'r') as fin:
            html_seminary = fin.read()
        reader = FakeHtmlReader(htmls=[html_idiom_courses, html_seminary])
        scraper = IdiomCourseScrapingService(reader, 'any_url')
        get_resources_urls.return_value = [
            'http://some_fake_url.com/01',
            'http://some_fake_url.com/02'
        ]

        resources = scraper.scrape()

        expect(len(resources)).to(equal(20))
        expect(resources[0].as_dict()).to(have_keys({
            'type': 'curso_de_idiomas',
            'name': 'Inglés A1.1',
            'description': 'Nivel: A1 - Beginner',
            'duration': 'Semestral',
            'title': '',
            'ects': '4',
            'price': '265€',
            'url': 'http://some_fake_url.com/01',
            'date_init': '17-02-2021'
        }))
        expect(resources[19].as_dict()).to(have_keys({
            'type': 'seminario',
            'name': 'Speaking Skills for Work',
            'description': 'Curso multinivel totalmente en línea impartido en inglés. Se dirige a personas que quieran mejorar su capacidad de expresarse oralmente en inglés en un entorno profesional. El curso está diseñado para que los estudiantes le dediquen un total de 25 horas, aproximadamente, a lo largo de un mes. Hay que contar con un ordenador con conexión a internet de banda ancha, así como unos auriculares con micrófono y una cámara web. Este seminario se impartirá dentro del campus del Centro de Idiomas Modernos de la UOC.',
            'duration': '1 mes',
            'title': 'Certificado de aprovechamiento de la UOC',
            'ects': None,
            'price': '140€',
            'url': 'http://some_fake_url.com/02',
            'date_init': '16 Junio'
        }))
