"""Pruebas de la historia HU-05 (apertura, arqueo y cierre bloqueante de caja).

Cubre CA-05.1 (cierre en ≤ 2 s con concentración de totales), CA-05.2 (inmutabilidad
tras el cierre) y CA-05.3 (consistencia del corte). Escenario E1 y ADR-002.
"""

import pytest

import reglas

PERIODO = "2026-10"


def _preparar_jornada(conn, reunion):
    """Socio presente + café de turno ($1,50) + cuota pagada ($25,00)."""
    socio = reglas.crear_socio(conn, "0401112223", "Socio Jornada", 4)
    reglas.registrar_asistencia(conn, reunion["reunionId"], socio["socioId"], "PRESENTE")
    reglas.registrar_cafe(conn, reunion["reunionId"], socio["socioId"])
    reglas.registrar_cuota(conn, reunion["reunionId"], socio["socioId"], PERIODO, 25.00)
    return socio


def test_cierre_consolida_y_es_consistente(conn, reunion):
    """CA-05.1 y CA-05.3: el cierre consolida los totales sin inconsistencias."""
    _preparar_jornada(conn, reunion)
    cierre = reglas.cerrar_reunion(conn, reunion["reunionId"])
    assert cierre["estado"] == "CERRADA"
    assert cierre["totalIngresos"] == 26.50  # cuota 25,00 + café 1,50
    assert cierre["consistente"] is True


def test_segundo_cierre_devuelve_conflicto(conn, reunion):
    """CA-05.2: cerrar una reunión ya cerrada es un conflicto."""
    reglas.cerrar_reunion(conn, reunion["reunionId"])
    with pytest.raises(reglas.ReunionYaCerrada):
        reglas.cerrar_reunion(conn, reunion["reunionId"])


def test_modificacion_tras_el_cierre_es_rechazada(conn, reunion):
    """CA-05.2 / ADR-002: la reunión cerrada no admite nuevos cobros."""
    socio = _preparar_jornada(conn, reunion)
    reglas.cerrar_reunion(conn, reunion["reunionId"])
    with pytest.raises(reglas.ReunionCerrada):
        reglas.registrar_cafe(conn, reunion["reunionId"], socio["socioId"])


def test_corte_de_caja_cuadra(conn, reunion):
    """CA-05.3: Fondo inicial + cobros − egresos = total, sin inconsistencias."""
    _preparar_jornada(conn, reunion)
    corte = reglas.corte_caja(conn, reunion["reunionId"])
    assert corte["consistente"] is True
    assert corte["total"] == 126.50  # 100,00 de fondo + 26,50 de cobros
