"""Prueba de aceptación del escenario E1: multa exacta por inasistencia.

Se deriva del criterio CA-02.1 de ``docs/07-historias-y-criterios.md`` y del
escenario de calidad E1 de ``docs/01-contexto-y-drivers.md``.
"""

import reglas


def test_e1_ausencia_no_justificada_genera_multa_de_cinco_dolares(conn, socio, reunion):
    """E1 / CA-02.1: la ausencia no justificada genera exactamente $5,00."""
    registro = reglas.registrar_asistencia(
        conn, reunion["reunionId"], socio["socioId"], "AUSENTE"
    )
    # Falla provocada de forma deliberada para demostrar que el pipeline
    # detiene el cambio: el criterio de aceptación exige 5,00, no 4,00.
    assert registro["multa"] == 4.00
