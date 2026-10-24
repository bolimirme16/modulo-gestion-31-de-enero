"""Pruebas de la historia HU-02 (asistencia y multas por inasistencia).

Cubre CA-02.1 (multa exacta de $5,00), CA-02.2 (un registro por socio y reunión) y
CA-02.3 (bloqueo del cierre). Escenario E1 (consistencia financiera).
"""

import pytest

import reglas


@pytest.mark.parametrize(
    ("estado", "multa_esperada"),
    [("PRESENTE", 0.00), ("AUSENTE", 5.00), ("JUSTIFICADO", 0.00)],
)
def test_multa_segun_estado_de_asistencia(conn, socio, reunion, estado, multa_esperada):
    """CA-02.1: solo la inasistencia no justificada genera la multa de $5,00."""
    registro = reglas.registrar_asistencia(conn, reunion["reunionId"], socio["socioId"], estado)
    assert registro["multa"] == multa_esperada


def test_rechazo_de_doble_registro_en_la_misma_reunion(conn, socio, reunion):
    """CA-02.2: un segundo registro del mismo socio devuelve conflicto."""
    reglas.registrar_asistencia(conn, reunion["reunionId"], socio["socioId"], "AUSENTE")
    with pytest.raises(reglas.RegistroDuplicado):
        reglas.registrar_asistencia(conn, reunion["reunionId"], socio["socioId"], "PRESENTE")


def test_no_se_puede_registrar_asistencia_en_reunion_cerrada(conn, socio, reunion):
    """CA-02.3 / ADR-002: una reunión cerrada rechaza cambios."""
    reglas.cerrar_reunion(conn, reunion["reunionId"])
    with pytest.raises(reglas.ReunionCerrada):
        reglas.registrar_asistencia(conn, reunion["reunionId"], socio["socioId"], "AUSENTE")


def test_la_multa_se_refleja_en_el_estado_de_cuenta(conn, socio, reunion):
    """CA-02.1: la multa incrementa el saldo adeudado del socio."""
    reglas.registrar_asistencia(conn, reunion["reunionId"], socio["socioId"], "AUSENTE")
    cuenta = reglas.estado_cuenta(conn, socio["socioId"])
    assert cuenta["saldo"] == 5.00
