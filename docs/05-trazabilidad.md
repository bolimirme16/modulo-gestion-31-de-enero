# 05 · Matriz de trazabilidad punta a punta

**Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
**Módulo 8 · Automatización de proceso de software · Actividad autónoma Semana 4 — Informe, repositorio y pipeline**
**Versión:** v0.4.0 (hito H4) · **Fecha:** 06/11/2026
**Alcance:** requisito → escenario de calidad → criterio de aceptación → ADR → artefacto → commit o PR → *check* del pipeline.

> Esta matriz es la fuente única de verdad de la trazabilidad. Los identificadores **HU-01…HU-07**, **E1…E6**, **ADR-001…ADR-004** y **CA-0x.y** se usan con el mismo significado en `docs/01-contexto-y-drivers.md`, `docs/03-adr/`, `docs/07-historias-y-criterios.md` y el código. Si un identificador cambia, esta matriz debe cambiar en el mismo *pull request*.

---

## 1. Cómo se lee una fila

Cada fila se puede recorrer de izquierda a derecha y de derecha a izquierda sin eslabones rotos:

1. **Requisito / HU:** historia de usuario con su restricción o driver asociado.
2. **Escenario de calidad:** E1–E6 del dossier de arquitectura, con su medida numérica.
3. **Criterio de aceptación:** CA verificable que traduce el escenario a una prueba.
4. **ADR:** decisión que explica *por qué* el artefacto tiene esa forma.
5. **Artefacto:** archivo real del repositorio (no una copia en el informe).
6. **Commit / PR:** dónde entró el artefacto al historial.
7. **Pipeline:** paso y prueba que lo verifican en cada *pull request*.

---

## 2. Matriz principal

| HU | Requisito / driver | Escenario | Criterio de aceptación | ADR | Artefacto(s) | Commit / PR | Verificación en el pipeline |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **HU-01** Registro y mantenimiento de socios | R6 (máximo 69), D2 (protección de datos) | — | CA-01.1 límite de 69 · CA-01.2 cédula única · CA-01.3 baja lógica | [ADR-001](03-adr/ADR-001-persistencia-sqlite-un-archivo.md), [ADR-002](03-adr/ADR-002-reglas-financieras-cierre-auditoria.md) | [07-historias §HU-01](07-historias-y-criterios.md), [`api/openapi.yaml`](../api/openapi.yaml) (`POST /socios`), [`src/reglas.py`](../src/reglas.py), [`tests/test_socios.py`](../tests/test_socios.py), [`tests/test_api.py`](../tests/test_api.py) | `9813be5` (PR #1) | Paso **Pruebas (pytest)** → `tests/test_socios.py`, `tests/test_api.py` |
| **HU-02** Asistencia y multas por inasistencia | D1 (consistencia financiera), R2 | **E1** | CA-02.1 multa exacta de $5,00 · CA-02.2 un registro por socio y reunión · CA-02.3 reunión cerrada bloquea cambios | [ADR-002](03-adr/ADR-002-reglas-financieras-cierre-auditoria.md) | [`tests/test_asistencia.py`](../tests/test_asistencia.py), [`tests/test_e1_multa.py`](../tests/test_e1_multa.py), [`tests/features/asistencia.feature`](../tests/features/asistencia.feature), [`src/reglas.py`](../src/reglas.py) | `9813be5` (PR #1), `e949bc0` (PR #25) | Paso **Pruebas (pytest)** → `tests/test_e1_multa.py`, `tests/test_bdd.py` |
| **HU-03** Cobro del servicio de café | D1, R2 | **E1** | CA-03.1 tarifa $1,50 al grupo de turno y $3,00 al resto · CA-03.2 un cobro por socio y período | [ADR-002](03-adr/ADR-002-reglas-financieras-cierre-auditoria.md) | [`tests/test_cafe.py`](../tests/test_cafe.py), [`tests/features/cafe.feature`](../tests/features/cafe.feature), [`src/reglas.py`](../src/reglas.py) (`calcular_tarifa_cafe`) | `9813be5` (PR #1) | Paso **Pruebas (pytest)** → `tests/test_cafe.py`, `tests/test_bdd.py` |
| **HU-04** Cuota mensual y abonos parciales | D1, R2 | **E1** | CA-04.1 cuota de $25,00 · CA-04.2 abonos parciales exactos · CA-04.3 rechazo de sobrepago | [ADR-001](03-adr/ADR-001-persistencia-sqlite-un-archivo.md), [ADR-002](03-adr/ADR-002-reglas-financieras-cierre-auditoria.md) | [`tests/test_cuota.py`](../tests/test_cuota.py), [`src/reglas.py`](../src/reglas.py) (`registrar_cuota`, `estado_cuenta`) | `9813be5` (PR #1) | Paso **Pruebas (pytest)** → `tests/test_cuota.py` |
| **HU-05** Cierre bloqueante de caja | D1, D6 (corte y comprobante) | **E1** | CA-05.1 cierre en ≤ 2 s · CA-05.2 inmutabilidad tras el cierre · CA-05.3 corte = fondo + cobros − egresos | [ADR-002](03-adr/ADR-002-reglas-financieras-cierre-auditoria.md), [ADR-003](03-adr/ADR-003-monolito-local-monousuario.md) | [`tests/test_cierre.py`](../tests/test_cierre.py), [`tests/test_api.py`](../tests/test_api.py), [`src/reglas.py`](../src/reglas.py) (`cerrar_reunion`, `corte_caja`) | `9813be5` (PR #1) | Paso **Pruebas (pytest)** → `tests/test_cierre.py` |
| **HU-06** Consulta y comprobante | D4 (offline), D6 | **E5** | CA-06.1 consulta en ≤ 1 s · CA-06.2 comprobante con logo, firma y sello · CA-06.3 operación 100 % offline | [ADR-002](03-adr/ADR-002-reglas-financieras-cierre-auditoria.md), [ADR-003](03-adr/ADR-003-monolito-local-monousuario.md) | [`tests/test_api.py`](../tests/test_api.py), [`src/reglas.py`](../src/reglas.py) (`comprobante`), [`templates/consulta.html`](../templates/consulta.html) | `9813be5` (PR #1) | Paso **Pruebas (pytest)** → `tests/test_api.py` |
| **HU-07** Respaldo e integridad | D1, D5 | **E6** | CA-07.1 respaldo en ≤ 5 s · CA-07.2 nueve chequeos de integridad | [ADR-001](03-adr/ADR-001-persistencia-sqlite-un-archivo.md), [ADR-003](03-adr/ADR-003-monolito-local-monousuario.md) | [`tests/test_sistema.py`](../tests/test_sistema.py), [`src/reglas.py`](../src/reglas.py) (`verificar_integridad`, `crear_respaldo`) | `9813be5` (PR #1) | Paso **Pruebas (pytest)** → `tests/test_sistema.py` |

**Nota sobre el escenario E1 y el caso de defensa.** El proyecto no gestiona citas: su equivalente funcional es **registrar la asistencia de la reunión mensual y generar la multa de $5,00**. Por eso la prueba de aceptación que se usa como caso demostrativo es [`tests/test_e1_multa.py`](../tests/test_e1_multa.py), que cubre el mismo criterio que la rúbrica llama «reservar cita»: una operación de negocio con medida numérica exacta que debe pasar por el pipeline.

---

## 3. Escenarios de calidad → decisión → prueba

| Escenario | Driver | Medida verificable | ADR que lo respalda | Prueba o artefacto de verificación | Paso del pipeline |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **E1** Consistencia financiera | D1 | 0 inconsistencias y 100 % de saldos exactos; cierre ≤ 2 s | ADR-001, ADR-002 | [`tests/test_e1_multa.py`](../tests/test_e1_multa.py), [`tests/test_cierre.py`](../tests/test_cierre.py) | Pruebas (pytest) |
| **E2** Seguridad y datos | D2 | 100 % de accesos no autenticados denegados en ≤ 1 s | ADR-002 | [`docs/10-gobierno-del-repositorio.md`](10-gobierno-del-repositorio.md), [`docs/evidencias/10-auditoria-de-secretos.txt`](evidencias/10-auditoria-de-secretos.txt) | Lint + Bandit |
| **E3** Facilidad de cambio | D3 | ≤ 1 día-persona y 0 cambios en otros módulos | ADR-002, ADR-003 | [`src/reglas.py`](../src/reglas.py) (tarifas centralizadas), [`docs/03-adr/matriz-de-decision.md`](03-adr/matriz-de-decision.md) | Pruebas (pytest) |
| **E4** Operación offline | D4 | Arranque ≤ 6 s; `/login` 200 sin internet | ADR-003 | [`docs/proyecto/05-manual-de-uso-rapido.md`](proyecto/05-manual-de-uso-rapido.md) | Build de documentación |
| **E5** Desempeño de consulta | D5 | 95 % de consultas en ≤ 1 s con 69 socios | ADR-002 | [`tests/test_api.py`](../tests/test_api.py) | Pruebas (pytest) |
| **E6** Tolerancia a fallos | D1, D5 | 0 registros perdidos; 9 de 9 chequeos; respaldo ≤ 5 s | ADR-001, ADR-003 | [`tests/test_sistema.py`](../tests/test_sistema.py) | Pruebas (pytest) |

---

## 4. Requisitos de gobierno y automatización (SEM03–SEM04)

| Requisito | Artefacto que lo cumple | Evidencia | Commit / PR | Verificación |
| :--- | :--- | :--- | :--- | :--- |
| Todo cambio entra por rama y PR, no directo a `main` | [`CONTRIBUTING.md`](../CONTRIBUTING.md), [`.github/CODEOWNERS`](../.github/CODEOWNERS) | [`docs/10-gobierno-del-repositorio.md`](10-gobierno-del-repositorio.md) | PR #5 (`42dcaff`) | Protección de `main` (1 aprobación, `enforce_admins`) |
| `main` exige el *check* en verde | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | [`docs/evidencias/13-proteccion-y-checks.txt`](evidencias/13-proteccion-y-checks.txt) | `0d47b70`, PR #25 (`98e11c1`) | `Spectral + Ruff + pytest` obligatorio y *strict* |
| Conflicto deliberado documentado | [`docs/11-practica-de-conflicto.md`](11-practica-de-conflicto.md) | Historial del PR #7 | PR #7 (`2fe4894`), resolución `e64fc60` | Revisión del reporte (causa, marcadores, resolución, prevención) |
| Versiones SemVer alineadas a los hitos | [`CHANGELOG.md`](../CHANGELOG.md), etiquetas anotadas | *Releases* del repositorio | `v0.1.0` `v0.2.0` `v0.3.0` `v0.3.1` `v0.4.0` | Etiqueta sobre el commit del hito |
| Sin secretos ni credenciales versionados | [`SECURITY.md`](../SECURITY.md), [`.gitignore`](../.gitignore) | [`docs/evidencias/10-auditoria-de-secretos.txt`](evidencias/10-auditoria-de-secretos.txt) | PR #20 (`243db60`) | `git grep` de patrones + Bandit |
| Pipeline con *quality gates* | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | [`docs/evidencias/11-falla-provocada.txt`](evidencias/11-falla-provocada.txt) | PR #25 (`98e11c1`) | Lint, Bandit, Spectral, pytest y build de docs |
| Falla provocada y corregida | [`tests/test_e1_multa.py`](../tests/test_e1_multa.py) | Run rojo `42045339641` → run verde `42045483208` | `74cf8d2` → `e949bc0` (PR #25) | Historial de *checks* del PR #25 |

---

## 5. Verificación de identificadores

| Identificador | Dónde se define | Dónde se usa | Consistencia |
| :--- | :--- | :--- | :---: |
| **HU-01…HU-07** | [`docs/07-historias-y-criterios.md`](07-historias-y-criterios.md) §2 | Esta matriz, `tests/`, `src/reglas.py` | ✔ |
| **CA-0x.y** | [`docs/07-historias-y-criterios.md`](07-historias-y-criterios.md) §2 | Docstrings de `tests/test_*.py` | ✔ |
| **E1…E6** | [`docs/01-contexto-y-drivers.md`](01-contexto-y-drivers.md) §5 | Esta matriz, pruebas, `docs/09-informe-final.md` | ✔ |
| **ADR-001…ADR-004** | [`docs/03-adr/`](03-adr/) | Esta matriz, informe final, `README.md` | ✔ |
| **S1…S6, R1…R6, D1…D6** | [`docs/01-contexto-y-drivers.md`](01-contexto-y-drivers.md) §2–§4 | Dossier, ADR, esta matriz | ✔ |

---

## 6. Mantenimiento de la matriz

La matriz se actualiza en el mismo *pull request* que cambia un requisito, un escenario, un ADR o una prueba. La plantilla de PR incluye la casilla «trazabilidad actualizada» y el revisor debe comprobar que los identificadores de la fila nueva coinciden con los documentos enlazados. Si un enlace de esta matriz deja de resolver, el paso **Build de la documentación** falla y el PR no puede fusionarse: la trazabilidad también es un *quality gate*.
