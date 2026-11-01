# Historial de cambios

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el versionado
adopta [SemVer 2.0.0](https://semver.org/lang/es/). Las versiones `0.x` corresponden a los hitos
del módulo, mientras el producto está en desarrollo.

---

## [No publicado]

### Pendiente
- Módulo de reportes exportables a PDF.
- Respaldo automático a USB al cierre de caja.

---

## [0.3.0] — 2026-11-01 — Repositorio gobernado (SEM03)

### Añadido
- `CONTRIBUTING.md` con roles, modelo de ramas, convención de commits, ciclo de revisión y
  *definition of done*.
- `.github/CODEOWNERS` para asignar revisores por área.
- Plantilla de *pull request* y plantillas de issue (tarea y defecto).
- `LICENSE` (MIT), `SECURITY.md` y este `CHANGELOG.md`.
- `.gitattributes` y `.editorconfig` para normalizar finales de línea y estilo de edición.
- `docs/10-gobierno-del-repositorio.md`: modelo de gobierno y su trazabilidad.
- Sección «Gobierno del repositorio» e insignias de estado en el `README.md`.

### Cambiado
- La rama `main` queda protegida: sin push directo, con revisión obligatoria y CI en verde.
- Se elimina la rama `valery/toolchain`, ya fusionada en la versión 0.2.0.

### Seguridad
- Se refuerza la exclusión de bases de datos locales con datos personales en `.gitignore`.
- Se actualiza **Flask de 3.1.0 a 3.1.3** tras la revisión de dependencias con la API de OSV:
  cuatro avisos publicados sobre la versión anterior, cero sobre la nueva.
- Se registra la revisión de dependencias en `SECURITY.md` y su evidencia en
  `docs/evidencias/08-revision-dependencias.txt`.

---

## [0.2.0] — 2026-10-25 — Cadena CASE y especificación (SEM02)

### Añadido
- Contrato OpenAPI 3.0.3 con 12 operaciones (`api/openapi.yaml`).
- Esqueleto ejecutable: reglas financieras y servicio Flask montado en `/api/v1`.
- Pruebas unitarias, de integración HTTP y BDD con Gherkin (34 pruebas).
- Mapa de toolchain con priorización frecuencia × esfuerzo × riesgo (`docs/06-mapa-toolchain.md`).
- Historias de usuario y criterios de aceptación (`docs/07-historias-y-criterios.md`).
- Matriz de evaluación y selección de herramientas (`docs/08-matriz-evaluacion-seleccion.md`).
- Informe de la cadena CASE (`docs/09-informe-cadena-case.md`).
- Integración continua con Spectral, Ruff y pytest (`.github/workflows/ci.yml`).

### Cambiado
- Se renombran los documentos 05 y 06 a 06 y 07 para conservar el orden del índice.

---

## [0.1.0] — 2026-10-18 — Dossier de arquitectura (SEM01)

### Añadido
- Dossier de arquitectura conforme a ISO/IEC/IEEE 42010:2022 e ISO/IEC 25010:2023.
- Contexto, *stakeholders*, restricciones, *drivers* y escenarios de calidad E1–E6.
- Vistas C4 de nivel 1 y 2 como código, con revisión cruzada de consistencia.
- ADR-001, ADR-002, ADR-003 y matriz de decisión.
- Registro de uso de IA (`docs/04-registro-ia.md`).

---

## [0.0.0] — 2026-09 — Versión inicial del sistema

### Añadido
- Aplicación Flask + SQLite para socios, reuniones, caja y auditoría.
- Empaquetado de escritorio con PyInstaller y ejecución offline.
