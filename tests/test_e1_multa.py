"""Pruebas de aceptación del escenario E1: multa exacta por inasistencia.

Se derivan del criterio CA-02.1 de ``docs/07-historias-y-criterios.md`` y del
escenario de calidad E1 de ``docs/01-contexto-y-drivers.md``.
"""

import reglas


def test_e1_ausencia_no_justificada_genera_multa_de_cinco_dolares(conn, socio, reunion):
    """E1 / CA-02.1: la ausencia no justificada genera exactamente $5,00."""
    registro = reglas.registrar_asistencia(
        conn, reunion["reunionId"], socio["socioId"], "AUSENTE"
    )
    assert registro["multa"] == 5.00

    cuenta = reglas.estado_cuenta(conn, socio["socioId"])
    assert cuenta["saldo"] == 5.00


def test_e1_el_cierre_conserva_la_multa_sin_inconsistencias(conn, socio, reunion):
    """E1: el corte de caja refleja la multa y queda consistente."""
    reglas.registrar_asistencia(conn, reunion["reunionId"], socio["socioId"], "AUSENTE")

    corte = reglas.cerrar_reunion(conn, reunion["reunionId"])

    assert corte["estado"] == "CERRADA"
    assert corte["totalIngresos"] == 5.00
    assert corte["consistente"] is True
