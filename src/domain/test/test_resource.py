from unittest import TestCase

from expects import (
    equal,
    expect,
    have_keys
)

from domain.models import Resource


class ResourceTestCase(TestCase):

    def setUp(self):
        self.correct_data = {
            'type': Resource.TYPE_MASTER,
            'name': 'How to fly a X-Wing',
            'description': 'Learn to fly a X-Wing and follow the resistance!',
            'duration': '2 weeks',
            'title': 'A beautiful diploma',
            'ects': 20,
            'price': '100 €',
            'url': 'http://followtheresistance.com',
            'date_init': '17 febrero 2021'
        }

    def test_it_raises_exception_when_type_value_is_unknown(self):
        wrong_data = self.correct_data.copy()
        wrong_data.update({'type': 'something wrong'})

        with self.assertRaises(ValueError):
            Resource(**wrong_data)

    def test_raises_exception_when_name_is_empty_or_blank(self):
        wrong_data = self.correct_data.copy()
        wrong_data.update({'name': '   '})

        with self.assertRaises(ValueError):
            Resource(**wrong_data)

    def test_it_exports_as_dict(self):
        resource = Resource(**self.correct_data)

        resource_dict = resource.as_dict()

        expect(resource_dict).to(have_keys(self.correct_data))

    def test_it_exports_as_list(self):
        resource = Resource(**self.correct_data)

        resource_list = resource.as_list()

        expect(resource_list).to(equal([
            Resource.TYPE_MASTER,
            'How to fly a X-Wing',
            'Learn to fly a X-Wing and follow the resistance!',
            '2 weeks',
            'A beautiful diploma',
            20,
            '100 €',
            'http://followtheresistance.com',
            '17 febrero 2021'
        ]))
