import csv


class ResourceCsvRepository:

    def __init__(self, filepath):
        self.__filepath = filepath

        with open(self.__filepath, 'w') as csv_file:
            csv_file.write(self._header())

    def persist(self, resource):
        with open(self.__filepath, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(resource.as_list())

    def _header(self):
        return 'type;name;description;duration;title;ects;price;url;date_init\n'
