import unittest

from flask import json

from openapi_server.models.comprobante import Comprobante  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.estado_cuenta import EstadoCuenta  # noqa: E501
from openapi_server.models.nuevo_socio import NuevoSocio  # noqa: E501
from openapi_server.models.socio import Socio  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSociosController(BaseTestCase):
    """SociosController integration test stubs"""

    def test_consultar_estado_cuenta(self):
        """Test case for consultar_estado_cuenta

        Consultar el estado de cuenta
        """
        query_string = [('periodo', '2026-10')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/socios/{socio_id}/estado-cuenta'.format(socio_id=UUID('6f1c2b8e-0a3d-4c7e-9b2a-1d5e8f3a7c90')),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_crear_socio(self):
        """Test case for crear_socio

        Registrar un socio
        """
        nuevo_socio = {"nombres":"Juan Pérez","grupoCafe":3,"identificacion":"1002345678"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/socios',
            method='POST',
            headers=headers,
            data=json.dumps(nuevo_socio),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_listar_socios(self):
        """Test case for listar_socios

        Listar socios
        """
        query_string = [('estado', 'ACTIVO')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/socios',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_comprobante(self):
        """Test case for obtener_comprobante

        Generar el comprobante de pago
        """
        query_string = [('periodo', '2026-10')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/socios/{socio_id}/comprobante'.format(socio_id=UUID('6f1c2b8e-0a3d-4c7e-9b2a-1d5e8f3a7c90')),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_socio(self):
        """Test case for obtener_socio

        Consultar un socio
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/socios/{socio_id}'.format(socio_id=UUID('6f1c2b8e-0a3d-4c7e-9b2a-1d5e8f3a7c90')),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
