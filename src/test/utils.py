class FakeHttpResponse:

    def __init__(self, status_code, content):
        self.status_code = status_code
        self.text = content


class FakeHttpClient:

    def __init__(self, status_code=200, content=''):
        self.__status_code = status_code
        self.__content = content

    def get(self, url):
        return FakeHttpResponse(self.__status_code, self.__content)


class FakeHtmlReader:
    
    def __init__(self, html=''):
        self.__html = html

    def read(self, url):
        return self.__html
