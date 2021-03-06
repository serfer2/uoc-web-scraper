class Resource:

    TYPE_MASTER_UNIVERSITARIO = 'master_universitario'
    TYPE_MASTER = 'master'
    TYPE_DIPLOMA_POSGRADO = 'diploma_de_posgrado'
    TYPE_ESPECIALIZACION = 'especializacion'
    TYPE_CURSO = 'curso'
    TYPE_CURSO_IDIOMAS = 'curso_de_idiomas'
    TYPE_SEMINARIO = 'seminario'
    TYPES = {
        TYPE_MASTER_UNIVERSITARIO: 'Máster universitario',
        TYPE_MASTER: 'Máster',
        TYPE_DIPLOMA_POSGRADO: 'Diploma de posgrado',
        TYPE_ESPECIALIZACION: 'Especialización',
        TYPE_CURSO: 'Curso',
        TYPE_CURSO_IDIOMAS: 'Curso de idiomas',
        TYPE_SEMINARIO: 'Seminario'
    }

    def __init__(self, type, name, description='', duration='', title='', ects=None, price=None, url='', date_init=''):
        self.__type = self.__validate_type(type)
        self.__name = self.__validate_name(name)
        self.__description = description
        self.__duration = duration
        self.__title = title
        self.__ects = ects
        self.__price = price
        self.__url = url
        self.__date_init = date_init

    def __str__(self):
        return f'[{self.__type}] {self.__name}'

    def as_dict(self):
        return {
            'type': self.__type,
            'name': self.__name,
            'description': self.__description,
            'duration': self.__duration,
            'title': self.__title,
            'ects': self.__ects,
            'price': self.__price,
            'url': self.__url,
            'date_init': self.__date_init
        }

    def as_list(self):
        return [
            self.__type,
            self.__name,
            self.__description,
            self.__duration,
            self.__title,
            self.__ects,
            self.__price,
            self.__url,
            self.__date_init
        ]

    def __validate_type(self, type):
        if not type or type not in self.TYPES:
            raise ValueError('Wrong resource type')
        return type

    def __validate_name(self, name):
        name = name.strip()
        if not name:
            raise ValueError('Wrong resource name')
        return name
