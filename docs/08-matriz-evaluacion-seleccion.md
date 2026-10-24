# 08 · Matriz de Evaluación y Selección de Herramientas CASE

**Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
**Módulo 8 · Automatización de proceso de software · Actividad autónoma Semana 2 — Cadena CASE**
**Versión:** v0.2.0 · **Fecha:** 25/10/2026
**Norma de referencia:** ISO/IEC 14102:2008 (evaluación y selección de herramientas CASE), ISO/IEC 25010:2023 (calidad del producto) y la Especificación OpenAPI 3.0.3.

> Esta matriz evalúa las herramientas candidatas del mapa de toolchain (`docs/06-mapa-toolchain.md`) sobre las tareas de mayor puntaje. Los puntajes se sustentan en la ejecución real registrada en `docs/evidencias/`, no en la documentación de los fabricantes.

---

## 1. Criterios de evaluación y pesos

| ID | Criterio | Qué mide | Peso |
| :--- | :--- | :--- | :---: |
| **C1** | Fidelidad al contrato | Qué tan bien el resultado respeta `api/openapi.yaml` (rutas, esquemas y códigos HTTP). | 25 % |
| **C2** | Esfuerzo de puesta en marcha | Instalación, dependencias (Node, Java, Docker) y curva de aprendizaje. | 15 % |
| **C3** | Calidad del resultado | Legibilidad, lint, seguridad del código generado e integridad del dato (OWASP, ISO/IEC 25010). | 20 % |
| **C4** | Integración con la cadena | Encaje con Spectral, Prism, pytest, Ruff y la integración continua. | 15 % |
| **C5** | Costo y licencia | Software libre y viable para el presupuesto de una asociación (restricción R3). | 10 % |
| **C6** | Riesgo de uso | Probabilidad e impacto de un resultado defectuoso y facilidad de verificación. | 15 % |
| | | **Total** | **100 %** |

Escala de puntuación: **1** (muy deficiente) a **5** (excelente). Puntaje ponderado = Σ (peso × puntaje); el máximo es 5,00 (equivalente a 100).

---

## 2. Matriz principal · Tarea T6 “Generar el código base del servicio desde el contrato”

| Herramienta | Categoría | C1 (25 %) | C2 (15 %) | C3 (20 %) | C4 (15 %) | C5 (10 %) | C6 (15 %) | **Ponderado** | **/100** |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **A1 · OpenAPI Generator CLI 7.26.0** | Lower CASE | 5 | 4 | 4 | 5 | 5 | 4 | **4,50** | **90** |
| **A2 · Plantilla manual en Python/Flask** | Sin automatizar | 3 | 3 | 4 | 2 | 5 | 2 | **3,10** | **62** |
| **A3 · Swagger Editor + escritura manual** | Upper CASE | 4 | 4 | 4 | 3 | 4 | 3 | **3,70** | **74** |
| **A4 · Asistente de IA (agente de codificación)** | IA | 4 | 5 | 3 | 3 | 4 | 2 | **3,50** | **70** |

### Justificación de los puntajes (con evidencia)

* **A1 · OpenAPI Generator CLI (90).** Genera documentación (`-g html2`), *stubs* (`-g python-flask`) y modelos directamente del contrato: **C1 = 5** porque las 12 operaciones quedaron idénticas a `api/openapi.yaml` (ver `docs/evidencias/04-openapi-generator-stubs.txt`); **C2 = 4** porque exige Java Temurin 17 además de Node; **C3 = 4** porque el código generado es consistente pero debe revisarse (no aplica la minimización de datos por sí solo); **C4 = 5** porque su salida es la entrada natural de Prism, pytest y Ruff; **C5 = 5** (Apache-2.0); **C6 = 4** (riesgo medio: un contrato defectuoso se propaga, pero Spectral lo contiene antes).
* **A2 · Plantilla manual (62).** **C2 = 3** y **C3 = 4** (control total del estilo), pero **C4 = 2** porque no se conecta automáticamente con el contrato y **C6 = 2** porque reintroduce el trabajo manual que la cadena CASE busca eliminar.
* **A3 · Swagger Editor + manual (74).** Buen editor y previsualización (**C1 = 4**, **C2 = 4**), pero la transcripción manual del contrato al código mantiene riesgo de desincronización (**C4 = 3**, **C6 = 3**).
* **A4 · Asistente de IA (70).** Rápido para arrancar (**C2 = 5**), pero **C3 = 3** y **C6 = 2** (el riesgo más alto) porque produce resultados plausibles pero no verificados: en esta iteración el asistente propuso un esquema que devolvía la cédula en el padrón y el equipo lo **rechazó** (detalle en `docs/04-registro-ia.md`). Solo es admisible bajo revisión humana y pruebas automatizadas.

**Selección T6:** **A1 (OpenAPI Generator CLI)** como herramienta principal, **complementada con A4 (asistente de IA)** únicamente para redactar borradores de documentación y pruebas, siempre con verificación por Spectral, Ruff y pytest. **A2 y A3** se descartan como mecanismo principal por su bajo encaje con la cadena.

---

## 3. Matriz complementaria · Tarea T7 “Pruebas BDD de la regla financiera”

| Herramienta | Categoría | C1 (25 %) | C2 (15 %) | C3 (20 %) | C4 (15 %) | C5 (10 %) | C6 (15 %) | **Ponderado** | **/100** |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **pytest + pytest-bdd** | Lower CASE | 5 | 4 | 4 | 5 | 5 | 4 | **4,50** | **90** |
| **Cucumber.js** | Lower CASE | 4 | 3 | 4 | 2 | 4 | 3 | **3,40** | **68** |
| **Pruebas unitarias escritas por IA** | IA | 4 | 5 | 3 | 3 | 4 | 2 | **3,50** | **70** |

* **pytest/pytest-bdd (90).** **C1 = 5**: los escenarios de `tests/features/` son la versión ejecutable de los criterios de aceptación de `docs/07-historias-y-criterios.md`; **C4 = 5**: comparte el mismo intérprete del monolito Flask; verificado con **34 pruebas en verde** (`docs/evidencias/07-pytest.txt`).
* **Cucumber.js (68).** **C4 = 2** porque introduce un segundo *runtime* (Node) para probar código Python, duplicando dependencias.
* **IA (70).** Acelera la redacción (**C2 = 5**) pero mantiene **C6 = 2**: exige revisión humana y pruebas de regresión.

**Selección T7:** **pytest + pytest-bdd**, con la IA como apoyo de redacción y el humano como responsable de la verificación.

---

## 4. Matriz complementaria · Tarea T8 “Linter y análisis estático”

| Herramienta | C1 | C2 | C3 | C4 | C5 | C6 | **Ponderado** | **/100** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ruff 0.15.21** | 5 | 5 | 4 | 5 | 5 | 4 | **4,60** | **92** |
| **Flake8** | 4 | 5 | 3 | 4 | 5 | 4 | **4,05** | **81** |
| **Pylint** | 4 | 4 | 5 | 4 | 5 | 3 | **4,20** | **84** |

**Selección T8:** **Ruff**, por velocidad, ejecución en un solo comando y resultado limpio (`All checks passed!` en `docs/evidencias/06-ruff.txt`); Flake8 y Pylint quedan como alternativas documentadas en el mapa.

---

## 5. Decisión consolidada y gestión de riesgos

| Tarea | Herramienta seleccionada | Resultado | Riesgo principal | Mitigación |
| :--- | :--- | :--- | :--- | :--- |
| T4 (Diseñar) | Spectral 6.17.0 | 0 errores / 0 advertencias | Contrato que incumple OAS 3.0.3 | Puerta de calidad: `spectral lint` obligatorio antes de generar. |
| T6 (Construir) | OpenAPI Generator CLI 7.26.0 | Documentación, *stubs* y *mock* coherentes | Código generado sin minimización de datos | Revisión OWASP + pruebas de no exposición de cédula (`tests/test_api.py`). |
| T7 (Probar) | pytest + pytest-bdd | 34 pruebas en verde | Pruebas que no cubren la regla financiera | Criterios de aceptación trazados a Gherkin y a `src/reglas.py`. |
| T8 (Probar) | Ruff 0.15.21 | Lint limpio | Defectos de estilo antes de la revisión | Ejecución en cada *commit* (integración continua). |
| Apoyo | Asistente de IA | Borradores revisados | Resultados no verificados (p. ej., fuga de cédula) | Verificación humana + Spectral + Ruff + pytest. |

**Conclusión.** La selección combina una herramienta **Upper CASE** (Spectral/Swagger para el contrato), una **Lower CASE** (OpenAPI Generator y pytest para construir y probar) y una **I-CASE** (GitHub Actions y *Pull Requests* para integrar), con un **asistente de IA** acotado a borradores bajo verificación. Ninguna herramienta se adopta por su popularidad: cada una supera el umbral de aceptación sobre la base de la evidencia de ejecución de esta iteración.
