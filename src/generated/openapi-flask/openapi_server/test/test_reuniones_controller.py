import unittest

from flask import json

from openapi_server.models.asistencia import Asistencia  # noqa: E501
from openapi_server.models.cierre import Cierre  # noqa: E501
from openapi_server.models.cobro_cafe import CobroCafe  # noqa: E501
from openapi_server.models.cuota import Cuota  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.registro_asistencia import RegistroAsistencia  # noqa: E501
from openapi_server.models.registro_cafe import RegistroCafe  # noqa: E501
from openapi_server.models.registro_cuota import RegistroCuota  # noqa: E501
from openapi_server.test import BaseTestCase


class TestReunionesController(BaseTestCase):
    """ReunionesController integration test stubs"""

    def test_cerrar_reunion(self):
        """Test case for cerrar_reunion

        Cerrar la reunión (bloqueante)
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/reuniones/{reunion_id}/cierre'.format(reunion_id=UUID('2a7d9c14-5b6e-4f38-8a1b-9c0d2e4f6a11')),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_registrar_asistencia(self):
        """Test case for registrar_asistencia

        Registrar asistencia de un socio
        """
        registro_asistencia = {"socioId":"6f1c2b8e-0a3d-4c7e-9b2a-1d5e8f3a7c90","estado":"AUSENTE"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/reuniones/{reunion_id}/asistencia'.format(reunion_id=UUID('2a7d9c14-5b6e-4f38-8a1b-9c0d2e4f6a11')),
            method='POST',
            headers=headers,
            data=json.dumps(registro_asistencia),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_registrar_cafe(self):
        """Test case for registrar_cafe

        Registrar el cobro del servicio de café
        """
        registro_cafe = {"socioId":"6f1c2b8e-0a3d-4c7e-9b2a-1d5e8f3a7c90","grupoTurno":4}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/reuniones/{reunion_id}/cafe'.format(reunion_id=UUID('2a7d9c14-5b6e-4f38-8a1b-9c0d2e4f6a11')),
            method='POST',
            headers=headers,
            data=json.dumps(registro_cafe),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_registrar_cuota(self):
        """Test case for registrar_cuota

        Registrar el pago de la cuota mensual
        """
        registro_cuota = {"socioId":"6f1c2b8e-0a3d-4c7e-9b2a-1d5e8f3a7c90","periodo":"2026-10","monto":10.0}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/reuniones/{reunion_id}/cuotas'.format(reunion_id=UUID('2a7d9c14-5b6e-4f38-8a1b-9c0d2e4f6a11')),
            method='POST',
            headers=headers,
            data=json.dumps(registro_cuota),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
