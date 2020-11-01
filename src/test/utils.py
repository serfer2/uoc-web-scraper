from shared.tools import clean_html


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

    def __init__(self, htmls=None):
        self.__number_of_reads = 0
        self.__htmls = htmls or []

    def read(self, url):
        response = clean_html(self.__htmls[self.__number_of_reads])
        self.__number_of_reads += 1
        return response


class FakeRepository:

    def __init__(self):
        self.__resources = []

    def persist(self, resource):
        self.__resources.append(resource)

    def list(self):
        return self.__resources
