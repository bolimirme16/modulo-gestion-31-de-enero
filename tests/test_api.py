"""Pruebas de extremo a extremo sobre el servicio HTTP (contrato api/openapi.yaml).

Verifican dos cosas que un linter de contrato no puede comprobar (ISO/IEC 29148 y
revisión OWASP): que el padrón no exponga datos personales (R1 / LOPDP) y que la
cadena HU-01 → HU-05 funcione sobre los endpoints reales.
"""

import reglas

API = "/api/v1"


def test_el_padron_no_expone_datos_personales(servicio):
    """Seguridad (R1 / LOPDP): la respuesta nunca devuelve la cédula."""
    _app, client, _conn = servicio
    client.post(
        f"{API}/socios",
        json={"identificacion": "1002345678", "nombres": "Socio A", "grupoCafe": 3},
    )
    respuesta = client.get(f"{API}/socios")
    assert respuesta.status_code == 200
    assert "1002345678" not in respuesta.get_data(as_text=True)
    assert "identificacion" not in respuesta.get_json()[0]


def test_flujo_completo_de_la_reunion(servicio):
    """Cadena HU-01 → HU-05 sobre los endpoints del contrato."""
    _app, client, conn = servicio
    socio = reglas.crear_socio(conn, "0401234567", "Socio Flujo", 4)
    reunion = reglas.abrir_reunion(conn, "2026-10-31", grupo_turno=4, fondo_inicial=100.0)
    sid, rid = socio["socioId"], reunion["reunionId"]

    r = client.post(f"{API}/reuniones/{rid}/asistencia", json={"socioId": sid, "estado": "AUSENTE"})
    assert r.status_code == 201
    assert client.post(f"{API}/reuniones/{rid}/cafe", json={"socioId": sid}).status_code == 201
    r = client.post(
        f"{API}/reuniones/{rid}/cuotas",
        json={"socioId": sid, "periodo": "2026-10", "monto": 25.0},
    )
    assert r.status_code == 201

    assert client.get(f"{API}/reuniones/{rid}/caja").get_json()["consistente"] is True
    assert client.post(f"{API}/reuniones/{rid}/cierre").get_json()["estado"] == "CERRADA"
    assert client.post(f"{API}/reuniones/{rid}/cafe", json={"socioId": sid}).status_code == 403
    assert client.get(f"{API}/sistema/integridad").get_json()["resultado"] == "ok"
