
CSV_PREFIX = 'uoc_educational_offer_'

repository_class = 'infrastructure.ResourceCsvRepository'

resource_types_configuration = {
    'Máster Universitario': {
        'scraper': 'application.UniversitaryMasterScrapingService',
        'reader': 'infrastructure.HtmlReader',
        'initial_url': 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/master-universitario'
    },
    'Máster': {
        'scraper': 'application.MasterScrapingService',
        'reader': 'infrastructure.HtmlReader',
        'initial_url': 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/master'
    },
    'Diploma de Posgrado': {
        'scraper': 'application.DiplomaScrapingService',
        'reader': 'infrastructure.HtmlReader',
        'initial_url': 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/diploma-posgrado'
    },
    'Especializalción': {
        'scraper': 'application.SpecializationScrapingService',
        'reader': 'infrastructure.HtmlReader',
        'initial_url': 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/especializacion'
    },
    'Curso': {
        'scraper': 'application.CourseScrapingService',
        'reader': 'infrastructure.HtmlReader',
        'initial_url': 'https://estudios.uoc.edu/es/masters-posgrados-especializaciones/curso'
    },
    'Curso de Idiomas': {
        'scraper': 'application.IdiomCourseScrapingService',
        'reader': 'infrastructure.HtmlReader',
        'initial_url': 'https://x.uoc.edu/es/que-quieres-estudiar/cursos-idiomas/'
    },
    'Seminario': {
        'scraper': 'application.SeminaryScrapingService',
        'reader': 'infrastructure.HtmlReader',
        'initial_url': 'https://x.uoc.edu/es/que-quieres-estudiar/seminarios/'
    }
}
