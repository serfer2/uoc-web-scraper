import importlib
import os
import sys
from datetime import datetime

from shared.settings import (
    CSV_PREFIX,
    resource_types_configuration
)
from infrastructure import ResourceCsvRepository


def main():

    destination_file = _csv_filepath(CSV_PREFIX)
    repository = ResourceCsvRepository(destination_file)

    for resource_type, config in resource_types_configuration.items():
        print(f'------ Scraping {resource_type} ...')

        scraping_service_class = _class(path=config['scraper'])
        reader_class = _class(path=config['reader'])

        scraping_service = scraping_service_class(
            reader=reader_class(),
            initial_url=config['initial_url']
        )

        resources = scraping_service.scrape()

    return 0


def _class(path):
    class_name_separator = path.rfind('.')
    module = path[:class_name_separator]
    class_name = path[class_name_separator + 1:]

    return getattr(importlib.import_module(module), class_name)


def _csv_filepath(csv_prefix):
    path = os.environ.get('STORE_PATH', 'store/')
    filename = f"{csv_prefix}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv"

    return os.path.join(path, f'/{filename}')


if __name__ == '__main__':
    sys.exit(main())
