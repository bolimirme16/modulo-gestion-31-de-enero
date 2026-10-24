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

## Declaración final del equipo

El análisis del contexto, los stakeholders, las restricciones, los drivers, los escenarios, la priorización, los pesos, la decisión de estilo y la cadena CASE son **de autoría del equipo**. La IA se usó **solo** para:

1. Redactar el borrador del código Mermaid de los diagramas C4 (**Google Gemini**).
2. Revisar el contenido del borrador y ayudar a encontrar errores y observaciones a corregir —incluido el contraste crítico de la decisión de estilo— (**Claude**).
3. Proponer alternativas de herramientas y detectar tareas omitidas en el mapa de toolchain (**Google Gemini / Claude**).
4. Redactar borradores del contrato OpenAPI, de los escenarios Gherkin, de la lógica de negocio y de las pruebas, siempre bajo verificación con Spectral, Ruff y pytest (**asistente de IA: OpenCode, DeepSeek V4.1 Flash**).

Toda salida fue **verificada** contra el análisis propio y la documentación del repositorio; lo no verificable se rechazó. El equipo asume la responsabilidad integral del contenido del dossier y los artefactos del proyecto.
