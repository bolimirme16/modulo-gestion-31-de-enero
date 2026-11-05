# 04 · Registro del uso de inteligencia artificial

**Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
**Actividad autónoma Semana 1 — Dossier de arquitectura · v0.1.0 · 18/10/2026**
**Actividad autónoma Semana 2 — Cadena CASE y Especificación · v0.2.0 · 25/10/2026**

> **Advertencia cumplida:** no se ingresaron datos personales (cédulas, nombres reales, domicilios, teléfonos), credenciales ni información confidencial de la asociación en ninguna herramienta de IA. Se usaron solo descripciones abstractas y cifras ya documentadas (montos y reglas).

---

## 1. Actividad autónoma · Semana 1 (Dossier de arquitectura)

### Actividad 1 · Borrador de los diagramas C4 como código (Mermaid)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Google Gemini (versión web, octubre de 2026) |
| **Prompt resumido** | “Actúa como asistente de documentación de arquitectura. Con esta descripción del sistema (secretaria única, monolito Flask + SQLite + pywebview + PyInstaller, offline, impresora y USB), genera un borrador de diagrama C4 **nivel 1** y **nivel 2** como código Mermaid (flowchart). Usa solo los elementos de la descripción; no agregues contenedores ni tecnologías; no mezcles niveles; cada relación con verbo y, en el nivel 2, la tecnología.” |
| **Salida** | Dos bloques Mermaid: contexto (personas y sistemas externos) y contenedores (splash, servidor, aplicación, base de datos, ventana). |
| **Cómo se verificó** | (1) Render del código en GitHub y en un editor Mermaid; (2) contraste elemento por elemento con la documentación técnica del repositorio (`docs/proyecto/02-arquitectura-y-diseno.md`, secciones 1–4); (3) revisión de nombres y tipos ([Persona], [Contenedor], [Sistema externo]); (4) revisión cruzada con otro equipo (`docs/02-vistas-c4/revision-cruzada.md`). |
| **Aceptado** | Estructura general de ambos niveles y la sintaxis Mermaid base. |
| **Modificado** | Se agregaron etiquetas de tecnología en las relaciones (p. ej. “HTTP local”, “SQL”, “WSGI”); se renombró “App” → “Aplicación” para unificar; se añadió “Directiva / Comisión de vigilancia” como actor. |
| **Rechazado** | Propuesta de representar a los 69 socios como nodos individuales (no interactúan directamente con el sistema); cualquier contenedor o tecnología inexistente (p. ej. broker, servicios en la nube, PostgreSQL). |

---

### Actividad 2 · Revisión del contenido y contraste crítico de la decisión de estilo

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Claude (Anthropic) (versión web, octubre de 2026) |
| **Prompt resumido** | “Actúa como revisor crítico del contenido de este dossier de arquitectura y abogado del diablo de su decisión de estilo. Señala errores, ambigüedades e incoherencias y observaciones para corregir; no reescribas el contenido ni propongas una arquitectura nueva. Con estos escenarios (E1–E6 con su medida), estas alternativas (A1 monolito local, A2 cliente-servidor en red, A3 microservicios en la nube), estos pesos y esta matriz, entrega una tabla con: objeción/riesgo, escenario afectado, alternativa ignorada o sesgo, y qué evidencia haría cambiar la decisión.” |
| **Salida** | Objeciones sobre el riesgo de pérdida de datos en un equipo local (E6), el sesgo de medir “costo” a favor del monolito y la posibilidad de que el crecimiento cambie la decisión. |
| **Cómo se verificó** | Cada objeción se contrastó con las medidas de los escenarios y con el análisis de sensibilidad de la matriz (paso 5 de `docs/03-adr/matriz-de-decision.md`). |
| **Aceptado** | La objeción del riesgo de pérdida de datos en E6 → se registró como **consecuencia en contra** del ADR-001 y ADR-003, e incluyó el respaldo `.db`. |
| **Modificado** | La objeción del posible crecimiento se incorporó como **punto de sensibilidad** (bajar el peso de “offline”, subir “facilidad de cambio”), mostrando que A1 sigue ganando pero con menor margen. |
| **Rechazado** | Sugerencia de adoptar microservicios “por modernidad”: contradice R3/R4/R5 y no está respaldada por ninguna medida de E1–E6. |

---

## 2. Actividad autónoma · Semana 2 (Cadena CASE y Especificación)

### Actividad 1 · Alternativas a las herramientas del mapa de toolchain (Sesión 4)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Google Gemini (versión web, octubre de 2026) |
| **Prompt resumido** | “Actúa como ingeniero de software senior y revisor crítico de herramientas CASE. No propongas un diseño nuevo ni cambies mi análisis: complétalo y contrástalo. Para la tarea de diseño de contratos/APIs, propón herramientas alternativas a Swagger Editor.” |
| **Salida** | Stoplight Studio como alternativa a Swagger Editor para el diseño visual de contratos OpenAPI. |
| **Cómo se verificó** | Instalación y revisión de la licencia y documentación oficial de Stoplight Studio. |
| **Aceptado** | Stoplight Studio como herramienta Upper CASE para el diseño de APIs. |
| **Modificado** | Se decidió probarla en paralelo con Swagger Editor; el equipo la clasifica como Upper CASE con un nivel de riesgo medio. |
| **Rechazado** | Propuestas de herramientas comerciales cerradas sin planes gratuitos viables para la asociación. |

---

### Actividad 2 · Tareas omitidas del proceso en el mapa de toolchain (Sesión 4)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Claude (Anthropic) (versión web, octubre de 2026) |
| **Prompt resumido** | “Actúa como revisor crítico de procesos de software. Revisa las tareas identificadas en las seis fases del proceso y detecta tareas de alto volumen u omitidas que sean repetitivas, frecuentes o propensas a error.” |
| **Salida** | Propuesta de incluir la tarea de escaneo automático de dependencias y vulnerabilidades en la fase de construcción/integración. |
| **Cómo se verificó** | Contraste directo con el proceso definido en el Paso 1 del proyecto y los requerimientos de seguridad. |
| **Aceptado** | La inclusión del escaneo de dependencias como candidata para fases posteriores (Lower CASE, riesgo medio). |
| **Modificado** | Se ajustó el posicionamiento para considerarla dentro de las mejoras incrementales tras el MVP. |
| **Rechazado** | Sugerencias de integrar herramientas de análisis dinámico pesado (DAST) debido al entorno completamente offline y local del sistema (`pywebview` + SQLite). |

---

### Actividad 3 · Borrador del contrato OpenAPI y de los escenarios Gherkin (Sesión 5)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Asistente de IA (agente de codificación en el repositorio: OpenCode, modelo DeepSeek V4.1 Flash; octubre de 2026) |
| **Prompt resumido** | “A partir de las 7 historias de usuario y sus criterios de aceptación de `docs/07-historias-y-criterios.md`, redacta un borrador de contrato OpenAPI 3.0.3 con al menos 4 operaciones para el sistema de la asociación. No incluyas la cédula en rutas ni en respuestas: identifica los recursos con un identificador interno. Propón el código HTTP de cada caso de error (404, 409, 403, 422).” |
| **Salida** | Borrador de `api/openapi.yaml` con 12 operaciones, esquemas y respuestas de error. |
| **Cómo se verificó** | (1) `spectral lint api/openapi.yaml` con el ruleset `spectral:oas` → **0 errores y 0 advertencias** (`docs/evidencias/02-spectral-lint.txt`); (2) contraste operación por operación con la matriz de trazabilidad de `docs/07-historias-y-criterios.md`; (3) generación de documentación, *mock* y *stubs* directamente desde el contrato. |
| **Aceptado** | Estructura general del contrato, las 12 operaciones y los códigos de error. |
| **Modificado** | El identificador del recurso pasó de `cedula` a `socioId` (UUID interno) en todas las rutas y esquemas; la identificación se conservó solo como campo `writeOnly` en el alta de socios. |
| **Rechazado** | El borrador (heredado del documento de planificación) exponía la cédula en `GET /socios/{cedula}` y en la respuesta del padrón: se **rechazó** por incumplir la minimización de datos (R1 / LOPDP). |

---

### Actividad 4 · Borrador de la lógica de negocio y de las pruebas (Sesión 6)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Asistente de IA (agente de codificación en el repositorio: OpenCode, modelo DeepSeek V4.1 Flash) |
| **Prompt resumido** | “Implementa la capa de reglas financieras (multa $5,00; café $1,50/$3,00; cuota $25,00; cierre bloqueante) sobre SQLite, y escribe pruebas unitarias y escenarios pytest-bdd derivados de los criterios de aceptación. No uses datos personales reales en las pruebas.” |
| **Salida** | `src/reglas.py`, `src/app.py`, `tests/` (unitarias, integración HTTP y BDD) y `tests/features/`. |
| **Cómo se verificó** | (1) `pytest` → **34 pruebas en verde** (`docs/evidencias/07-pytest.txt`); (2) `ruff check src tests` → *All checks passed!* (`docs/evidencias/06-ruff.txt`); (3) `tests/test_api.py` comprueba que el padrón **no** devuelve la cédula. |
| **Aceptado** | Estructura de la capa de reglas, el servicio Flask y los escenarios BDD. |
| **Modificado** | La primera corrida de `pytest` detectó un desajuste de claves (`grupo_turno` frente a `grupoTurno`) que hacía fallar el cobro de café; se corrigió en `src/reglas.py`. |
| **Rechazado** | Se descartó resolver las pruebas BDD con Cucumber.js (implica un segundo *runtime* de Node para probar código Python) y se mantuvo pytest-bdd, ya usado en el monolito. |

---

## 3. Actividad autónoma · Semana 3 (Repositorio gobernado, matriz Git vs SVN y ADR-004)

### Actividad 1 · Reglas de contribución, plantillas y protección de `main` (Sesión 7)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Asistente de IA (agente de codificación en el repositorio: OpenCode, modelo DeepSeek V4.1 Flash) |
| **Prompt resumido** | “Redacta las reglas de contribución del repositorio: roles, modelo de ramas, convención de commits, ciclo de revisión y *definition of done*. Añade `CODEOWNERS` y plantillas de *pull request* e issue cohe­rentes con el proyecto. No inventes integrantes ni áreas que no existan en el repositorio.” |
| **Salida** | `CONTRIBUTING.md`, `.github/CODEOWNERS`, `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/tarea.md`, `.github/ISSUE_TEMPLATE/defecto.md` y `docs/10-gobierno-del-repositorio.md` (PR #5). |
| **Cómo se verificó** | (1) `spectral lint api/openapi.yaml`, `ruff check src tests` y `pytest` en verde en la CI del PR; (2) revisión cruzada aprobada por José Miguel Guerrero; (3) contraste de cada regla con la configuración real de protección de `main` en GitHub. |
| **Aceptado** | Estructura de `CONTRIBUTING.md`, las plantillas y la tabla regla → evidencia de `docs/10-gobierno-del-repositorio.md`. |
| **Modificado** | La primera versión del cuerpo del PR incluía `Closes #2`, `Closes #3` y `Closes #4`, que habrían cerrado las historias de usuario sin implementarlas. Se eliminaron y se sustituyeron por una nota de alcance antes de fusionar. |
| **Rechazado** | Se descartó exigir dos aprobaciones por PR: con cuatro integrantes y trabajo asíncrono, bloquea la fusión sin aportar control adicional sobre un equipo de este tamaño. |

---

### Actividad 2 · Conflicto deliberado y su reporte (Sesiones 7 y 8)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Asistente de IA (agente de codificación en el repositorio: OpenCode, modelo DeepSeek V4.1 Flash) |
| **Prompt resumido** | “Diseña un conflicto de fusión real y reproducible entre dos ramas que modifiquen la misma línea, resuélvelo conservando las condiciones de ambas propuestas y documenta causa, marcadores, resolución y prevención.” |
| **Salida** | `docs/11-practica-de-conflicto.md`, las ramas `practica/conflicto-a` y `practica/conflicto-b`, los commits `c63833d` y `4196d2b`, el commit de fusión `e64fc60` y el PR #7. |
| **Cómo se verificó** | (1) `git merge` devolvió `CONFLICT (content): Merge conflict in docs/11-practica-de-conflicto.md`; (2) `git log --graph` muestra la bifurcación y el commit de fusión; (3) el archivo final no conserva marcadores `<<<<<<<`; (4) la CI del PR #7 pasó en verde. |
| **Aceptado** | El procedimiento y la tabla comparativa de las dos redacciones. |
| **Modificado** | La resolución propuesta inicialmente elegía la redacción de una sola rama; se reemplazó por una redacción que conserva las tres condiciones de ambas (frecuencia diaria, disparador de revisión y excepción por emergencia). |
| **Rechazado** | Se descartó provocar el conflicto sobre `src/reglas.py`: habría puesto en riesgo código con pruebas asociadas y el valor didáctico es el mismo sobre un documento. |

---

### Actividad 3 · Matriz Git vs SVN y ADR-004 (Sesión 8)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Asistente de IA (agente de codificación en el repositorio: OpenCode, modelo DeepSeek V4.1 Flash) |
| **Prompt resumido** | “Compara Git y Subversion en las siete dimensiones pedidas (modelo, historial, ramas, trabajo sin conexión, permisos, rendimiento y ecosistema) con apoyo en Chacon y Straub (2014) y Collins-Sussman et al. (2011), y redacta el ADR-004 con contexto, decisión, alternativa SVN, consecuencias y el caso en que SVN aplicaría. No atribuyas a ninguna fuente afirmaciones que no estén en la lectura.” |
| **Salida** | `docs/08-matriz-git-vs-svn.md` y `docs/03-adr/ADR-004-seleccion-git-como-scm.md`. |
| **Cómo se verificó** | (1) Contraste de cada fila de la matriz con los capítulos 1 y 2 de *Version Control with Subversion* y con *Pro Git*; (2) verificación de que las dos referencias están citadas en el texto y no solo listadas; (3) revisión de que el ADR incluya los cinco elementos exigidos y el caso de aplicación de SVN. |
| **Aceptado** | La estructura de siete dimensiones, la distinción entre permisos por ruta (SVN) y por rama (Git), y la sección «Cuándo aplicaría Subversion». |
| **Modificado** | La primera propuesta presentaba a Git como superior en todas las dimensiones; se corrigió para reconocer que SVN tiene una ventaja real (permisos por ruta) y explicar por qué no aplica a este contexto. |
| **Rechazado** | Se descartaron afirmaciones de rendimiento sin respaldo (comparaciones de velocidad en milisegundos): las fuentes no las sostienen y el proyecto no las midió. |

---

## 4. Actividad autónoma — Semana 4 (Informe, repositorio y pipeline)

### Actividad 1 · Pipeline CI con puertas de calidad y build de documentación

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Asistente de IA (agente de codificación en el repositorio: OpenCode, modelo DeepSeek V4.1 Flash; noviembre de 2026) |
| **Prompt resumido** | “Completa `.github/workflows/ci.yml` para que en cada PR ejecute lint, análisis estático, pruebas, validación del contrato OpenAPI con Spectral y build de la documentación. Usa permisos mínimos, acciones fijadas por versión y ningún secreto. Añade un script de build que falle si hay enlaces internos rotos.” |
| **Salida** | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml), [`scripts/build_docs.py`](../scripts/build_docs.py), `requirements-dev.txt` y las insignias de [`README.md`](../README.md). |
| **Cómo se verificó** | (1) Ejecución real del pipeline: run rojo `42045339641` y run verde `42045483208`; (2) `ruff check src tests scripts`, `bandit -q -r src -x src/generated -ll`, `pytest -q` y `python scripts/build_docs.py --out site` en local; (3) revisión de la configuración de protección de `main` por API. |
| **Aceptado** | Estructura de un solo trabajo con seis pasos, permisos `contents: read`, `persist-credentials: false` y nombres de paso explícitos. |
| **Modificado** | La propuesta inicial usaba `pull_request_target` y acciones por rama (`@main`). Se cambió a `pull_request` y a versiones fijas (`@v4`, `@v5`); también se movió el lint antes de las pruebas para dar retroalimentación más rápida. |
| **Rechazado** | Se descartó ejecutar `npm install -g @stoplight/spectral-cli` sin versión y publicar el artefacto de documentación con retención indefinida. |

### Actividad 2 · Informe final y matriz de trazabilidad

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Asistente de IA (OpenCode, DeepSeek V4.1 Flash) para el borrador; revisión y decisiones del equipo |
| **Prompt resumido** | “Integra en `docs/09-informe-final.md` la arquitectura, la cadena CASE, el versionamiento y la automatización, con análisis crítico y métricas DORA calculadas a partir del historial. Construye `docs/05-trazabilidad.md` con la cadena requisito → escenario → ADR → artefacto → commit/PR → pipeline, usando solo identificadores y archivos que existan en el repositorio.” |
| **Salida** | [`docs/09-informe-final.md`](09-informe-final.md) y [`docs/05-trazabilidad.md`](05-trazabilidad.md). |
| **Cómo se verificó** | (1) Cada enlace del informe y de la matriz se resuelve en el repositorio; (2) `python scripts/build_docs.py` construyó 25 documentos sin enlaces rotos; (3) los identificadores HU, CA, E y ADR se contrastaron con `docs/07-historias-y-criterios.md`, `docs/01-contexto-y-drivers.md` y `docs/03-adr/`; (4) las cifras DORA se recalcularon desde la API de GitHub. |
| **Aceptado** | La estructura de ocho secciones (a–h) y la separación entre “qué funcionó” y “qué quedó débil”. |
| **Modificado** | El borrador presentaba las métricas DORA como concluyentes; se corrigió para declarar que son proxies con una muestra de cinco versiones y sin despliegue a producción. |
| **Rechazado** | Se descartaron afirmaciones de mejora de productividad sin medición y cualquier dato personal de los socios. |

### Actividad 3 · Cálculo de métricas DORA

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Script propio sobre la API REST de GitHub (`/pulls`, `/actions/runs`) y `git log` |
| **Prompt resumido** | “Calcula frecuencia de despliegue, lead time, change failure rate y MTTR con los datos reales del repositorio. Explica la fórmula y el corte temporal de cada cifra.” |
| **Salida** | [`docs/evidencias/12-metricas-dora.txt`](evidencias/12-metricas-dora.txt) y la sección (f) del informe final. |
| **Cómo se verificó** | Recálculo independiente con `git log -1 --format='%cI'` para las etiquetas y con los campos `created_at`, `merged_at` y `conclusion` de la API; contraste de los run ID citados. |
| **Aceptado** | Las fórmulas y la distinción entre *change failure rate* de CI y de versiones. |
| **Modificado** | Se sustituyó la media del *lead time* por la mediana, porque un PR de 21,7 h distorsionaba el promedio. |
| **Rechazado** | Se descartó presentar la frecuencia de despliegue como si hubiera producción real. |

### Lista de verificación del workflow generado

| Verificación exigida | Resultado | Evidencia |
| :--- | :---: | :--- |
| Permisos mínimos | ✔ | `permissions: contents: read` en `ci.yml` |
| Acciones fijadas por versión | ✔ | `checkout@v4`, `setup-python@v5`, `setup-node@v4`, `upload-artifact@v4` |
| Herramientas fijadas por versión | ✔ | `@stoplight/spectral-cli@6.17.0`; `requirements-dev.txt` con versiones exactas |
| Ausencia de secretos | ✔ | No se usa `secrets.*`; auditoría en [`evidencias/10-auditoria-de-secretos.txt`](evidencias/10-auditoria-de-secretos.txt) |
| Ejecución real | ✔ | Runs `42045339641` (rojo) y `42045483208` (verde) |
| Sin datos personales | ✔ | Solo cédulas ficticias en `tests/` |

---

## Declaración final del equipo

El análisis del contexto, los stakeholders, las restricciones, los drivers, los escenarios, la priorización, los pesos, la decisión de estilo y la cadena CASE son **de autoría del equipo**. La IA se usó **solo** para:

1. Redactar el borrador del código Mermaid de los diagramas C4 (**Google Gemini**).
2. Revisar el contenido del borrador y ayudar a encontrar errores y observaciones a corregir —incluido el contraste crítico de la decisión de estilo— (**Claude**).
3. Proponer alternativas de herramientas y detectar tareas omitidas en el mapa de toolchain (**Google Gemini / Claude**).
4. Redactar borradores del contrato OpenAPI, de los escenarios Gherkin, de la lógica de negocio y de las pruebas, siempre bajo verificación con Spectral, Ruff y pytest (**asistente de IA: OpenCode, DeepSeek V4.1 Flash**).
5. Redactar el borrador de las reglas de contribución, plantillas y `CODEOWNERS`, verificados contra la configuración real de protección de `main` (**OpenCode, DeepSeek V4.1 Flash**).
6. Diseñar el ejercicio de conflicto deliberado y su reporte, verificado con `git log --graph` y la CI del PR #7 (**OpenCode, DeepSeek V4.1 Flash**).
7. Redactar el borrador de la matriz Git vs SVN y del ADR-004, contrastado con las dos fuentes de la actividad (**OpenCode, DeepSeek V4.1 Flash**).
8. Proponer el borrador del pipeline CI, del build de documentación y de las métricas DORA, verificado con ejecuciones reales y con la API de GitHub (**OpenCode, DeepSeek V4.1 Flash**).

Toda salida fue **verificada** contra el análisis propio y la documentación del repositorio; lo no verificable se rechazó. El equipo asume la responsabilidad integral del contenido del dossier y los artefactos del proyecto.
