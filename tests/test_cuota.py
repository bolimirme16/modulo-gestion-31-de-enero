"""Pruebas de la historia HU-04 (cuota mensual y abonos parciales).

Cubre CA-04.1 (cuota fija de $25,00), CA-04.2 (abono parcial con saldo exacto) y
CA-04.3 (rechazo del sobrepago). Escenario E1 y ADR-002.
"""

import pytest

import reglas

PERIODO = "2026-10"


def test_pago_completo_de_la_cuota(conn, socio, reunion):
    """CA-04.1: el pago completo deja el saldo en $0,00 y el rubro PAGADO."""
    cuota = reglas.registrar_cuota(conn, reunion["reunionId"], socio["socioId"], PERIODO, 25.00)
    assert cuota["montoTotal"] == 25.00
    assert cuota["saldo"] == 0.00
    assert cuota["estado"] == "PAGADO"


def test_abono_parcial_deja_saldo_en_15(conn, socio, reunion):
    """CA-04.2: un abono de $10,00 deja un saldo exacto de $15,00."""
    cuota = reglas.registrar_cuota(conn, reunion["reunionId"], socio["socioId"], PERIODO, 10.00)
    assert cuota["saldo"] == 15.00
    assert cuota["estado"] == "PARCIAL"


def test_rechazo_de_sobrepago(conn, socio, reunion):
    """CA-04.3: no se admite un abono mayor que el saldo pendiente."""
    reglas.registrar_cuota(conn, reunion["reunionId"], socio["socioId"], PERIODO, 10.00)
    with pytest.raises(reglas.Sobrepago):
        reglas.registrar_cuota(conn, reunion["reunionId"], socio["socioId"], PERIODO, 20.00)


def test_no_se_puede_abonar_en_reunion_cerrada(conn, socio, reunion):
    """ADR-002: la reunión cerrada congela los cobros."""
    reglas.cerrar_reunion(conn, reunion["reunionId"])
    with pytest.raises(reglas.ReunionCerrada):
        reglas.registrar_cuota(conn, reunion["reunionId"], socio["socioId"], PERIODO, 25.00)
