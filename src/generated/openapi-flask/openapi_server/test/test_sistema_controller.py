import unittest

from flask import json

from openapi_server.models.integridad import Integridad  # noqa: E501
from openapi_server.models.respaldo import Respaldo  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSistemaController(BaseTestCase):
    """SistemaController integration test stubs"""

    def test_crear_respaldo(self):
        """Test case for crear_respaldo

        Crear un respaldo de la base de datos
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/sistema/respaldo',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_verificar_integridad(self):
        """Test case for verificar_integridad

        Verificar la integridad de la base de datos
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/sistema/integridad',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
