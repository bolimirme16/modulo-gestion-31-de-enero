"""Fixtures compartidas por las pruebas del esqueleto ejecutable."""

import pytest

import reglas


@pytest.fixture
def conn():
    """Base de datos en memoria con el esquema aplicado."""
    return reglas.conectar(":memory:")


@pytest.fixture
def socio(conn):
    """Socio de prueba (nunca se usan cédulas ni nombres reales)."""
    return reglas.crear_socio(conn, "0401234567", "Socio de prueba", 4)


@pytest.fixture
def reunion(conn):
    """Reunión mensual abierta con fondo de caja de $100."""
    return reglas.abrir_reunion(conn, "2026-10-31", grupo_turno=4, fondo_inicial=100.0)


@pytest.fixture
def servicio():
    """Aplicación Flask con su propio cliente de prueba y su conexión."""
    from app import crear_app

    app = crear_app(":memory:")
    client = app.test_client()
    return app, client, app.config["DB"]
