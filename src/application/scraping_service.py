class ScrapingService:

    def __init__(self, reader, repository, initial_url):
        self.__reader = reader
        self.__repository = repository
        self.__initial_url = initial_url
