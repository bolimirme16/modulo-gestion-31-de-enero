"""Pruebas de la historia HU-03 (cobro del servicio de café).

Cubre CA-03.1 (tarifa diferenciada $1,50 / $3,00) y CA-03.2 (un cobro por socio y
reunión). Escenario E1 y ADR-002 (reglas financieras centralizadas).
"""

import pytest

import reglas


@pytest.mark.parametrize(
    ("grupo_turno", "grupo_socio", "tarifa_esperada"),
    [(4, 4, 1.50), (4, 1, 3.00), (4, 10, 3.00), (8, 8, 1.50)],
)
def test_tarifa_de_cafe_por_grupo(conn, grupo_turno, grupo_socio, tarifa_esperada):
    """CA-03.1: el grupo de turno paga $1,50; el resto, $3,00."""
    reunion = reglas.abrir_reunion(conn, "2026-10-31", grupo_turno=grupo_turno)
    socio = reglas.crear_socio(conn, "0405556667", "Socio Café", grupo_socio)
    cobro = reglas.registrar_cafe(conn, reunion["reunionId"], socio["socioId"])
    assert cobro["tarifa"] == tarifa_esperada


def test_rechazo_de_doble_cobro_de_cafe(conn, socio, reunion):
    """CA-03.2 / R2: un solo cobro de café por socio y reunión."""
    reglas.registrar_cafe(conn, reunion["reunionId"], socio["socioId"])
    with pytest.raises(reglas.RegistroDuplicado):
        reglas.registrar_cafe(conn, reunion["reunionId"], socio["socioId"])


def test_no_se_puede_cobrar_cafe_en_reunion_cerrada(conn, socio, reunion):
    """ADR-002: la reunión cerrada congela los cobros."""
    reglas.cerrar_reunion(conn, reunion["reunionId"])
    with pytest.raises(reglas.ReunionCerrada):
        reglas.registrar_cafe(conn, reunion["reunionId"], socio["socioId"])
