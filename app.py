#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asociación 31 DE ENERO NARCIZA DE JESUS - sistema local (Flask + SQLite)."""
VERSION = "1.2.0"
import sqlite3, os, sys, calendar, secrets
from datetime import datetime, date
from functools import wraps
from flask import Flask, request, redirect, url_for, render_template, g, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

def _base_dir():
    # Congelado (exe): todo vive junto al ejecutable; si no hay escritura, usar carpeta del usuario
    if getattr(sys, "frozen", False):
        exe = os.path.dirname(sys.executable)
        if os.access(exe, os.W_OK):
            return exe
        alt = os.path.join(os.path.expanduser("~"), "Sistema31Enero")
        os.makedirs(alt, exist_ok=True)
        return alt
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = _base_dir()
DB_PATH = os.path.join(BASE_DIR, "asociacion.db")
EXE_DIR = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else BASE_DIR

def _recurso(*partes):
    """Primero junto al exe/fuente (editable), luego dentro del bundle _internal."""
    c1 = os.path.join(BASE_DIR, *partes)
    if os.path.exists(c1):
        return c1
    c2 = os.path.join(EXE_DIR, "_internal", *partes)
    if os.path.exists(c2):
        return c2
    return c1

STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
LOGO_PATH = os.path.join(STATIC_DIR, "logo.png")
CUOTA_MENSUAL = 25.0
MULTA_FALTA = 5.0
CAFE_TURNO = 1.50
CAFE_NORMAL = 3.00
MAX_SOCIOS = 69
BASE_PERIODO = (2026, 10)
ESTADOS_CIVILES = ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a", "Unión libre"]

app = Flask(__name__, template_folder=_recurso("templates"),
              static_folder=_recurso("static"))


def _clave_sesion():
    """Clave de firma de la cookie de sesión.

    Orden de precedencia:
      1. Variable de entorno ``SECRET_KEY`` (recomendado en despliegue).
      2. Archivo local ``clave_sesion.key`` junto a la base de datos.
      3. Si no existe ninguno, se genera una clave aleatoria y se guarda en ese
         archivo con permisos de solo lectura del propietario.

    La clave nunca se versiona: ``clave_sesion.key`` está en ``.gitignore``.
    """
    del_entorno = os.environ.get("SECRET_KEY")
    if del_entorno:
        return del_entorno

    ruta = os.path.join(BASE_DIR, "clave_sesion.key")
    try:
        with open(ruta, encoding="utf-8") as fh:
            guardada = fh.read().strip()
        if guardada:
            return guardada
    except OSError:
        pass

    nueva = secrets.token_urlsafe(48)
    try:
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write(nueva)
        os.chmod(ruta, 0o600)
    except OSError:
        # Disco de solo lectura (por ejemplo, un USB protegido): la clave vale
        # para esta ejecución y se avisa en lugar de impedir el arranque.
        print("[31Enero] Aviso: no se pudo guardar la clave de sesión en disco; "
              "las sesiones no sobrevivirán al reinicio.")
    return nueva


app.secret_key = _clave_sesion()


def _guardar_clave_inicial(clave):
    """Escribe en disco la clave inicial recién generada.

    Se usa solo la primera vez que se crea el usuario ``secretaria``. El archivo
    queda junto a la base de datos, fuera del control de versiones, y debe
    borrarse después de cambiar la clave desde ⚙ Config.
    """
    ruta = os.path.join(BASE_DIR, "clave_inicial.txt")
    try:
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write(
                "Sistema Asociación 31 de Enero\n"
                "Usuario: secretaria\n"
                f"Clave inicial: {clave}\n\n"
                "Cámbiela en ⚙ Config tras el primer inicio de sesión.\n"
                "Después de cambiarla puede borrar este archivo.\n"
            )
        os.chmod(ruta, 0o600)
        destino = ruta
    except OSError:
        # Si el disco no admite escritura, la clave solo se muestra por consola.
        destino = "(no se pudo escribir el archivo)"
    print(f"[31Enero] Clave inicial de 'secretaria': {clave}")
    print(f"[31Enero] También quedó registrada en {destino}")


# ---------- utils ----------
def cedula_valida(ced):
    """Valida cédula ecuatoriana: 10 dígitos + algoritmo módulo 10."""
    ced = (ced or "").strip()
    if len(ced) != 10 or not ced.isdigit():
        return False, "La cédula debe tener exactamente 10 dígitos numéricos."
    prov = int(ced[:2])
    if prov < 1 or prov > 24:
        return False, "Código de provincia inválido (01-24)."
    if int(ced[2]) >= 6:
        return False, "Tercer dígito inválido para cédula de persona natural."
    coef = [2,1,2,1,2,1,2,1,2]
    s = 0
    for i in range(9):
        v = int(ced[i]) * coef[i]
        s += v - 9 if v >= 10 else v
    dig = (10 - (s % 10)) % 10
    if dig != int(ced[9]):
        return False, "Dígito verificador incorrecto (cédula inválida)."
    return True, ""

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
    CREATE TABLE IF NOT EXISTS socios(
        cedula TEXT PRIMARY KEY, nombres TEXT NOT NULL, apellidos TEXT NOT NULL,
        fecha_nac TEXT DEFAULT '', nacionalidad TEXT DEFAULT 'Ecuatoriana',
        estado_civil TEXT DEFAULT '', domicilio TEXT DEFAULT '', telefono TEXT DEFAULT '',
        num_socio INTEGER UNIQUE, orden_lista INTEGER UNIQUE,
        estado TEXT DEFAULT 'ACTIVO', saldo_inicial REAL DEFAULT 0, fecha_registro TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS asistencia(
        id INTEGER PRIMARY KEY AUTOINCREMENT, cedula TEXT NOT NULL REFERENCES socios(cedula),
        fecha TEXT NOT NULL, estado TEXT NOT NULL, multa REAL DEFAULT 0,
        multa_estado TEXT DEFAULT 'PAGADO', UNIQUE(cedula, fecha));
    CREATE TABLE IF NOT EXISTS cafe_rifas(
        id INTEGER PRIMARY KEY AUTOINCREMENT, cedula TEXT NOT NULL REFERENCES socios(cedula),
        fecha TEXT NOT NULL, es_turno INTEGER DEFAULT 0, monto REAL DEFAULT 3.0,
        estado TEXT DEFAULT 'DEBE', comision INTEGER DEFAULT 1, UNIQUE(cedula, fecha));
    CREATE TABLE IF NOT EXISTS mensualidades(
        id INTEGER PRIMARY KEY AUTOINCREMENT, cedula TEXT NOT NULL REFERENCES socios(cedula),
        periodo TEXT NOT NULL, fecha_corte TEXT DEFAULT '', cuota REAL DEFAULT 25.0,
        pagado REAL DEFAULT 0, estado TEXT DEFAULT 'DEBE', UNIQUE(cedula, periodo));
    CREATE TABLE IF NOT EXISTS caja_chica(
        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT NOT NULL, tipo TEXT NOT NULL,
        concepto TEXT NOT NULL, monto REAL NOT NULL, periodo_ref TEXT DEFAULT '', cedula_ref TEXT DEFAULT '',
        doc TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS auditoria(
        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha_hora TEXT NOT NULL, accion TEXT NOT NULL,
        tabla TEXT DEFAULT '', cedula TEXT DEFAULT '', detalle TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS reuniones(
        fecha TEXT PRIMARY KEY, periodo TEXT DEFAULT '', estado TEXT DEFAULT 'ABIERTA',
        cerrada_en TEXT DEFAULT '', total_ing REAL DEFAULT 0, observacion TEXT DEFAULT '',
        titulo TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS usuarios(
        username TEXT PRIMARY KEY, pass_hash TEXT NOT NULL, nombre TEXT DEFAULT '');
    """)
    # sembrar logo inicial junto al exe para que Config lo pueda reemplazar
    try:
        semilla = os.path.join(EXE_DIR, "_internal", "static", "logo.png")
        if not os.path.exists(LOGO_PATH) and os.path.exists(semilla):
            import shutil as _sh
            _sh.copyfile(semilla, LOGO_PATH)
    except Exception:
        pass
    # Usuario inicial: la clave se genera al azar en el primer arranque y se
    # escribe una sola vez en clave_inicial.txt. No hay contraseña incrustada
    # ni en el código ni en los manuales.
    r = db.execute("SELECT 1 FROM usuarios WHERE username='secretaria'").fetchone()
    if not r:
        inicial = secrets.token_urlsafe(9)
        db.execute("INSERT INTO usuarios(username,pass_hash,nombre) VALUES(?,?,?)",
                   ("secretaria", generate_password_hash(inicial), "Secretaría"))
        _guardar_clave_inicial(inicial)
    # migración: columnas nuevas en BD ya creadas
    cols_reu = [c[1] for c in db.execute("PRAGMA table_info(reuniones)").fetchall()]
    if "titulo" not in cols_reu:
        db.execute("ALTER TABLE reuniones ADD COLUMN titulo TEXT DEFAULT ''")
    cols_caja = [c[1] for c in db.execute("PRAGMA table_info(caja_chica)").fetchall()]
    if "doc" not in cols_caja:
        db.execute("ALTER TABLE caja_chica ADD COLUMN doc TEXT DEFAULT ''")
    db.commit(); db.close()

def log(accion, tabla="", cedula="", detalle=""):
    try:
        db = get_db()
        quien = session.get("user", "secretaria")
        db.execute("INSERT INTO auditoria(fecha_hora,accion,tabla,cedula,detalle) VALUES(?,?,?,?,?)",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{accion} [{quien}]", tabla, cedula, detalle))
        db.commit()
    except Exception:
        pass

def login_required(f):
    @wraps(f)
    def w(*a, **kw):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*a, **kw)
    return w

# ---------- negocio ----------
def ultimo_sabado(year, month):
    cal = calendar.monthcalendar(year, month)
    sabs = [s[calendar.SATURDAY] for s in cal if s[calendar.SATURDAY] != 0]
    return date(year, month, sabs[-1]).isoformat()

def proximos_sabados(n=3):
    out, y, m = [], date.today().year, date.today().month
    if (y, m) < BASE_PERIODO: y, m = BASE_PERIODO
    for _ in range(n):
        out.append(ultimo_sabado(y, m))
        m += 1
        if m > 12: m, y = 1, y + 1
    return out

def comision_de_orden(orden):
    return (int(orden) - 1) // 7 + 1

def comision_turno_para_fecha(fecha_iso):
    y, m, _ = map(int, fecha_iso.split("-"))
    return (((y * 12 + m) - (BASE_PERIODO[0] * 12 + BASE_PERIODO[1])) % 10) + 1

def periodo_de_fecha(f): return f[:7]

import re
def parse_monto(raw, campo="monto"):
    """Acepta '25', '25.5', '25.50', '25,50', '$ 25,50'. Rechaza '25..50', '2.5.5', letras."""
    s = (str(raw) if raw is not None else "").strip().replace("$", "").replace(" ", "")
    if not s:
        return 0.0, ""
    if s.count(".") + s.count(",") > 1 or ("." in s and "," in s):
        # permitir solo "1.234,56"? No: formato local simple, rechazar doble separador salvo miles
        # aceptamos "1,234.56" miles? lo normalizamos
        t = s.replace(",", "")
        if not re.fullmatch(r"\d+(\.\d{1,2})?", t):
            return None, f"{campo} inválido ('{raw}'): use solo números con hasta 2 decimales, ej. 25.50"
        return round(float(t), 2), ""
    s = s.replace(",", ".")
    if not re.fullmatch(r"\d+(\.\d{1,2})?", s):
        return None, f"{campo} inválido ('{raw}'): use solo números con hasta 2 decimales, ej. 25.50"
    return round(float(s), 2), ""

def reordenar_alfabetico():
    """Orden de lista y N° socio automáticos por orden alfabético (apellidos, nombres)."""
    db = get_db()
    rows = db.execute("SELECT cedula FROM socios ORDER BY apellidos COLLATE NOCASE, nombres COLLATE NOCASE").fetchall()
    db.execute("UPDATE socios SET orden_lista = 1000 + orden_lista, num_socio = 1000 + num_socio")
    for i, r in enumerate(rows, start=1):
        db.execute("UPDATE socios SET orden_lista=?, num_socio=? WHERE cedula=?", (i, i, r["cedula"]))
    db.commit()

def es_reunion_ordinaria(fecha_iso):
    try:
        y, m, _ = map(int, fecha_iso.split("-"))
        return fecha_iso == ultimo_sabado(y, m)
    except Exception:
        return False

def sabados_ordinarios(desde=(2026, 10), n=15):
    out, y, m = [], desde[0], desde[1]
    for _ in range(n):
        out.append(ultimo_sabado(y, m))
        m += 1
        if m > 12: m, y = 1, y + 1
    return out

def deuda_socio(cedula):
    db = get_db()
    s = db.execute("SELECT * FROM socios WHERE cedula=?", (cedula,)).fetchone()
    if not s: return None
    mens = db.execute("SELECT COALESCE(SUM(cuota-pagado),0) FROM mensualidades WHERE cedula=? AND estado!='PAGADO'", (cedula,)).fetchone()[0]
    mens_pag = db.execute("SELECT COALESCE(SUM(pagado),0) FROM mensualidades WHERE cedula=?", (cedula,)).fetchone()[0]
    cafe_debe = db.execute("SELECT COALESCE(SUM(monto),0) FROM cafe_rifas WHERE cedula=? AND estado='DEBE'", (cedula,)).fetchone()[0]
    cafe_pag = db.execute("SELECT COALESCE(SUM(monto),0) FROM cafe_rifas WHERE cedula=? AND estado='PAGADO'", (cedula,)).fetchone()[0]
    multa_debe = db.execute("SELECT COALESCE(SUM(multa),0) FROM asistencia WHERE cedula=? AND multa_estado='DEBE'", (cedula,)).fetchone()[0]
    multa_pag = db.execute("SELECT COALESCE(SUM(multa),0) FROM asistencia WHERE cedula=? AND multa_estado='PAGADO' AND multa>0", (cedula,)).fetchone()[0]
    inicial = s["saldo_inicial"] or 0
    return {"socio": s, "mens_debe": round(mens,2), "cafe_debe": round(cafe_debe,2),
            "multa_debe": round(multa_debe,2), "inicial": round(inicial,2),
            "total_debe": round(mens+cafe_debe+multa_debe+inicial,2),
            "total_pagado": round(mens_pag+cafe_pag+multa_pag,2)}

# ---------- auth ----------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u, p = request.form.get("username","").strip(), request.form.get("password","")
        db = get_db()
        r = db.execute("SELECT * FROM usuarios WHERE username=?", (u,)).fetchone()
        if r and check_password_hash(r["pass_hash"], p):
            session["user"] = u
            log("LOGIN", "usuarios", u, "ingreso")
            return redirect(url_for("index"))
        flash("Usuario o clave incorrectos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    log("LOGOUT", "usuarios", session.get("user",""), "salida")
    session.clear()
    return redirect(url_for("login"))

@app.route("/salir")
@login_required
def salir():
    log("CERRAR PROGRAMA", "config", session.get("user",""), "apagado desde botón Salir")
    session.clear()
    import threading as _th
    _th.Timer(1.2, lambda: os._exit(0)).start()  # apaga servidor + ventana
    return render_template("salir.html", logo_exists=os.path.exists(LOGO_PATH))

@app.route("/config", methods=["GET","POST"])
@login_required
def config():
    db = get_db()
    if request.method == "POST":
        if "logo" in request.files and request.files["logo"].filename:
            f = request.files["logo"]
            ext = os.path.splitext(secure_filename(f.filename))[1].lower()
            if ext in (".png",".jpg",".jpeg"):
                f.save(LOGO_PATH)
                log("SUBIR LOGO","config","","logo actualizado")
                flash("Logo actualizado")
            else:
                flash("Formato inválido (use PNG o JPG)")
        if request.form.get("nueva_clave"):
            if len(request.form["nueva_clave"]) < 6:
                flash("La clave debe tener mínimo 6 caracteres")
            else:
                db.execute("UPDATE usuarios SET pass_hash=? WHERE username=?",
                           (generate_password_hash(request.form["nueva_clave"]), session["user"]))
                db.commit(); log("CAMBIO CLAVE","usuarios",session["user"],"clave actualizada")
                flash("Clave actualizada")
        return redirect(url_for("config"))
    return render_template("config.html", logo_exists=os.path.exists(LOGO_PATH),
                           user=session.get("user"), version=VERSION, revision=None)

def revision_integridad():
    """Devuelve lista de (ok, mensaje) con chequeos de consistencia."""
    db = get_db()
    res = []
    n = db.execute("SELECT COUNT(*) FROM socios WHERE estado='ACTIVO'").fetchone()[0]
    res.append((n <= MAX_SOCIOS, f"Socios activos: {n}/{MAX_SOCIOS}" + ("" if n <= MAX_SOCIOS else " ⚠ EXCEDE EL LÍMITE")))
    mal = db.execute("SELECT COUNT(*) FROM socios WHERE LENGTH(cedula)!=10").fetchone()[0]
    # en SQLite LIKE es case-insensitive para ASCII; GLOB sí distingue
    mal += db.execute("SELECT COUNT(*) FROM socios WHERE cedula GLOB '*[^0-9]*'").fetchone()[0]
    res.append((mal == 0, f"Cédulas con formato inválido: {mal}"))
    ords = [r[0] for r in db.execute("SELECT orden_lista FROM socios ORDER BY orden_lista").fetchall()]
    res.append((len(ords) == len(set(ords)) and ords == list(range(1, len(ords) + 1)),
                f"Orden de lista 1..{len(ords)} sin huecos ni duplicados" if ords else "Sin socios registrados"))
    nums = [r[0] for r in db.execute("SELECT num_socio FROM socios").fetchall()]
    res.append((len(nums) == len(set(nums)), f"N° de socio únicos: {len(nums)}"))
    for tabla in ("asistencia", "cafe_rifas", "mensualidades"):
        h = db.execute(f"SELECT COUNT(*) FROM {tabla} t LEFT JOIN socios s ON s.cedula=t.cedula WHERE s.cedula IS NULL").fetchone()[0]
        res.append((h == 0, f"Registros huérfanos en {tabla}: {h}"))
    neg = db.execute("SELECT COUNT(*) FROM mensualidades WHERE pagado<0 OR cuota<0").fetchone()[0]
    exc = db.execute("SELECT COUNT(*) FROM mensualidades WHERE pagado>cuota+0.001").fetchone()[0]
    res.append((neg == 0 and exc == 0, f"Mensualidades con valores raros: {neg + exc}"))
    mc = db.execute("SELECT COUNT(*) FROM caja_chica WHERE monto<=0").fetchone()[0]
    res.append((mc == 0, f"Movimientos de caja con monto ≤ 0: {mc}"))
    try:
        db.execute("PRAGMA quick_check").fetchone()
        res.append((True, "Estructura física de la base (quick_check): OK"))
    except Exception as e:
        res.append((False, f"quick_check: {e}"))
    return res

@app.route("/integridad")
@login_required
def integridad():
    res = revision_integridad()
    log("VERIFICAR INTEGRIDAD", "config", "", f"{sum(1 for ok, _ in res if ok)}/{len(res)} OK")
    return render_template("config.html", logo_exists=os.path.exists(LOGO_PATH),
                           user=session.get("user"), revision=res, version=VERSION)

@app.route("/respaldo")
@login_required
def respaldo():
    log("DESCARGAR RESPALDO", "config", "", "asociacion.db")
    return send_file(DB_PATH, as_attachment=True,
                     download_name=f"respaldo_31enero_{date.today().isoformat()}.db")

def pie_data(segmentos):
    """Arma datos para pastel CSS: [(etiqueta, valor, color)] -> {style, items, vacio}."""
    total = sum(v for _, v, _ in segmentos)
    if total <= 0:
        return {"style": "background:#ddd;", "parts": [], "vacio": True}
    grad, acc = [], 0.0
    parts = []
    for lab, val, col in segmentos:
        pct = val * 100.0 / total
        grad.append(f"{col} {acc:.1f}% {acc+pct:.1f}%")
        acc += pct
        parts.append({"lab": lab, "val": round(val, 2), "pct": round(pct, 1), "col": col})
    return {"style": f"background: conic-gradient({', '.join(grad)});", "parts": parts, "vacio": False}

# ---------- dashboard ----------
@app.route("/")
@login_required
def index():
    db = get_db()
    n = db.execute("SELECT COUNT(*) c FROM socios WHERE estado='ACTIVO'").fetchone()[0]
    hoy = date.today().isoformat()
    turno = comision_turno_para_fecha(hoy)
    dm = db.execute("SELECT COALESCE(SUM(cuota-pagado),0) FROM mensualidades WHERE estado!='PAGADO'").fetchone()[0]
    dc = db.execute("SELECT COALESCE(SUM(monto),0) FROM cafe_rifas WHERE estado='DEBE'").fetchone()[0]
    dmu = db.execute("SELECT COALESCE(SUM(multa),0) FROM asistencia WHERE multa_estado='DEBE'").fetchone()[0]
    ing = db.execute("SELECT COALESCE(SUM(monto),0) FROM caja_chica WHERE tipo='INGRESO'").fetchone()[0]
    gas = db.execute("SELECT COALESCE(SUM(monto),0) FROM caja_chica WHERE tipo='GASTO'").fetchone()[0]
    y, m = date.today().year, date.today().month
    if (y, m) < BASE_PERIODO: y, m = BASE_PERIODO
    us = ultimo_sabado(y, m)
    per = periodo_de_fecha(us)
    # avance reunión actual
    na = db.execute("SELECT COUNT(*) FROM asistencia WHERE fecha=?", (us,)).fetchone()[0]
    nf = db.execute("SELECT COUNT(*) FROM asistencia WHERE fecha=? AND estado='FALTA'", (us,)).fetchone()[0]
    cp = db.execute("SELECT COUNT(*) FROM cafe_rifas WHERE fecha=? AND estado='PAGADO'", (us,)).fetchone()[0]
    ct = db.execute("SELECT COUNT(*) FROM cafe_rifas WHERE fecha=?", (us,)).fetchone()[0]
    mp = db.execute("SELECT COALESCE(SUM(pagado),0),COUNT(*) FROM mensualidades WHERE periodo=?", (per,)).fetchone()
    reu = db.execute("SELECT * FROM reuniones WHERE fecha=?", (us,)).fetchone()
    estado_reu = reu["estado"] if reu else ("ABIERTA" if na else "SIN INICIAR")
    # top deudores
    socios_ = db.execute("SELECT cedula,nombres,apellidos FROM socios WHERE estado='ACTIVO'").fetchall()
    top = []
    for s in socios_:
        d = deuda_socio(s["cedula"])
        if d and d["total_debe"] > 0:
            top.append((s["cedula"], f"{s['apellidos']} {s['nombres']}", d["total_debe"]))
    top = sorted(top, key=lambda x: -x[2])[:5]
    max_top = top[0][2] if top else 1
    # pasteles espejo de las 5 tarjetas (CSS puro, sin internet)
    debe_total = round(dm + dc + dmu, 2)
    ini_total = db.execute("SELECT COALESCE(SUM(saldo_inicial),0) FROM socios WHERE estado='ACTIVO'").fetchone()[0] or 0
    ing_mens = db.execute("SELECT COALESCE(SUM(monto),0) FROM caja_chica WHERE tipo='INGRESO' AND concepto LIKE 'Mensualidad%'").fetchone()[0]
    ing_cafe = db.execute("SELECT COALESCE(SUM(monto),0) FROM caja_chica WHERE tipo='INGRESO' AND concepto LIKE 'Café%'").fetchone()[0]
    ing_mult = db.execute("SELECT COALESCE(SUM(monto),0) FROM caja_chica WHERE tipo='INGRESO' AND concepto LIKE 'Multa%'").fetchone()[0]
    ing_otr = max(ing - ing_mens - ing_cafe - ing_mult, 0)
    g_socios = pie_data([("Activos", n, "#0a7a2f"), ("Cupos libres", max(MAX_SOCIOS - n, 0), "#bbbbbb")])
    g_debe = pie_data([("Mensualidades $", dm, "#c0392b"), ("Café $", dc, "#e6a800"),
                       ("Multas $", dmu, "#2471a3"), ("Inicial $", ini_total, "#8e44ad")])
    g_ing = pie_data([("Mensualidad $", ing_mens, "#0a7a2f"), ("Café $", ing_cafe, "#e6a800"),
                      ("Multas $", ing_mult, "#2471a3"), ("Otros $", ing_otr, "#bbbbbb")])
    top_gastos = db.execute("SELECT concepto, SUM(monto) t FROM caja_chica WHERE tipo='GASTO' GROUP BY concepto ORDER BY t DESC LIMIT 4").fetchall()
    resto_g = max(gas - sum(r[1] for r in top_gastos), 0)
    segs_gas = [(r[0][:28], r[1], c) for r, c in zip(top_gastos, ["#c0392b", "#e67e22", "#8e44ad", "#2471a3"])]
    if resto_g > 0.005:
        segs_gas.append(("Otros", resto_g, "#bbbbbb"))
    g_gas = pie_data(segs_gas)
    g_saldo = pie_data([("Ingresos $", ing, "#0a7a2f"), ("Gastos $", gas, "#c0392b")])
    return render_template("index.html", n=n, turno=turno, debe=debe_total,
        ingresos=ing, gastos=gas, saldo=round(ing-gas,2), usab=us, hoy=hoy, periodo=per,
        na=na, nf=nf, cp=cp, ct=ct, mp=round(mp[0] or 0,2), mt=mp[1] or 0,
        estado_reu=estado_reu, top=top, max_top=max_top, proximos=proximos_sabados(3),
        logo_exists=os.path.exists(LOGO_PATH), user=session.get("user"),
        g_socios=g_socios, g_debe=g_debe, g_ing=g_ing, g_gas=g_gas, g_saldo=g_saldo)

# ---------- socios ----------
@app.route("/socios", methods=["GET","POST"])
@login_required
def socios():
    db = get_db()
    if request.method == "POST":
        ced = request.form.get("cedula","").strip()
        if len(ced) != 10 or not ced.isdigit():
            flash("Cédula inválida: debe tener exactamente 10 dígitos numéricos."); return redirect(url_for("socios"))
        ok, msg = cedula_valida(ced)
        if not ok:
            flash(f"Advertencia: {msg} (se guarda igual, verifique el número).")
        ec = request.form.get("estado_civil","")
        if ec and ec not in ESTADOS_CIVILES:
            flash("Estado civil inválido"); return redirect(url_for("socios"))
        fnac = request.form.get("fecha_nac","")
        if fnac:
            try:
                if fnac > date.today().isoformat():
                    flash("Fecha de nacimiento no puede ser futura"); return redirect(url_for("socios"))
            except Exception:
                flash("Fecha de nacimiento inválida"); return redirect(url_for("socios"))
        total = db.execute("SELECT COUNT(*) FROM socios").fetchone()[0]
        existe = db.execute("SELECT 1 FROM socios WHERE cedula=?", (ced,)).fetchone()
        if not existe and total >= MAX_SOCIOS:
            flash(f"Límite de {MAX_SOCIOS} alcanzado"); return redirect(url_for("socios"))
        monto_ini, err = parse_monto(request.form.get("saldo_inicial") or 0, "Deuda inicial")
        if err:
            flash(err); return redirect(url_for("socios"))
        prev = db.execute("SELECT orden_lista,num_socio FROM socios WHERE cedula=?", (ced,)).fetchone()
        if prev:
            n_ord, n_num = prev["orden_lista"], prev["num_socio"]
        else:
            mx = db.execute("SELECT MAX(orden_lista) m FROM socios").fetchone()[0]
            n_ord = n_num = (mx or 0) + 1
        try:
            db.execute("""INSERT OR REPLACE INTO socios(cedula,nombres,apellidos,fecha_nac,nacionalidad,
                        estado_civil,domicilio,telefono,num_socio,orden_lista,estado,saldo_inicial,fecha_registro)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (ced, request.form.get("nombres","").strip(), request.form.get("apellidos","").strip(),
                 fnac, request.form.get("nacionalidad","Ecuatoriana"), ec,
                 request.form.get("domicilio",""), request.form.get("telefono",""),
                 n_ord, n_ord,
                 request.form.get("estado","ACTIVO"), monto_ini,
                 datetime.now().strftime("%Y-%m-%d")))
            db.commit(); reordenar_alfabetico(); log("CREAR/ACTUALIZAR SOCIO","socios",ced,"CRUD (orden alfabético auto)")
            flash("Socio guardado (orden y N° asignados alfabéticamente)")
        except Exception as e:
            flash(f"Error: {e}")
        return redirect(url_for("socios"))
    q = request.args.get("q","").strip()
    if q:
        rows = db.execute("SELECT * FROM socios WHERE cedula LIKE ? OR nombres LIKE ? OR apellidos LIKE ? ORDER BY orden_lista",
                          (f"%{q}%",f"%{q}%",f"%{q}%")).fetchall()
    else:
        rows = db.execute("SELECT * FROM socios ORDER BY orden_lista").fetchall()
    out = [dict(r, comision=comision_de_orden(r["orden_lista"] or 1)) for r in (dict(x) for x in rows)]
    # edad
    for d in out:
        try:
            if d.get("fecha_nac"):
                fn = date.fromisoformat(d["fecha_nac"]); hoy = date.today()
                d["edad"] = hoy.year - fn.year - ((hoy.month, hoy.day) < (fn.month, fn.day))
            else: d["edad"] = ""
        except Exception: d["edad"] = ""
    return render_template("socios.html", socios=out, q=q, total=len(rows),
                           civiles=ESTADOS_CIVILES, hoy=date.today().isoformat(), user=session.get("user"))

@app.route("/socios/eliminar/<cedula>")
@login_required
def eliminar_socio(cedula):
    db = get_db()
    db.execute("UPDATE socios SET estado='INACTIVO' WHERE cedula=?", (cedula,))
    db.commit(); log("BAJA SOCIO","socios",cedula,"baja lógica")
    flash("Socio dado de baja (no se borra historial)")
    return redirect(url_for("socios"))

# ---------- reunion ----------
def reunion_cerrada(fecha):
    db = get_db()
    r = db.execute("SELECT * FROM reuniones WHERE fecha=?", (fecha,)).fetchone()
    return r is not None and r["estado"] == "CERRADA"

@app.route("/reunion", methods=["GET","POST"])
@login_required
def reunion():
    db = get_db()
    fecha = request.values.get("fecha") or ultimo_sabado(*([date.today().year, date.today().month] if (date.today().year,date.today().month)>=BASE_PERIODO else BASE_PERIODO))
    periodo = periodo_de_fecha(fecha)
    turno = comision_turno_para_fecha(fecha)
    acc = request.values.get("acc","")
    cerrada = reunion_cerrada(fecha)
    ordinaria = es_reunion_ordinaria(fecha)
    tipo_reu = "ORDINARIA (último sábado)" if ordinaria else "EXTRAORDINARIA (solo pasa lista)"
    bloqueo = " (REUNIÓN CERRADA - solo lectura)" if cerrada else ""

    if acc and cerrada and acc not in ("", "reabrir"):
        flash("Reunión cerrada: use Reabrir para corregir"); acc = ""
    if acc == "gen_asistencia":
        ss = db.execute("SELECT * FROM socios WHERE estado='ACTIVO' ORDER BY orden_lista").fetchall()
        for s in ss:
            db.execute("INSERT OR IGNORE INTO asistencia(cedula,fecha,estado,multa,multa_estado) VALUES(?,?,?,0,?)",
                       (s["cedula"], fecha, "PRESENTE", "PAGADO"))
        db.execute("INSERT OR IGNORE INTO reuniones(fecha,periodo,estado) VALUES(?,?,?)", (fecha, periodo, "ABIERTA"))
        db.commit(); log("GENERAR ASISTENCIA","asistencia","",f"fecha {fecha}")
        flash(f"Asistencia generada para {fecha}")
    elif acc == "gen_cafe":
        if not ordinaria:
            flash("Evento extraordinario: solo se pasa lista (no genera café)."); return redirect(url_for("reunion", fecha=fecha))
        ss = db.execute("SELECT * FROM socios WHERE estado='ACTIVO' ORDER BY orden_lista").fetchall()
        for s in ss:
            com = comision_de_orden(s["orden_lista"] or 1)
            es = 1 if com == turno else 0
            db.execute("INSERT OR IGNORE INTO cafe_rifas(cedula,fecha,es_turno,monto,estado,comision) VALUES(?,?,?,?,?,?)",
                       (s["cedula"], fecha, es, CAFE_TURNO if es else CAFE_NORMAL, "DEBE", com))
        db.execute("INSERT OR IGNORE INTO reuniones(fecha,periodo,estado) VALUES(?,?,?)", (fecha, periodo, "ABIERTA"))
        db.commit(); log("GENERAR CAFE","cafe_rifas","",f"fecha {fecha} turno C{turno}")
        flash(f"Café generado: C{turno} paga ${CAFE_TURNO}, resto ${CAFE_NORMAL}")
    elif acc == "gen_mens":
        if not ordinaria:
            flash("Evento extraordinario: solo se pasa lista (no genera mensualidad)."); return redirect(url_for("reunion", fecha=fecha))
        ss = db.execute("SELECT * FROM socios WHERE estado='ACTIVO'").fetchall()
        for s in ss:
            db.execute("INSERT OR IGNORE INTO mensualidades(cedula,periodo,fecha_corte,cuota,pagado,estado) VALUES(?,?,?,?,?,?)",
                       (s["cedula"], periodo, fecha, CUOTA_MENSUAL, 0, "DEBE"))
        db.execute("INSERT OR IGNORE INTO reuniones(fecha,periodo,estado) VALUES(?,?,?)", (fecha, periodo, "ABIERTA"))
        db.commit(); log("GENERAR MENSUALIDAD","mensualidades","",f"periodo {periodo}")
        flash(f"Mensualidades {periodo} generadas ($25 c/u)")
    elif acc == "set_asistencia" and request.method == "POST":
        ced, est = request.form["cedula"], request.form["estado"]
        multa = MULTA_FALTA if est == "FALTA" else 0
        db.execute("UPDATE asistencia SET estado=?,multa=?,multa_estado=? WHERE cedula=? AND fecha=?",
                   (est, multa, "DEBE" if multa else "PAGADO", ced, fecha))
        db.commit(); log(f"ASISTENCIA {est}","asistencia",ced,f"{fecha} multa {multa}")
    elif acc == "pagar_multa" and request.method == "POST":
        ced = request.form["cedula"]
        db.execute("UPDATE asistencia SET multa_estado='PAGADO' WHERE cedula=? AND fecha=?", (ced, fecha))
        db.execute("INSERT INTO caja_chica(fecha,tipo,concepto,monto,periodo_ref,cedula_ref,doc) VALUES(?,?,?,?,?,?,?)",
                   (fecha,"INGRESO",f"Multa falta {fecha}",MULTA_FALTA,periodo,ced,f"Socio {ced}"))
        db.commit(); log("PAGO MULTA","caja_chica",ced,fecha)
    elif acc == "pagar_cafe" and request.method == "POST":
        ced = request.form["cedula"]
        r = db.execute("SELECT * FROM cafe_rifas WHERE cedula=? AND fecha=?", (ced, fecha)).fetchone()
        if r and r["estado"] == "DEBE":
            db.execute("UPDATE cafe_rifas SET estado='PAGADO' WHERE cedula=? AND fecha=?", (ced, fecha))
            db.execute("INSERT INTO caja_chica(fecha,tipo,concepto,monto,periodo_ref,cedula_ref,doc) VALUES(?,?,?,?,?,?,?)",
                       (fecha,"INGRESO",f"Café/rifa {fecha}",r["monto"],periodo,ced,f"Socio {ced}"))
            db.commit(); log("PAGO CAFE","caja_chica",ced,f"{fecha} ${r['monto']}")
    elif acc == "pagar_mens" and request.method == "POST":
        ced = request.form["cedula"]
        abono, err = parse_monto(request.form.get("abono"), "Abono")
        if err:
            flash(err); return redirect(url_for("reunion", fecha=fecha))
        r = db.execute("SELECT * FROM mensualidades WHERE cedula=? AND periodo=?", (ced, periodo)).fetchone()
        if r and abono > 0:
            nuevo = (r["pagado"] or 0) + abono
            est = "PAGADO" if nuevo >= r["cuota"] else "PARCIAL"
            db.execute("UPDATE mensualidades SET pagado=?,estado=? WHERE cedula=? AND periodo=?", (nuevo, est, ced, periodo))
            db.execute("INSERT INTO caja_chica(fecha,tipo,concepto,monto,periodo_ref,cedula_ref,doc) VALUES(?,?,?,?,?,?,?)",
                       (fecha,"INGRESO",f"Mensualidad {periodo} abono",abono,periodo,ced,f"Socio {ced}"))
            db.commit(); log("PAGO MENSUALIDAD","caja_chica",ced,f"{periodo} abono {abono}")
    elif acc == "titulo" and request.method == "POST":
        tit = request.form.get("titulo","").strip()[:120]
        db.execute("INSERT INTO reuniones(fecha,periodo,estado,titulo) VALUES(?,?,?,?) "
                   "ON CONFLICT(fecha) DO UPDATE SET titulo=?",
                   (fecha, periodo, "ABIERTA", tit, tit))
        db.commit(); log("TITULO EVENTO","reuniones","",f"{fecha}: {tit}")
        flash("Título del evento guardado")
        return redirect(url_for("reunion", fecha=fecha))
    elif acc == "cerrar" and request.method == "POST":
        ing = db.execute("SELECT COALESCE(SUM(monto),0) FROM caja_chica WHERE fecha=? AND tipo='INGRESO'", (fecha,)).fetchone()[0]
        obs = request.form.get("observacion","")[:300]
        db.execute("INSERT INTO reuniones(fecha,periodo,estado,cerrada_en,total_ing,observacion) VALUES(?,?,?,?,?,?) "
                   "ON CONFLICT(fecha) DO UPDATE SET estado='CERRADA',cerrada_en=?,total_ing=?,observacion=?",
                   (fecha, periodo, "CERRADA", datetime.now().strftime("%Y-%m-%d %H:%M"), ing, obs,
                    datetime.now().strftime("%Y-%m-%d %H:%M"), ing, obs))
        db.commit(); log("CERRAR REUNION","reuniones","",f"{fecha} total ${ing} - {obs}")
        flash(f"Reunión {fecha} TERMINADA y guardada. Total cobrado: ${ing}. Ya no se puede editar.")
        return redirect(url_for("reunion", fecha=fecha))
    elif acc == "reabrir":
        db.execute("UPDATE reuniones SET estado='ABIERTA' WHERE fecha=?", (fecha,))
        db.commit(); log("REABRIR REUNION","reuniones","",fecha)
        flash("Reunión reabierta para correcciones")

    cerrada = reunion_cerrada(fecha)
    asist = db.execute("SELECT a.*,s.nombres,s.apellidos,s.orden_lista FROM asistencia a JOIN socios s ON s.cedula=a.cedula WHERE a.fecha=? ORDER BY s.orden_lista", (fecha,)).fetchall()
    cafes = db.execute("SELECT c.*,s.nombres,s.apellidos,s.orden_lista FROM cafe_rifas c JOIN socios s ON s.cedula=c.cedula WHERE c.fecha=? ORDER BY s.orden_lista", (fecha,)).fetchall()
    mens = db.execute("SELECT m.*,s.nombres,s.apellidos,s.orden_lista FROM mensualidades m JOIN socios s ON s.cedula=m.cedula WHERE m.periodo=? ORDER BY s.orden_lista", (periodo,)).fetchall()
    reu = db.execute("SELECT * FROM reuniones WHERE fecha=?", (fecha,)).fetchone()
    titulo = (reu["titulo"] if reu and reu["titulo"] else
              (f"Reunión ordinaria {periodo}" if ordinaria else "Evento extraordinario"))
    return render_template("reunion.html", fecha=fecha, periodo=periodo, turno=turno,
        asist=asist, cafes=cafes, mens=mens, cerrada=cerrada, reu=reu, bloqueo=bloqueo, user=session.get("user"),
        ordinaria=ordinaria, tipo_reu=tipo_reu, ordinarias=sabados_ordinarios(),
        titulo=titulo, logo_exists=os.path.exists(LOGO_PATH))

# ---------- consulta ----------
@app.route("/consulta")
@login_required
def consulta():
    ced = request.args.get("cedula","").strip()
    ctx, hist = None, {}
    if ced:
        ctx = deuda_socio(ced)
        if ctx:
            db = get_db()
            hist["asist"] = db.execute("SELECT * FROM asistencia WHERE cedula=? ORDER BY fecha DESC LIMIT 24", (ced,)).fetchall()
            hist["cafes"] = db.execute("SELECT * FROM cafe_rifas WHERE cedula=? ORDER BY fecha DESC LIMIT 24", (ced,)).fetchall()
            hist["mens"] = db.execute("SELECT * FROM mensualidades WHERE cedula=? ORDER BY periodo DESC LIMIT 24", (ced,)).fetchall()
    ncomp = ""
    if ctx:
        ncomp = f"CMP-{datetime.now().strftime('%Y%m%d')}-{ced[-4:]}"
    return render_template("consulta.html", ced=ced, ctx=ctx, hist=hist,
        ahora=datetime.now().strftime("%Y-%m-%d %H:%M"), ncomp=ncomp,
        logo_exists=os.path.exists(LOGO_PATH), user=session.get("user"))

# ---------- caja ----------
@app.route("/caja", methods=["GET","POST"])
@login_required
def caja():
    db = get_db()
    if request.method == "POST":
        tipo = request.form.get("tipo","GASTO")
        monto, err = parse_monto(request.form.get("monto"), "Monto")
        if err:
            flash(err)
        elif monto <= 0:
            flash("Monto debe ser mayor a 0")
        else:
            db.execute("INSERT INTO caja_chica(fecha,tipo,concepto,monto,periodo_ref,cedula_ref,doc) VALUES(?,?,?,?,?,?,?)",
                (request.form.get("fecha") or date.today().isoformat(), tipo,
                 request.form.get("concepto",""), monto, request.form.get("periodo_ref",""), "",
                 request.form.get("doc","")[:120]))
            db.commit(); log(f"CAJA {tipo}","caja_chica","",request.form.get("concepto",""))
            flash("Movimiento registrado")
        return redirect(url_for("caja", mes=request.args.get("mes","")))
    mes = request.args.get("mes","")
    if mes:
        rows = db.execute("SELECT * FROM caja_chica WHERE periodo_ref=? OR fecha LIKE ? ORDER BY fecha,id", (mes, f"{mes}%")).fetchall()
    else:
        rows = db.execute("SELECT * FROM caja_chica ORDER BY fecha DESC,id DESC LIMIT 200").fetchall()
    ing = sum(r["monto"] for r in rows if r["tipo"] == "INGRESO")
    gas = sum(r["monto"] for r in rows if r["tipo"] == "GASTO")
    return render_template("caja.html", rows=rows, ing=round(ing,2), gas=round(gas,2),
                           saldo=round(ing-gas,2), mes=mes, hoy=date.today().isoformat(), user=session.get("user"),
                           ahora=datetime.now().strftime("%Y-%m-%d %H:%M"), logo_exists=os.path.exists(LOGO_PATH))

# ---------- auditoria ----------
@app.route("/auditoria")
@login_required
def auditoria():
    db = get_db()
    fd, fh = request.args.get("desde",""), request.args.get("hasta","")
    fc, ft = request.args.get("cedula","").strip(), request.args.get("tipo","").strip()
    q, p = "SELECT * FROM auditoria WHERE 1=1", []
    if fd: q += " AND fecha_hora>=?"; p.append(fd)
    if fh: q += " AND fecha_hora<=?"; p.append(fh + " 23:59:59")
    if fc: q += " AND cedula LIKE ?"; p.append(f"%{fc}%")
    if ft: q += " AND accion LIKE ?"; p.append(f"%{ft}%")
    q += " ORDER BY id DESC LIMIT 500"
    return render_template("auditoria.html", rows=db.execute(q, p).fetchall(),
        desde=fd, hasta=fh, cedula=fc, tipo=ft, user=session.get("user"),
        ahora=datetime.now().strftime("%Y-%m-%d %H:%M"), logo_exists=os.path.exists(LOGO_PATH))

if __name__ == "__main__":
    init_db()
    print("Asociación 31 DE ENERO - http://localhost:5000 - backup: copiar asociacion.db")
    app.run(host="127.0.0.1", port=5000, debug=False)
