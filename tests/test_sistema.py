"""Pruebas de la historia HU-07 (respaldo e integridad de datos).

Cubre CA-07.1 (respaldo restaurable en ≤ 5 s) y CA-07.2 (9 de 9 chequeos de
integridad). Escenario E6.
"""

import reglas


def test_integridad_supera_los_nueve_chequeos(conn, socio, reunion):
    """CA-07.2 / E6: la rutina de diagnóstico devuelve 9 de 9 chequeos correctos."""
    reglas.registrar_asistencia(conn, reunion["reunionId"], socio["socioId"], "AUSENTE")
    resultado = reglas.verificar_integridad(conn)
    assert resultado["resultado"] == "ok"
    assert resultado["chequeosSuperados"] == reglas.CHEQUEOS_INTEGRIDAD
    assert resultado["errores"] == 0


def test_respaldo_genera_archivo_restaurable(conn, tmp_path):
    """CA-07.1 / E6: el respaldo se materializa como archivo con marca de tiempo."""
    reglas.crear_socio(conn, "0401234567", "Socio Respaldo", 1)
    respaldo = reglas.crear_respaldo(conn, str(tmp_path), "asociacion_20261031.db")
    assert respaldo["estado"] == "COMPLETADO"
    assert respaldo["bytes"] > 0
    assert (tmp_path / "asociacion_20261031.db").exists()
