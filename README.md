# UOC Educational Offer web scraping project


## Introducción

El presente proyecto es un ejemplo de webscraping. Su propósito es obtener un dataset en csv con la oferta formativa de la UOC.

Su desarrollo se enmarca dentro de la realización de la práctica 1 de la asignatura _Tipología y ciclo de vida de datos_.

Los pros y contras de la web de la UOC a la hora de aplicar webscraping han sido:

- **PROS**:
    - La estructura de HTML devuelta por el servidor, para cada uno de los distintos tipos de recurso,  incluye toda la información que necesitamos extraer. Es por ello que no he necesitado interptetar el Javascript anexo a la web.
    - La web no tiene medidas de protección contra bots, por lo que no ha sido necesario falsear el `user-agent` ni ninguna otra cabecera HTTP.

- **CONTRAS**:
    - La estrcutura del código HTML es, en general, correcta. Pero está formateado de un modo caótico, lo cual dificulta su análisis y hace necesario pre-formatearlo antes de extraer la información.  [Ejemplo de código fuente mal formateado](https://estudios.uoc.edu/es/masters-posgrados-especializaciones/master-universitario).
    - Los errores _404 Not Found_ no son devueltos con _status code = 404_. El servidor los devuelve como _200 OK_ pero el contenido de la página revela que se trata de un recurso no encontrado.    
    Existen varios recursos, linkados en distintas partes de la web, que llevan a este tipo de página de error [ejemplo](https://estudios.uoc.edu/es/masters-posgrados-especializaciones/diploma-posgrado/artes-humanidades/gestion-marketing-editorial/presentacion)

### Información adicional

Está escrito en Python 3 y hace uso de las librerías [requests](https://requests.readthedocs.io/en/master/) y [lxml](https://lxml.de/) para las tareas de extracción de datos. Los tests están implementados con [Unittest](https://docs.python.org/3/library/unittest.html) y [expects](https://expects.readthedocs.io/en/stable/).

El desarrollo se ha llevado a cabo aplicando TDD y la estructura del mismo sigue los principios de la arquitectura hexagonal (_ports & adapters_).


## Instalación

### Requisitos

Si bien es posible ejecutar el código Pyton sin necesidad de hacer uso de Docker, por sencillez, se recomienda su uso. De este modo podemos prescindir de entornos virtuales y se evitan conflictos con la configuración previa de la máquina anfitrión.

Instale [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) y [docker-compose](https://docs.docker.com/compose/install/).

### Uso

Clone el presente repositorio y ejecute el código Python directamente sobre el contenedor _uocscraper_.


```
git clone git@github.com:serfer2/uoc-web-scraper.git
cd uoc-web-scraper
docker-compose run uocscraper python main.py
```
Docker-compose construirá el contenedor e instalará las dependencias de Python3 en el mismo. El proceso de recogida de datos se iniciará inmediatamente, mostrando los registros de actividad en consola. Este tardará unos minutos en completarse.

Cada nueva ejecución creará un fichero CSV en la carpera `src/store/`, con la marca temporal en el nombre del propio fichero. El contenido de dicho fichero se escribe al completar el proceso.

Ejemplo: `src/store/uoc_educational_offer__2020-11-02_122714.csv`

## Arquitectrura

La arquitectura del presente proyecto sigue los principios de la arquitectura hexagonal (ports and adapters).  
Esto permite articular el código de modo que sea extensible y fácil de mantener. Normalmente las webs son cambiantes, de modo que es conveniente disponer de una base de código fácilmente mantenible.

De esta manera podríamos añadir, por ejemplo, persistencia para almacenar los datos en una BD en lugar de un CSV.  
También podríamos añadir funcionalidad de lectura del HTML con otro tipo de agentes como [Selenium y PhantomJS](https://realpython.com/headless-selenium-testing-with-python-and-phantomjs/). [Ejemplo para obtener el HTML (una vez renderizado al ejecutar JS)](https://stackoverflow.com/questions/52428409/get-fully-rendered-html-using-selenium-webdriver-and-python). Esto sería necesario en caso de analizar una web hecha con algún framework, o librería, javascript como Angular, Vue o React.

El código se distribuye en tres capas principales:

- **Infrastructure**:    
La capa más externa. Controla todo lo relacionado con I/O, como por ejemplo lanzar requests HTTP o escribir el fichero CSV con los datos recogidos. En nuestro caso destacaremos `HtmlReader` y `ResourceCsvRepository`. Es habitual referirse a ellos como _adapters_.

- **Application**:    
Casos de uso, implementados en los servicios de aplicación. Es nuestra _"lógica de negocio"_. Se implementan en las clases `CourseScrapingService`, `MasterScrapingService`, `SeminaryScrapingService`, etc ...    
Puesto que algunas estructuras de la web se repiten para los diferentes tipos de recursos, estos servicios presentan algo de lógica común.    
Para evitar duplicidad de código, la lógica común se implementa en `ScrapingService` y cada uno de los servicios heredan de esta clase y añaden/modifican aquellas funcinalidades propias de ese tipo de recurso.

- **Domain**:    
La capa más interna. Es donde se definen los modelos de datos.    
En este caso solo hay un modelo de datos. Lo he llamado `Resource`.    
Las interfaces de los repositorios (conocidas como _ports_), también irían en esta capa. Pero como solo se requiere un tipo de repositorio (`ResourceCsvRepository`), he optado por no implementarlas.

El **proceso principal** se lanza desde `main.py`.

### Estructura del repositorio

El árbol de directorios del repositorio es como el que sigue:

```
.
├── docker-compose.yml
├── LICENSE
├── Practica_1_Soluciones.pdf
├── README.md
└── src
    ├── application
    │   ├── course_scraping_service.py
    │   ├── diploma_scraping_service.py
    │   ├── idiom_course_scraping_service.py
    │   ├── __init__.py
    │   ├── master_scraping_service.py
    │   ├── scraping_service.py
    │   ├── seminary_scraping_service.py
    │   ├── specialization_scraping_service.py
    │   ├── test
    │   │   ├── fixtures
    │   │   │   ├── curso01.html
    │   │   │   ├── curso02.html
    │   │   │   ├── curso_idiomas_ingles.html
    │   │   │   ├── cursos.html
    │   │   │   ├── cursos_idiomas.html
    │   │   │   ├── cursos_idiomas_ingles.html
    │   │   │   ├── cursos_idiomas_ingles_snippet.html
    │   │   │   ├── cursos_idiomas_seminario.html
    │   │   │   ├── diploma01.html
    │   │   │   ├── diploma02.html
    │   │   │   ├── diplomas-posgrado.html
    │   │   │   ├── especializacion01.html
    │   │   │   ├── especializacion02.html
    │   │   │   ├── especializaciones.html
    │   │   │   ├── master01.html
    │   │   │   ├── master02.html
    │   │   │   ├── masters.html
    │   │   │   ├── masters_universitarios.html
    │   │   │   ├── master_universitario01.html
    │   │   │   ├── master_universitario02.html
    │   │   │   ├── seminarios.html
    │   │   │   ├── seminary01.html
    │   │   │   └── seminary02.html
    │   │   ├── __init__.py
    │   │   ├── test_course_scraping_service.py
    │   │   ├── test_diploma_scraping_service.py
    │   │   ├── test_idiom_course_scraping_service.py
    │   │   ├── test_master_scraping_service.py
    │   │   ├── test_scraping_service.py
    │   │   ├── test_seminary_scraping_service.py
    │   │   ├── test_specialization_scraping_service.py
    │   │   └── test_universitary_master_scraping_service.py
    │   └── universitary_master_scraping_service.py
    ├── Dockerfile
    ├── domain
    │   ├── __init__.py
    │   ├── models
    │   │   ├── __init__.py
    │   │   └── resource.py
    │   └── test
    │       ├── __init__.py
    │       └── test_resource.py
    ├── infrastructure
    │   ├── html_reader.py
    │   ├── __init__.py
    │   ├── resource_csv_repository.py
    │   └── test
    │       ├── __init__.py
    │       └── test_html_reader.py
    ├── main.py  ----------------------->  Poceso principal
    ├── requirements.txt
    ├── shared
    │   ├── settings.py
    │   └── tools.py
    ├── store
    │   └── uoc_educational_offer__2020-11-02_122714.csv ------> ¡¡¡ DATASET obtrenido !!!
    └── test
        ├── fixtures
        │   ├── master01.html
        │   └── masters.html
        ├── __init__.py
        ├── test_main.py
        └── utils.py
```

## Testing


### Ejecución de los tests

Para ejecutar los tests basta con:

```
docker-compose run uocscraper python -m unittest discover
```

### Estrategia de testing

El desarrollo del código ha sido llevado a cabo mediante TDD.

La mayor complejidad para este tipo de proyectos es que no podemos lanzar requests HTTP en la ejecución de los tests, lo cual complica el testeo de la lógica de los servicios de aplicación.    
Para resolver este problema, he usado [_fake_](https://www.softwaretestingmagazine.com/knowledge/unit-testing-fakes-mocks-and-stubs/) para el `HtmlReader`, leyendo los ficheros de fixtures. También he [_mockeado_](https://docs.python.org/3/library/unittest.mock.html) la configuración de `settings.py` en los tests del proceso principal (`main.py`).

## Resultados

De los 7 tipos de recursos que extraidos (_Máster Universitario, Máster, Diploma de posgrado, Especialización, Curso, Curso de Idiomas, Seminario_), he obtenido un total de **422 recursos**, en 383 urls.

El número de recursos obtenidos es mayor que el de urls analizadas. Esto se debe a que las urls de cursos de idiomas contienen varios recursos. Se trata de cursos de un mismo idioma pero para distintos niveles.

[Ver dataset obtenido](https://github.com/serfer2/uoc-web-scraper/tree/main/src/store)

## Autor

Sergio Fernández García.   
@serfer2  
serfer2[at]protonmail.com





























