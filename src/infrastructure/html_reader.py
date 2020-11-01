import requests

from shared.tools import clean_html


class HtmlReader:

    def __init__(self, http_client=None):
        self.__http_client = http_client or requests

    def read(self, url):
        try:
            response = self.__http_client.get(url)
            if response.status_code == 200:
                return clean_html(str(response.text))
        except Exception:
            pass

        return None
