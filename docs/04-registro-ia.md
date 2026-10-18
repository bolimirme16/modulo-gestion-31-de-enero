# 04 · Registro del uso de inteligencia artificial

**Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
**Actividad autónoma Semana 1 — Dossier de arquitectura · v0.1.0 · 18/10/2026**

> **Advertencia cumplida:** no se ingresaron datos personales (cédulas, nombres reales, domicilios, teléfonos), credenciales ni información confidencial de la asociación en ninguna herramienta de IA. Se usaron solo descripciones abstractas y cifras ya documentadas (montos y reglas).

---

## Actividad 1 · Borrador de los diagramas C4 como código (Mermaid)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Google Gemini (versión web, octubre de 2026) |
| **Prompt resumido** | “Actúa como asistente de documentación de arquitectura. Con esta descripción del sistema (secretaria única, monolito Flask + SQLite + pywebview + PyInstaller, offline, impresora y USB), genera un borrador de diagrama C4 **nivel 1** y **nivel 2** como código Mermaid (flowchart). Usa solo los elementos de la descripción; no agregues contenedores ni tecnologías; no mezcles niveles; cada relación con verbo y, en el nivel 2, la tecnología.” |
| **Salida** | Dos bloques Mermaid: contexto (personas y sistemas externos) y contenedores (splash, servidor, aplicación, base de datos, ventana). |
| **Cómo se verificó** | (1) Render del código en GitHub y en un editor Mermaid; (2) contraste elemento por elemento con el Documento 2 del repositorio (`DOCUMENTACION/DOCUMENTO2_Arquitectura_y_Diseno.md`, secciones 1–4); (3) revisión de nombres y tipos ([Persona], [Contenedor], [Sistema externo]); (4) revisión cruzada con otro equipo (`docs/02-vistas-c4/revision-cruzada.md`). |
| **Aceptado** | Estructura general de ambos niveles y la sintaxis Mermaid base. |
| **Modificado** | Se agregaron etiquetas de tecnología en las relaciones (p. ej. “HTTP local”, “SQL”, “WSGI”); se renombró “App” → “Aplicación” para unificar; se añadió “Directiva / Comisión de vigilancia” como actor. |
| **Rechazado** | Propuesta de representar a los 69 socios como nodos individuales (no interactúan directamente con el sistema); cualquier contenedor o tecnología inexistente (p. ej. broker, servicios en la nube, PostgreSQL). |

---

## Actividad 2 · Contraste crítico de la decisión de estilo (abogado del diablo)

| Campo | Registro |
|-------|----------|
| **Herramienta y versión** | Claude (Anthropic) (versión web, octubre de 2026) |
| **Prompt resumido** | “Actúa como abogado del diablo de una decisión arquitectónica. No propongas una arquitectura nueva. Con estos escenarios (E1–E6 con su medida), estas alternativas (A1 monolito local, A2 cliente-servidor en red, A3 microservicios en la nube), estos pesos y esta matriz, entrega una tabla con: objeción/riesgo, escenario afectado, alternativa ignorada o sesgo, y qué evidencia haría cambiar la decisión.” |
| **Salida** | Objeciones sobre el riesgo de pérdida de datos en un equipo local (E6), el sesgo de medir “costo” a favor del monolito y la posibilidad de que el crecimiento cambie la decisión. |
| **Cómo se verificó** | Cada objeción se contrastó con las medidas de los escenarios y con el análisis de sensibilidad de la matriz (paso 5 de `docs/03-adr/matriz-de-decision.md`). |
| **Aceptado** | La objeción del riesgo de pérdida de datos en E6 → se registró como **consecuencia en contra** del ADR-001 y ADR-003, e incluyó el respaldo `.db`. |
| **Modificado** | La objeción del posible crecimiento se incorporó como **punto de sensibilidad** (bajar el peso de “offline”, subir “facilidad de cambio”), mostrando que A1 sigue ganando pero con menor margen. |
| **Rechazado** | Sugerencia de adoptar microservicios “por modernidad”: contradice R3/R4/R5 y no está respaldada por ninguna medida de E1–E6. |

---

## Declaración final del equipo

El análisis del contexto, los stakeholders, las restricciones, los drivers, los escenarios, la priorización, los pesos y la decisión de estilo son **de autoría del equipo**. La IA se usó **solo** para (1) redactar el borrador del código Mermaid de los diagramas C4, con **Google Gemini**, y (2) ejercer de revisor crítico (abogado del diablo) del borrador, con **Claude (Anthropic)**. Toda salida fue **verificada** contra el análisis propio y la documentación del repositorio; lo no verificable se rechazó. El equipo asume la responsabilidad del contenido del dossier.
