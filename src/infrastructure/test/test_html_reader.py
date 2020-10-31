from unittest import TestCase

from expects import (
    be_none,
    equal,
    expect
)

from infrastructure import HtmlReader
from test.utils import FakeHttpClient


class HtmlReaderTestCase(TestCase):

    def test_it_returns_none_when_status_code_not_200_OK(self):
        http_client = FakeHttpClient(status_code=400)

        html = HtmlReader(http_client).read(url='http://whatever.com')

        expect(html).to(be_none)

    def test_it_returns_readed_html_when_status_code_is_200_OK(self):
        http_client = FakeHttpClient(status_code=200, content='<h1>something</h1>')

        html = HtmlReader(http_client).read(url='http://whatever.com')

        expect(html).to(equal('<h1>something</h1>'))

    def test_it_cleans_tabs_and_spaces_from_html_lines(self):
        content = '''\
            <div>
                <p>hello</p>  
                <p>world</p> 
            </div>            
        '''
        http_client = FakeHttpClient(200, content)

        html = HtmlReader(http_client).read(url='http://whatever.com')

        expect(html).to(equal('<div><p>hello</p><p>world</p></div>'))
