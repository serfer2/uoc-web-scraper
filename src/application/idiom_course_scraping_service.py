import lxml.etree
import lxml.html

from application.scraping_service import ScrapingService
from domain.models import Resource
from shared.tools import clean_html


class IdiomCourseScrapingService(ScrapingService):

    def __init__(self, *args, **kwargs):
        super(IdiomCourseScrapingService, self).__init__(*args, **kwargs)

        self._resource_type = Resource.TYPE_DIPLOMA_POSGRADO
        self._urls_xpath = '//a[@class="card-absolute-link"]/@href'

    def scrape(self):

        # Cada url te lleva a una página que puede tener
        # varios (idiomas) o solo uno (seminarios).
        # Los seminarios los extraemos de tirón.
        # Los de idiomas, tenemos que iterar las tarjetas
        # para sacarlos todos.

        resources = []

        for url in self.get_resources_urls():
            self.delay()

            html = self._reader.read(url)

            if self.is_seminary_web(html):
                data = self.x_uoc_resource_data(html)
                data.update({
                    'type': Resource.TYPE_SEMINARIO,
                    'url': url
                })
                resources.append(Resource(**data))

            else:
                for snippet in self.idiom_courses_html_snippets(html):
                    course_data = self.idiom_course_resource_data(snippet)
                    course_data.update({
                        'type': Resource.TYPE_CURSO_IDIOMAS,
                        'url': url
                    })
                    resources.append(Resource(**course_data))

        return resources

    def is_seminary_web(self, html):
        doc = lxml.html.fromstring(html)
        h1 = doc.xpath('//h1[@property="name"]')
        if h1:
            return 'seminario' in h1[0].text_content().strip().lower()

        return False

    def idiom_courses_html_snippets(self, html):
        doc = lxml.html.fromstring(html)

        snippets = [lxml.etree.tostring(snippet) for snippet in doc.xpath('//div[@id="idiomas-producto"]//div[@class="col-md-3"]')]

        return [clean_html(snippet.decode('utf-8')) for snippet in snippets]

    def idiom_course_resource_data(self, html):
        doc = lxml.html.fromstring(html)

        name = doc.xpath('//h3')[0].text_content().strip()
        desc = doc.xpath('//div[@class="h5"]')[0].text_content().strip()
        duration = doc.xpath('//h5')[0].text_content().strip().split(':')[-1].strip()
        date_init = doc.xpath('//div[@class="col-md-6"]')[0].text_content().strip().split(':')[-1].strip()
        price = doc.xpath('//div[@class="col-md-6 text-right"]')[0].text_content().strip()
        ects = doc.get('data-credits', None)

        return {
            'name': name,
            'description': desc,
            'duration': duration,
            'date_init': date_init,
            'price': price,
            'ects': ects
        }
