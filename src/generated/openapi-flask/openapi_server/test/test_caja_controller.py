import unittest

from flask import json

from openapi_server.models.corte_caja import CorteCaja  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCajaController(BaseTestCase):
    """CajaController integration test stubs"""

    def test_obtener_corte_caja(self):
        """Test case for obtener_corte_caja

        Obtener el corte de caja
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/reuniones/{reunion_id}/caja'.format(reunion_id=UUID('2a7d9c14-5b6e-4f38-8a1b-9c0d2e4f6a11')),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
