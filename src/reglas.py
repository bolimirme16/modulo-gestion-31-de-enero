"""Reglas de negocio y persistencia del Sistema de Gestión 31 de Enero.

Capa de reglas financieras centralizada (driver D3 / escenario E3): las tarifas y
reglas viven en un único punto. Persistencia local en SQLite sin dependencias
externas (ADR-001). Ver `docs/06-mapa-toolchain.md` y `docs/07-historias-y-criterios.md`.
"""

from __future__ import annotations

import sqlite3
import uuid

# --- Tarifas y límites vigentes (único punto de cambio · D3 / E3) -------------
CUOTA_MENSUAL = 25.00          # USD por mes (R2, E1)
MULTA_INASISTENCIA = 5.00      # USD por falta no justificada (E1)
TARIFA_CAFE_TURNO = 1.50       # USD grupo de turno (E1)
TARIFA_CAFE_REGULAR = 3.00     # USD resto de grupos (E1)
MAX_SOCIOS = 69                # R6
CHEQUEOS_INTEGRIDAD = 9        # E6

ESTADOS_ASISTENCIA = ("PRESENTE", "AUSENTE", "JUSTIFICADO")
CONCEPTOS = ("CUOTA", "MULTA", "CAFE")

ESQUEMA = """
CREATE TABLE IF NOT EXISTS socios (
    socio_id       TEXT PRIMARY KEY,
    identificacion TEXT NOT NULL UNIQUE,
    nombres        TEXT NOT NULL,
    grupo_cafe     INTEGER NOT NULL,
    activo         INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS reuniones (
    reunion_id    TEXT PRIMARY KEY,
    fecha         TEXT NOT NULL,
    grupo_turno   INTEGER NOT NULL,
    estado        TEXT NOT NULL DEFAULT 'ABIERTA',
    fondo_inicial REAL NOT NULL DEFAULT 0,
    egresos       REAL NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS asistencias (
    asistencia_id TEXT PRIMARY KEY,
    reunion_id    TEXT NOT NULL,
    socio_id      TEXT NOT NULL,
    estado        TEXT NOT NULL,
    multa         REAL NOT NULL DEFAULT 0,
    UNIQUE (reunion_id, socio_id)
);
CREATE TABLE IF NOT EXISTS cargos (
    cargo_id   TEXT PRIMARY KEY,
    socio_id   TEXT NOT NULL,
    reunion_id TEXT,
    periodo    TEXT NOT NULL,
    concepto   TEXT NOT NULL,
    monto      REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS abonos (
    abono_id  TEXT PRIMARY KEY,
    socio_id  TEXT NOT NULL,
    periodo   TEXT NOT NULL,
    concepto  TEXT NOT NULL,
    monto     REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cargos_socio ON cargos (socio_id, periodo);
CREATE INDEX IF NOT EXISTS idx_abonos_socio ON abonos (socio_id, periodo);
"""


# --- Errores de negocio con código HTTP --------------------------------------
class ReglaViolada(Exception):
    """Error de negocio traducible a una respuesta HTTP."""

    codigo = "REGLA_VIOLADA"
    http = 422

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class NoEncontrado(ReglaViolada):
    codigo = "NO_ENCONTRADO"
    http = 404


class IdentificacionDuplicada(ReglaViolada):
    codigo = "IDENTIFICACION_DUPLICADA"
    http = 409


class LimiteSocios(ReglaViolada):
    codigo = "LIMITE_SOCIOS"
    http = 422


class ReunionCerrada(ReglaViolada):
    """La reunión está congelada: no admite cambios (ADR-002)."""

    codigo = "REUNION_CERRADA"
    http = 403


class ReunionYaCerrada(ReglaViolada):
    codigo = "REUNION_YA_CERRADA"
    http = 409


class RegistroDuplicado(ReglaViolada):
    codigo = "REGISTRO_DUPLICADO"
    http = 409


class Sobrepago(ReglaViolada):
    codigo = "SOBREPAGO"
    http = 422


# --- Utilidades ---------------------------------------------------------------
def _nuevo_id() -> str:
    return str(uuid.uuid4())


def _dinero(valor: float) -> float:
    return round(float(valor) + 0.0, 2)


def _periodo(fecha: str) -> str:
    """Devuelve AAAA-MM a partir de una fecha ISO (AAAA-MM-DD)."""
    return fecha[:7]


def conectar(ruta: str = ":memory:") -> sqlite3.Connection:
    """Abre (y crea si hace falta) la base de datos local aplicando el esquema."""
    conn = sqlite3.connect(ruta)
    conn.row_factory = sqlite3.Row
    conn.executescript(ESQUEMA)
    return conn


# --- Socios (HU-01) -----------------------------------------------------------
def _fila_socio(fila: sqlite3.Row) -> dict:
    """Proyección pública del socio: sin cédula (R1 / LOPDP)."""
    return {
        "socioId": fila["socio_id"],
        "nombres": fila["nombres"],
        "grupoCafe": fila["grupo_cafe"],
        "estado": "ACTIVO" if fila["activo"] else "INACTIVO",
    }


def crear_socio(
    conn: sqlite3.Connection, identificacion: str, nombres: str, grupo_cafe: int
) -> dict:
    """Registra un socio aplicando R6 (máximo 69) y la unicidad de identificación."""
    if not 1 <= int(grupo_cafe) <= 10:
        raise ReglaViolada("El grupo de café debe estar entre 1 y 10.")

    activos = conn.execute("SELECT COUNT(*) AS n FROM socios WHERE activo = 1").fetchone()["n"]
    if activos >= MAX_SOCIOS:
        raise LimiteSocios(
            f"Límite máximo alcanzado: la asociación no puede exceder los {MAX_SOCIOS} socios."
        )

    socio_id = _nuevo_id()
    try:
        with conn:
            conn.execute(
                "INSERT INTO socios (socio_id, identificacion, nombres, grupo_cafe, activo) "
                "VALUES (?, ?, ?, ?, 1)",
                (socio_id, identificacion, nombres, int(grupo_cafe)),
            )
    except sqlite3.IntegrityError as exc:
        raise IdentificacionDuplicada(
            f"La cédula {identificacion} ya se encuentra registrada en el sistema."
        ) from exc
    return obtener_socio(conn, socio_id)


def listar_socios(conn: sqlite3.Connection, estado: str | None = None) -> list[dict]:
    sql = "SELECT * FROM socios"
    params: tuple = ()
    if estado == "ACTIVO":
        sql += " WHERE activo = 1"
    elif estado == "INACTIVO":
        sql += " WHERE activo = 0"
    sql += " ORDER BY nombres"
    return [_fila_socio(f) for f in conn.execute(sql, params).fetchall()]


def obtener_socio(conn: sqlite3.Connection, socio_id: str) -> dict:
    fila = conn.execute("SELECT * FROM socios WHERE socio_id = ?", (socio_id,)).fetchone()
    if fila is None:
        raise NoEncontrado(f"El socio {socio_id} no existe.")
    return _fila_socio(fila)


def inactivar_socio(conn: sqlite3.Connection, socio_id: str) -> dict:
    """Baja lógica: nunca se borra el historial (R6)."""
    obtener_socio(conn, socio_id)
    with conn:
        conn.execute("UPDATE socios SET activo = 0 WHERE socio_id = ?", (socio_id,))
    return obtener_socio(conn, socio_id)


# --- Reuniones -----------------------------------------------------------------
def abrir_reunion(
    conn: sqlite3.Connection, fecha: str, grupo_turno: int, fondo_inicial: float = 0.0
) -> dict:
    reunion_id = _nuevo_id()
    with conn:
        conn.execute(
            "INSERT INTO reuniones "
            "(reunion_id, fecha, grupo_turno, estado, fondo_inicial, egresos) "
            "VALUES (?, ?, ?, 'ABIERTA', ?, 0)",
            (reunion_id, fecha, int(grupo_turno), _dinero(fondo_inicial)),
        )
    return obtener_reunion(conn, reunion_id)


def obtener_reunion(conn: sqlite3.Connection, reunion_id: str) -> dict:
    fila = conn.execute("SELECT * FROM reuniones WHERE reunion_id = ?", (reunion_id,)).fetchone()
    if fila is None:
        raise NoEncontrado(f"La reunión {reunion_id} no existe.")
    return {
        "reunionId": fila["reunion_id"],
        "fecha": fila["fecha"],
        "grupoTurno": fila["grupo_turno"],
        "estado": fila["estado"],
        "fondoInicial": _dinero(fila["fondo_inicial"]),
    }


def _exigir_abierta(conn: sqlite3.Connection, reunion_id: str) -> dict:
    reunion = obtener_reunion(conn, reunion_id)
    if reunion["estado"] == "CERRADA":
        raise ReunionCerrada(
            "Operación denegada: la reunión está cerrada y congelada para auditoría."
        )
    return reunion


def _exigir_socio(conn: sqlite3.Connection, socio_id: str) -> sqlite3.Row:
    fila = conn.execute("SELECT * FROM socios WHERE socio_id = ?", (socio_id,)).fetchone()
    if fila is None:
        raise NoEncontrado(f"El socio {socio_id} no existe.")
    return fila


# --- Asistencia y multas (HU-02) ----------------------------------------------
def registrar_asistencia(
    conn: sqlite3.Connection, reunion_id: str, socio_id: str, estado: str
) -> dict:
    if estado not in ESTADOS_ASISTENCIA:
        raise ReglaViolada(f"Estado de asistencia inválido: {estado}.")
    reunion = _exigir_abierta(conn, reunion_id)
    _exigir_socio(conn, socio_id)

    multa = MULTA_INASISTENCIA if estado == "AUSENTE" else 0.0
    asistencia_id = _nuevo_id()
    try:
        with conn:
            conn.execute(
                "INSERT INTO asistencias (asistencia_id, reunion_id, socio_id, estado, multa) "
                "VALUES (?, ?, ?, ?, ?)",
                (asistencia_id, reunion_id, socio_id, estado, _dinero(multa)),
            )
            if multa > 0:
                conn.execute(
                    "INSERT INTO cargos (cargo_id, socio_id, reunion_id, periodo, concepto, monto) "
                    "VALUES (?, ?, ?, ?, 'MULTA', ?)",
                    (_nuevo_id(), socio_id, reunion_id, _periodo(reunion["fecha"]), _dinero(multa)),
                )
    except sqlite3.IntegrityError as exc:
        raise RegistroDuplicado(
            "El socio ya tiene una asistencia registrada en esta reunión."
        ) from exc

    return {
        "asistenciaId": asistencia_id,
        "reunionId": reunion_id,
        "socioId": socio_id,
        "estado": estado,
        "multa": _dinero(multa),
    }


# --- Café (HU-03) --------------------------------------------------------------
def calcular_tarifa_cafe(grupo_socio: int, grupo_turno: int) -> float:
    """Tarifa de café: $1,50 para el grupo de turno, $3,00 para el resto (E1)."""
    return TARIFA_CAFE_TURNO if int(grupo_socio) == int(grupo_turno) else TARIFA_CAFE_REGULAR


def registrar_cafe(conn: sqlite3.Connection, reunion_id: str, socio_id: str) -> dict:
    reunion = _exigir_abierta(conn, reunion_id)
    socio = _exigir_socio(conn, socio_id)
    tarifa = calcular_tarifa_cafe(socio["grupo_cafe"], reunion["grupoTurno"])

    duplicado = conn.execute(
        "SELECT 1 FROM cargos WHERE reunion_id = ? AND socio_id = ? AND concepto = 'CAFE'",
        (reunion_id, socio_id),
    ).fetchone()
    if duplicado is not None:
        raise RegistroDuplicado("El socio ya tiene un cobro de café en esta reunión.")

    with conn:
        conn.execute(
            "INSERT INTO cargos (cargo_id, socio_id, reunion_id, periodo, concepto, monto) "
            "VALUES (?, ?, ?, ?, 'CAFE', ?)",
            (_nuevo_id(), socio_id, reunion_id, _periodo(reunion["fecha"]), _dinero(tarifa)),
        )
    return {"socioId": socio_id, "tarifa": _dinero(tarifa), "grupoTurno": reunion["grupoTurno"]}


# --- Cuota mensual y abonos (HU-04) -------------------------------------------
def _abonado_cuota(conn: sqlite3.Connection, socio_id: str, periodo: str) -> float:
    fila = conn.execute(
        "SELECT COALESCE(SUM(monto), 0) AS s FROM abonos "
        "WHERE socio_id = ? AND periodo = ? AND concepto = 'CUOTA'",
        (socio_id, periodo),
    ).fetchone()
    return _dinero(fila["s"])


def _estado_cuota(saldo: float, abonado: float) -> str:
    if saldo <= 0:
        return "PAGADO"
    if abonado > 0:
        return "PARCIAL"
    return "PENDIENTE"


def registrar_cuota(
    conn: sqlite3.Connection, reunion_id: str, socio_id: str, periodo: str, monto: float
) -> dict:
    _exigir_abierta(conn, reunion_id)
    _exigir_socio(conn, socio_id)
    if monto <= 0:
        raise ReglaViolada("El monto del abono debe ser mayor que cero.")

    cargo = conn.execute(
        "SELECT monto FROM cargos WHERE socio_id = ? AND periodo = ? AND concepto = 'CUOTA'",
        (socio_id, periodo),
    ).fetchone()
    if cargo is None:
        with conn:
            conn.execute(
                "INSERT INTO cargos (cargo_id, socio_id, reunion_id, periodo, concepto, monto) "
                "VALUES (?, ?, ?, ?, 'CUOTA', ?)",
                (_nuevo_id(), socio_id, reunion_id, periodo, _dinero(CUOTA_MENSUAL)),
            )
        total = CUOTA_MENSUAL
    else:
        total = _dinero(cargo["monto"])

    abonado = _abonado_cuota(conn, socio_id, periodo)
    pendiente = _dinero(total - abonado)
    if _dinero(monto) > pendiente + 1e-9:
        raise Sobrepago(
            f"El abono de {_dinero(monto):.2f} supera el saldo pendiente de {pendiente:.2f}."
        )

    with conn:
        conn.execute(
            "INSERT INTO abonos (abono_id, socio_id, periodo, concepto, monto) "
            "VALUES (?, ?, ?, 'CUOTA', ?)",
            (_nuevo_id(), socio_id, periodo, _dinero(monto)),
        )

    abonado = _abonado_cuota(conn, socio_id, periodo)
    saldo = _dinero(total - abonado)
    return {
        "socioId": socio_id,
        "periodo": periodo,
        "montoTotal": _dinero(total),
        "abonado": abonado,
        "saldo": saldo,
        "estado": _estado_cuota(saldo, abonado),
    }


# --- Estado de cuenta y comprobante (HU-06) -----------------------------------
def _cargos(
    conn: sqlite3.Connection, socio_id: str, periodo: str | None = None
) -> list[sqlite3.Row]:
    sql = "SELECT concepto, monto FROM cargos WHERE socio_id = ?"
    params: list = [socio_id]
    if periodo:
        sql += " AND periodo = ?"
        params.append(periodo)
    sql += " ORDER BY concepto"
    return conn.execute(sql, tuple(params)).fetchall()


def estado_cuenta(conn: sqlite3.Connection, socio_id: str, periodo: str | None = None) -> dict:
    _exigir_socio(conn, socio_id)
    filas_cargo = _cargos(conn, socio_id, periodo)
    cargos = [{"concepto": c["concepto"], "monto": _dinero(c["monto"])} for c in filas_cargo]
    sql = "SELECT concepto, monto FROM abonos WHERE socio_id = ?"
    params: list = [socio_id]
    if periodo:
        sql += " AND periodo = ?"
        params.append(periodo)
    filas_abono = conn.execute(sql, tuple(params)).fetchall()
    abonos = [{"concepto": a["concepto"], "monto": _dinero(a["monto"])} for a in filas_abono]
    saldo = _dinero(sum(c["monto"] for c in cargos) - sum(a["monto"] for a in abonos))
    return {"socioId": socio_id, "saldo": saldo, "cargos": cargos, "abonos": abonos}


def comprobante(conn: sqlite3.Connection, socio_id: str, periodo: str) -> dict:
    _exigir_socio(conn, socio_id)
    cargos = _cargos(conn, socio_id, periodo)
    if not cargos:
        raise NoEncontrado(f"No hay movimientos del socio {socio_id} en el período {periodo}.")
    detalle = [{"concepto": c["concepto"], "monto": _dinero(c["monto"])} for c in cargos]
    return {
        "socioId": socio_id,
        "periodo": periodo,
        "detalle": detalle,
        "total": _dinero(sum(c["monto"] for c in cargos)),
    }


# --- Cierre y caja (HU-05) -----------------------------------------------------
def _totales(conn: sqlite3.Connection, reunion_id: str) -> dict:
    filas = conn.execute(
        "SELECT concepto, COALESCE(SUM(monto), 0) AS s FROM cargos "
        "WHERE reunion_id = ? GROUP BY concepto",
        (reunion_id,),
    ).fetchall()
    por_concepto = {f["concepto"]: _dinero(f["s"]) for f in filas}
    cuotas = por_concepto.get("CUOTA", 0.0)
    cafe = por_concepto.get("CAFE", 0.0)
    multas = por_concepto.get("MULTA", 0.0)
    return {
        "cuotas": cuotas,
        "cafe": cafe,
        "multas": multas,
        "cobrosEfectivo": _dinero(cuotas + cafe + multas),
    }


def _inconsistencias(conn: sqlite3.Connection, reunion_id: str) -> list[str]:
    """Invariantes del corte (E1): 0 inconsistencias esperadas."""
    fallos: list[str] = []
    for fila in conn.execute(
        "SELECT concepto, monto FROM cargos WHERE reunion_id = ?", (reunion_id,)
    ).fetchall():
        concepto, monto = fila["concepto"], _dinero(fila["monto"])
        esperado = {"CUOTA": CUOTA_MENSUAL, "MULTA": MULTA_INASISTENCIA}
        if concepto in esperado and monto != esperado[concepto]:
            fallos.append(f"{concepto} con monto {monto:.2f}")
        if concepto == "CAFE" and monto not in (TARIFA_CAFE_TURNO, TARIFA_CAFE_REGULAR):
            fallos.append(f"CAFE con monto {monto:.2f}")
        if monto < 0:
            fallos.append(f"{concepto} con monto negativo")
    return fallos


def corte_caja(conn: sqlite3.Connection, reunion_id: str) -> dict:
    fila = conn.execute("SELECT * FROM reuniones WHERE reunion_id = ?", (reunion_id,)).fetchone()
    if fila is None:
        raise NoEncontrado(f"La reunión {reunion_id} no existe.")
    totales = _totales(conn, reunion_id)
    total = _dinero(fila["fondo_inicial"] + totales["cobrosEfectivo"] - fila["egresos"])
    return {
        "reunionId": reunion_id,
        "fondoInicial": _dinero(fila["fondo_inicial"]),
        "cobrosEfectivo": totales["cobrosEfectivo"],
        "egresos": _dinero(fila["egresos"]),
        "total": total,
        "consistente": len(_inconsistencias(conn, reunion_id)) == 0,
    }


def cerrar_reunion(conn: sqlite3.Connection, reunion_id: str) -> dict:
    reunion = obtener_reunion(conn, reunion_id)
    if reunion["estado"] == "CERRADA":
        raise ReunionYaCerrada("La reunión ya estaba cerrada.")
    totales = _totales(conn, reunion_id)
    consistente = len(_inconsistencias(conn, reunion_id)) == 0
    with conn:
        conn.execute("UPDATE reuniones SET estado = 'CERRADA' WHERE reunion_id = ?", (reunion_id,))
    return {
        "reunionId": reunion_id,
        "estado": "CERRADA",
        "totalIngresos": totales["cobrosEfectivo"],
        "consistente": consistente,
    }


# --- Integridad y respaldo (HU-07) --------------------------------------------
def verificar_integridad(conn: sqlite3.Connection) -> dict:
    chequeos: list[str] = []

    def ok(nombre: str, condicion: bool) -> None:
        if condicion:
            chequeos.append(nombre)

    ok("integridad_fisica", conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok")
    ok("claves_foraneas", len(conn.execute("PRAGMA foreign_key_check").fetchall()) == 0)
    ok(
        "indices",
        len(
            conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'index' AND name LIKE 'idx_%'"
            ).fetchall()
        )
        >= 2,
    )
    ok(
        "duplicados_identificacion",
        len(
            conn.execute(
                "SELECT identificacion FROM socios GROUP BY identificacion HAVING COUNT(*) > 1"
            ).fetchall()
        )
        == 0,
    )
    ok(
        "multas_validas",
        len(
            conn.execute(
                "SELECT 1 FROM cargos WHERE concepto = 'MULTA' AND monto <> ?",
                (MULTA_INASISTENCIA,),
            ).fetchall()
        )
        == 0,
    )
    ok(
        "cafe_valido",
        len(
            conn.execute(
                "SELECT 1 FROM cargos WHERE concepto = 'CAFE' AND monto NOT IN (?, ?)",
                (TARIFA_CAFE_TURNO, TARIFA_CAFE_REGULAR),
            ).fetchall()
        )
        == 0,
    )
    ok(
        "cuota_valida",
        len(
            conn.execute(
                "SELECT 1 FROM cargos WHERE concepto = 'CUOTA' AND monto <> ?",
                (CUOTA_MENSUAL,),
            ).fetchall()
        )
        == 0,
    )
    ok(
        "saldos_no_negativos",
        len(conn.execute("SELECT 1 FROM cargos WHERE monto < 0").fetchall()) == 0,
    )
    ok(
        "cierres_consistentes",
        all(
            len(_inconsistencias(conn, r["reunion_id"])) == 0
            for r in conn.execute("SELECT reunion_id FROM reuniones").fetchall()
        ),
    )

    errores = CHEQUEOS_INTEGRIDAD - len(chequeos)
    return {
        "resultado": "ok" if errores == 0 else "error",
        "chequeosSuperados": len(chequeos),
        "errores": errores,
        "chequeos": chequeos,
    }


def crear_respaldo(conn: sqlite3.Connection, destino: str, archivo: str) -> dict:
    """Respalda la base a un archivo (unidad USB) usando la API de respaldo de SQLite."""
    from pathlib import Path

    ruta = Path(destino) / archivo
    ruta.parent.mkdir(parents=True, exist_ok=True)
    respaldo = sqlite3.connect(str(ruta))
    with respaldo:
        conn.backup(respaldo)
    respaldo.close()
    return {
        "archivo": archivo,
        "destino": str(destino),
        "bytes": ruta.stat().st_size,
        "estado": "COMPLETADO",
    }
