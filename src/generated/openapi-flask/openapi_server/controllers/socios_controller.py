import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.comprobante import Comprobante  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.estado_cuenta import EstadoCuenta  # noqa: E501
from openapi_server.models.nuevo_socio import NuevoSocio  # noqa: E501
from openapi_server.models.socio import Socio  # noqa: E501
from openapi_server import util


def consultar_estado_cuenta(socio_id, periodo=None):  # noqa: E501
    """Consultar el estado de cuenta

    Devuelve los cargos (cuota, multa, café) y abonos del socio, con el saldo calculado. Respalda el escenario E5 (consulta en la cola final).  # noqa: E501

    :param socio_id: Identificador interno (UUID) del socio.
    :type socio_id: str
    :type socio_id: str
    :param periodo: Período mensual en formato AAAA-MM.
    :type periodo: str

    :rtype: Union[EstadoCuenta, Tuple[EstadoCuenta, int], Tuple[EstadoCuenta, int, Dict[str, str]]
    """
    return 'do some magic!'


def crear_socio(body):  # noqa: E501
    """Registrar un socio

    Da de alta un socio. Aplica R6 (máximo 69 socios) y la unicidad de la identificación. La cédula enviada en &#x60;identificacion&#x60; no se devuelve.  # noqa: E501

    :param nuevo_socio: 
    :type nuevo_socio: dict | bytes

    :rtype: Union[Socio, Tuple[Socio, int], Tuple[Socio, int, Dict[str, str]]
    """
    nuevo_socio = body
    if flask.request.is_json:
        nuevo_socio = NuevoSocio.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def listar_socios(estado=None):  # noqa: E501
    """Listar socios

    Devuelve el padrón de socios. No expone cédulas ni datos personales. # noqa: E501

    :param estado: Filtra por estado del socio.
    :type estado: str

    :rtype: Union[List[Socio], Tuple[List[Socio], int], Tuple[List[Socio], int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_comprobante(socio_id, periodo):  # noqa: E501
    """Generar el comprobante de pago

    Devuelve el detalle imprimible del comprobante (logo, firma y sello se componen en la capa de presentación). Respalda el driver D6.  # noqa: E501

    :param socio_id: Identificador interno (UUID) del socio.
    :type socio_id: str
    :type socio_id: str
    :param periodo: Período mensual del comprobante.
    :type periodo: str

    :rtype: Union[Comprobante, Tuple[Comprobante, int], Tuple[Comprobante, int, Dict[str, str]]
    """
    return 'do some magic!'


def obtener_socio(socio_id):  # noqa: E501
    """Consultar un socio

    Devuelve la ficha de un socio por su identificador interno. # noqa: E501

    :param socio_id: Identificador interno (UUID) del socio.
    :type socio_id: str
    :type socio_id: str

    :rtype: Union[Socio, Tuple[Socio, int], Tuple[Socio, int, Dict[str, str]]
    """
    return 'do some magic!'
