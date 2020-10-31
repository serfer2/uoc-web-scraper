import requests


class HtmlReader:

    def __init__(self, http_client=None):
        self.__http_client = http_client or requests

    def read(self, url):
        try:
            response = self.__http_client.get(url)
            if response.status_code == 200:
                return self.__minimize_html(str(response.text))
        except Exception:
            pass

        return None

    def __minimize_html(self, text):
        # Clean HTML text format
        return text.replace('\n', '').replace('\t', '').replace('      ', ' ').replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace('  ', ' ').replace('> <', '><').strip()
