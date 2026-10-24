import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2,<=2.14.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="API del Sistema de Gestión y Auditoría — Asociación 31 de Enero",
    author_email="",
    url="",
    keywords=["OpenAPI", "API del Sistema de Gestión y Auditoría — Asociación 31 de Enero"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    Contrato de la API local del Sistema de Gestión Automatizada y Auditoría de la Asociación “31 de Enero Narciza de Jesús”. El servicio se ejecuta en una sola PC, monousuario y 100 % offline (R4).  Trazabilidad con el Dossier de Arquitectura v0.1.0: - Escenarios E1 (consistencia financiera), E2 (seguridad), E5 (desempeño), E6 (integridad). - Drivers D1, D2, D4, D5 y D6. - ADR-001 (SQLite local), ADR-002 (reglas financieras centralizadas), ADR-003 (monolito local).  Minimización de datos (R1, LOPDP): la cédula es un dato personal y **nunca** se devuelve en las respuestas. Los recursos se identifican con un &#x60;socioId&#x60; sustituto (UUID interno). El único campo con dato personal es &#x60;identificacion&#x60;, marcado &#x60;writeOnly&#x60; en el alta de socios. 
    """
)

