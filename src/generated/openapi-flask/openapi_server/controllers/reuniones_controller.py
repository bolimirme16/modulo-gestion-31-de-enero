import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.asistencia import Asistencia  # noqa: E501
from openapi_server.models.cierre import Cierre  # noqa: E501
from openapi_server.models.cobro_cafe import CobroCafe  # noqa: E501
from openapi_server.models.cuota import Cuota  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.registro_asistencia import RegistroAsistencia  # noqa: E501
from openapi_server.models.registro_cafe import RegistroCafe  # noqa: E501
from openapi_server.models.registro_cuota import RegistroCuota  # noqa: E501
from openapi_server import util


def cerrar_reunion(reunion_id):  # noqa: E501
    """Cerrar la reunión (bloqueante)

    Consolida los totales y congela la reunión. Una vez cerrada, cualquier cambio se rechaza (ADR-002). La operación se completa en ≤ 2 s (E1).  # noqa: E501

    :param reunion_id: Identificador interno (UUID) de la reunión mensual.
    :type reunion_id: str
    :type reunion_id: str

    :rtype: Union[Cierre, Tuple[Cierre, int], Tuple[Cierre, int, Dict[str, str]]
    """
    return 'do some magic!'


def registrar_asistencia(reunion_id, body):  # noqa: E501
    """Registrar asistencia de un socio

    Registra la asistencia del socio en la reunión. Si el estado es &#x60;AUSENTE&#x60; genera la multa fija de $5,00 (E1). No admite dos registros del mismo socio en la misma reunión (R2).  # noqa: E501

    :param reunion_id: Identificador interno (UUID) de la reunión mensual.
    :type reunion_id: str
    :type reunion_id: str
    :param registro_asistencia: 
    :type registro_asistencia: dict | bytes

    :rtype: Union[Asistencia, Tuple[Asistencia, int], Tuple[Asistencia, int, Dict[str, str]]
    """
    registro_asistencia = body
    if flask.request.is_json:
        registro_asistencia = RegistroAsistencia.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def registrar_cafe(reunion_id, body):  # noqa: E501
    """Registrar el cobro del servicio de café

    Cobra el café según el grupo de rotación: $1,50 si el socio pertenece al grupo de turno de la reunión y $3,00 en caso contrario (E1, ADR-002). Solo admite un cobro por socio y reunión (R2).  # noqa: E501

    :param reunion_id: Identificador interno (UUID) de la reunión mensual.
    :type reunion_id: str
    :type reunion_id: str
    :param registro_cafe: 
    :type registro_cafe: dict | bytes

    :rtype: Union[CobroCafe, Tuple[CobroCafe, int], Tuple[CobroCafe, int, Dict[str, str]]
    """
    registro_cafe = body
    if flask.request.is_json:
        registro_cafe = RegistroCafe.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def registrar_cuota(reunion_id, body):  # noqa: E501
    """Registrar el pago de la cuota mensual

    Registra la cuota mensual de $25,00 y los abonos parciales. Recalcula el saldo como &#x60;Cuota − Suma(abonos)&#x60; y rechaza el sobrepago (E1, ADR-002).  # noqa: E501

    :param reunion_id: Identificador interno (UUID) de la reunión mensual.
    :type reunion_id: str
    :type reunion_id: str
    :param registro_cuota: 
    :type registro_cuota: dict | bytes

    :rtype: Union[Cuota, Tuple[Cuota, int], Tuple[Cuota, int, Dict[str, str]]
    """
    registro_cuota = body
    if flask.request.is_json:
        registro_cuota = RegistroCuota.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'
