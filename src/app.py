"""Servicio HTTP local: espejo ejecutable de `api/openapi.yaml`.

Monta las operaciones del contrato bajo `/api/v1` y delega la lógica de negocio en
la capa de reglas (`reglas.py`). Pensado para operar en una sola PC, monousuario y
offline (R4, ADR-003).
"""

from __future__ import annotations

import os

from flask import Flask, jsonify, request

import reglas

API = "/api/v1"


def crear_app(ruta_db: str = ":memory:") -> Flask:
    """Crea la aplicación con su conexión a la base local."""
    app = Flask(__name__)
    conn = reglas.conectar(ruta_db)
    app.config["DB"] = conn

    @app.errorhandler(reglas.ReglaViolada)
    def _error_negocio(exc: reglas.ReglaViolada):  # pragma: no cover - envoltura
        return jsonify({"codigo": exc.codigo, "mensaje": exc.mensaje}), exc.http

    def db():
        return app.config["DB"]

    def cuerpo() -> dict:
        return request.get_json(silent=True) or {}

    # --- Socios ---------------------------------------------------------------
    @app.get(f"{API}/socios")
    def listar_socios():
        return jsonify(reglas.listar_socios(db(), request.args.get("estado")))

    @app.post(f"{API}/socios")
    def crear_socio():
        datos = cuerpo()
        socio = reglas.crear_socio(
            db(),
            str(datos.get("identificacion", "")),
            str(datos.get("nombres", "")),
            int(datos.get("grupoCafe", 0) or 0),
        )
        return jsonify(socio), 201

    @app.get(f"{API}/socios/<socio_id>")
    def obtener_socio(socio_id: str):
        return jsonify(reglas.obtener_socio(db(), socio_id))

    @app.get(f"{API}/socios/<socio_id>/estado-cuenta")
    def consultar_estado_cuenta(socio_id: str):
        return jsonify(reglas.estado_cuenta(db(), socio_id, request.args.get("periodo")))

    @app.get(f"{API}/socios/<socio_id>/comprobante")
    def obtener_comprobante(socio_id: str):
        return jsonify(reglas.comprobante(db(), socio_id, request.args.get("periodo", "")))

    # --- Reuniones ------------------------------------------------------------
    @app.post(f"{API}/reuniones/<reunion_id>/asistencia")
    def registrar_asistencia(reunion_id: str):
        datos = cuerpo()
        registro = reglas.registrar_asistencia(
            db(), reunion_id, str(datos.get("socioId", "")), str(datos.get("estado", ""))
        )
        return jsonify(registro), 201

    @app.post(f"{API}/reuniones/<reunion_id>/cafe")
    def registrar_cafe(reunion_id: str):
        registro = reglas.registrar_cafe(db(), reunion_id, str(cuerpo().get("socioId", "")))
        return jsonify(registro), 201

    @app.post(f"{API}/reuniones/<reunion_id>/cuotas")
    def registrar_cuota(reunion_id: str):
        datos = cuerpo()
        registro = reglas.registrar_cuota(
            db(),
            reunion_id,
            str(datos.get("socioId", "")),
            str(datos.get("periodo", "")),
            float(datos.get("monto", 0) or 0),
        )
        return jsonify(registro), 201

    @app.post(f"{API}/reuniones/<reunion_id>/cierre")
    def cerrar_reunion(reunion_id: str):
        return jsonify(reglas.cerrar_reunion(db(), reunion_id))

    @app.get(f"{API}/reuniones/<reunion_id>/caja")
    def obtener_corte_caja(reunion_id: str):
        return jsonify(reglas.corte_caja(db(), reunion_id))

    # --- Sistema --------------------------------------------------------------
    @app.get(f"{API}/sistema/integridad")
    def verificar_integridad():
        return jsonify(reglas.verificar_integridad(db()))

    @app.post(f"{API}/sistema/respaldo")
    def crear_respaldo():
        destino = os.environ.get("RESPALDO_DIR", "./respaldos")
        archivo = os.environ.get("RESPALDO_NOMBRE", "asociacion_respaldo.db")
        return jsonify(reglas.crear_respaldo(db(), destino, archivo)), 202

    return app


if __name__ == "__main__":  # pragma: no cover
    crear_app(os.environ.get("DB_RUTA", "asociacion.db")).run(
        host="127.0.0.1", port=8080, debug=False
    )
