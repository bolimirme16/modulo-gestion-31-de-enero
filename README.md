# Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”

**Módulo 8 · Automatización de proceso de software (UPEC)**
**Hito H1 · v0.1.0 · 18/10/2026** — Dossier de arquitectura (SEM01)
**Hito H2 · v0.2.0 · 25/10/2026** — Cadena CASE y especificación (SEM02)

Repositorio de la aplicación de escritorio (100 % offline) para la administración de socios, reuniones, caja y auditoría de la asociación, junto con su documentación. El **dossier de arquitectura** se elabora conforme a ISO/IEC/IEEE 42010:2022 e ISO/IEC 25010:2023, y la **cadena CASE** conforme a ISO/IEC/IEEE 12207:2017 (procesos) e ISO/IEC 14102:2008 (evaluación y selección de herramientas).

## Estructura del repositorio

```
.
├─ app.py, escritorio.py           # Aplicación Flask + escritorio (pywebview/waitress)
├─ templates/, static/, resources/ # Vistas, estilos e imágenes
├─ iniciar.bat, verificar.bat       # Ejecución (código) y verificación
├─ requirements.txt                 # Dependencias de la aplicación
├─ requirements-dev.txt             # Dependencias de desarrollo y de la cadena CASE
├─ pytest.ini, ruff.toml            # Configuración de pruebas y de análisis estático
├─ .spectral.yaml                   # Reglas de lint del contrato OpenAPI
├─ *.spec                           # Empaquetado PyInstaller
├─ api/                             # ENTREGABLE SEM02 · Contrato OpenAPI 3.0.3
│  └─ openapi.yaml
├─ src/                             # ENTREGABLE SEM02 · Esqueleto ejecutable
│  ├─ reglas.py                     # Reglas financieras y acceso a SQLite
│  ├─ app.py                        # Servicio Flask montado en /api/v1
│  └─ generated/                    # Stubs derivados del contrato (OpenAPI Generator)
├─ tests/                           # ENTREGABLE SEM02 · Pruebas
│  ├─ features/                     # Escenarios Gherkin (.feature)
│  └─ test_*.py                     # Unitarias, integración HTTP y BDD
├─ docs/                            # ENTREGABLE · Documentación
│  ├─ 00-Dossier-de-arquitectura.md
│  ├─ 01-contexto-y-drivers.md
│  ├─ 02-vistas-c4/                 # C4 nivel 1 y 2 (como código) + revisión cruzada
│  ├─ 03-adr/                       # ADR-001, ADR-002, ADR-003 y matriz de decisión
│  ├─ 04-registro-ia.md             # Registro de uso de IA
│  ├─ 06-mapa-toolchain.md          # ENTREGABLE SEM02 · Mapa de toolchain
│  ├─ 07-historias-y-criterios.md   # ENTREGABLE SEM02 · HU + criterios (Gherkin)
│  ├─ 08-matriz-evaluacion-seleccion.md  # ENTREGABLE SEM02 · Matriz de selección
│  ├─ 09-informe-cadena-case.md     # ENTREGABLE SEM02 · Informe de la cadena CASE
│  ├─ api/                          # Documentación HTML generada desde el contrato
│  ├─ evidencias/                   # Transcripciones de ejecución (01–07)
│  └─ proyecto/                     # Documentación técnica del sistema
└─ .github/workflows/ci.yml         # Integración continua (Spectral + Ruff + pytest)
```

## Entregable SEM01 — Dossier de arquitectura

| Pieza | Ruta |
|-------|------|
| Dossier consolidado | [`docs/00-Dossier-de-arquitectura.md`](docs/00-Dossier-de-arquitectura.md) |
| Contexto, stakeholders, restricciones, drivers y escenarios | [`docs/01-contexto-y-drivers.md`](docs/01-contexto-y-drivers.md) |
| Vistas C4 nivel 1 y 2 (como código) | [`docs/02-vistas-c4/`](docs/02-vistas-c4/) |
| Revisión cruzada de consistencia | [`docs/02-vistas-c4/revision-cruzada.md`](docs/02-vistas-c4/revision-cruzada.md) |
| ADR-001, ADR-002, ADR-003 y matriz de decisión | [`docs/03-adr/`](docs/03-adr/) |
| Registro de uso de IA | [`docs/04-registro-ia.md`](docs/04-registro-ia.md) |

## Entregable SEM02 — Cadena CASE

| Pieza | Ruta |
|-------|------|
| Mapa de toolchain (tareas F×E×R y herramientas por fase) | [`docs/06-mapa-toolchain.md`](docs/06-mapa-toolchain.md) |
| Historias de usuario y criterios de aceptación (Gherkin) | [`docs/07-historias-y-criterios.md`](docs/07-historias-y-criterios.md) |
| Contrato OpenAPI 3.0.3 (12 operaciones) | [`api/openapi.yaml`](api/openapi.yaml) |
| Documentación generada del contrato | [`docs/api/index.html`](docs/api/index.html) |
| Esqueleto ejecutable (reglas + servicio) | [`src/reglas.py`](src/reglas.py), [`src/app.py`](src/app.py) |
| Pruebas (unitarias, integración y BDD) | [`tests/`](tests/) |
| Matriz de evaluación y selección de herramientas | [`docs/08-matriz-evaluacion-seleccion.md`](docs/08-matriz-evaluacion-seleccion.md) |
| Informe de la cadena CASE | [`docs/09-informe-cadena-case.md`](docs/09-informe-cadena-case.md) |
| Evidencias de ejecución | [`docs/evidencias/`](docs/evidencias/) |
| Registro de uso de IA | [`docs/04-registro-ia.md`](docs/04-registro-ia.md) |

## Trazabilidad S → D → E → ADR → vista

| Escenario | Driver | ADR que lo respalda | Vista C4 |
|-----------|--------|---------------------|----------|
| E1 Consistencia financiera | D1 | ADR-001, ADR-002, ADR-003 | Nivel 2: Aplicación ↔ Base de datos |
| E2 Seguridad y datos | D2 | ADR-002 | Nivel 2: Aplicación (login + auditoría) |
| E3 Facilidad de cambio | D3 | ADR-002, ADR-003 | Nivel 2: Aplicación |
| E4 Operabilidad offline | D4 | ADR-003 | Nivel 2: Splash → Servidor → Ventana |
| E5 Desempeño de consulta | D5 | ADR-002 | Nivel 2: Aplicación ↔ Impresora |
| E6 Tolerancia a fallos y respaldo | D1, D5 | ADR-001, ADR-003 | Nivel 2: Base de datos ↔ USB |

## Ejecución

- **Recomendada (programa):** ver [`docs/proyecto/05-manual-de-uso-rapido.md`](docs/proyecto/05-manual-de-uso-rapido.md).
- **Desde código:** `iniciar.bat` (requiere Python y `pip install -r requirements.txt`).

### Cadena CASE (SEM02)

```bash
# 1. Validar el contrato OpenAPI (T4)
spectral lint api/openapi.yaml

# 2. Generar la documentación y los stubs desde el contrato (T6)
openapi-generator-cli generate -i api/openapi.yaml -g html2 -o docs/api
openapi-generator-cli generate -i api/openapi.yaml -g python-flask -o src/generated/openapi-flask

# 3. Levantar el servidor simulado (T5)
prism mock api/openapi.yaml --port 4010

# 4. Lint y pruebas del esqueleto ejecutable (T7 y T8)
pip install -r requirements-dev.txt
ruff check src tests
pytest
```

## Equipo

Alejandra Valeria Lucero Burbano · José Miguel Guerrero Tapia · Bolívar Alexander Valenzuela Mejía
Docente: MSc. José Luis Rodríguez
