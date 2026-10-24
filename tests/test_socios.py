"""Pruebas de la historia HU-01 (registro y mantenimiento de socios).

Cubre los criterios de aceptación CA-01.1 (límite de 69 socios), CA-01.2 (unicidad
de identificación) y CA-01.3 (baja lógica sin borrado físico).
"""

import pytest

import reglas


def test_registro_exitoso_de_socio(conn):
    """CA-01.1: un socio nuevo queda ACTIVO y se cuenta en el padrón."""
    socio = reglas.crear_socio(conn, "1002345678", "Socio Nuevo", 3)
    assert socio["estado"] == "ACTIVO"
    assert socio["grupoCafe"] == 3
    assert len(reglas.listar_socios(conn)) == 1


def test_rechazo_al_exceder_el_limite_de_69_socios(conn):
    """CA-01.1 / R6: no se admite el socio 70."""
    for i in range(reglas.MAX_SOCIOS):
        reglas.crear_socio(conn, f"17000000{i:02d}", f"Socio {i}", (i % 10) + 1)
    with pytest.raises(reglas.LimiteSocios):
        reglas.crear_socio(conn, "1799999999", "Socio 70", 1)


def test_rechazo_de_identificacion_duplicada(conn):
    """CA-01.2: la restricción UNIQUE de la base impide cédulas repetidas."""
    reglas.crear_socio(conn, "0401234567", "Carlos Andrade", 4)
    with pytest.raises(reglas.IdentificacionDuplicada):
        reglas.crear_socio(conn, "0401234567", "Otro Nombre", 5)


def test_baja_logica_conserva_el_registro(conn, socio):
    """CA-01.3: el retiro cambia el estado pero no borra el historial."""
    actualizado = reglas.inactivar_socio(conn, socio["socioId"])
    assert actualizado["estado"] == "INACTIVO"
    assert conn.execute("SELECT COUNT(*) AS n FROM socios").fetchone()["n"] == 1
