import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.corte_caja import CorteCaja  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server import util


def obtener_corte_caja(reunion_id):  # noqa: E501
    """Obtener el corte de caja

    Devuelve el arqueo de caja chica con la verificación de consistencia &#x60;FondoInicial + CobrosEfectivo − Egresos &#x3D; Total&#x60; (E1).  # noqa: E501

    :param reunion_id: Identificador interno (UUID) de la reunión mensual.
    :type reunion_id: str
    :type reunion_id: str

    :rtype: Union[CorteCaja, Tuple[CorteCaja, int], Tuple[CorteCaja, int, Dict[str, str]]
    """
    return 'do some magic!'
