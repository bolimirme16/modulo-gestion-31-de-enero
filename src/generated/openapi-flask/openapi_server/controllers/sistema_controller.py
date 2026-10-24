import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.integridad import Integridad  # noqa: E501
from openapi_server.models.respaldo import Respaldo  # noqa: E501
from openapi_server import util


def crear_respaldo():  # noqa: E501
    """Crear un respaldo de la base de datos

    Copia el archivo &#x60;asociacion.db&#x60; a la unidad USB con marca de tiempo. La medida de E6 exige que el respaldo se complete en ≤ 5 s.  # noqa: E501


    :rtype: Union[Respaldo, Tuple[Respaldo, int], Tuple[Respaldo, int, Dict[str, str]]
    """
    return 'do some magic!'


def verificar_integridad():  # noqa: E501
    """Verificar la integridad de la base de datos

    Ejecuta los 9 chequeos de integridad de SQLite y devuelve el resultado. La medida de E6 exige 9 de 9 chequeos correctos.  # noqa: E501


    :rtype: Union[Integridad, Tuple[Integridad, int], Tuple[Integridad, int, Dict[str, str]]
    """
    return 'do some magic!'
