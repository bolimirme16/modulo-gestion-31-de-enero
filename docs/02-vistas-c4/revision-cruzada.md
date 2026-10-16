# 02 · Revisión cruzada de consistencia (C4)

**Actividad:** intercambio entre equipos (Práctica 02, paso 4). Cada equipo entrega sus diagramas a otro equipo, que busca ambigüedades con la lista de control y devuelve los hallazgos.
**Artefactos revisados:** `c4-nivel1-contexto.md` y `c4-nivel2-contenedores.md` (v0.1.0).

## Lista de control (criterios)

1. ¿Cada elemento tiene **nombre y tipo** ([Persona], [Sistema], [Sistema externo], [Contenedor])?
2. ¿Cada relación tiene **etiqueta con verbo** y, en el nivel 2, la **tecnología**?
3. ¿Los **niveles C4 se mantienen separados** (sin contenedores en el nivel 1)?
4. ¿Los **nombres coinciden** entre diagramas, ADR y escenarios de calidad?
5. ¿El diagrama **se renderiza** sin errores en GitHub?

## Hallazgos y correcciones

| N.º | Hallazgo | Criterio incumplido | Decisión | Corrección aplicada |
|-----|----------|---------------------|----------|---------------------|
| 1 | La relación “Ventana interna ↔ Servidor” no indicaba el protocolo | Relaciones etiquetadas (2) | Modificar | Se agregó “Consume la UI - HTTP local” |
| 2 | El nivel 1 incluía la base de datos en un borrador | Niveles separados (3) | Modificar | La base de datos se movió al nivel 2 |
| 3 | Se usaban “App” y “Aplicación” para el mismo contenedor | Nombres consistentes (4) | Modificar | Se unificó a “Aplicación” en diagramas, ADR y escenarios |
| 4 | Faltaba el actor que audita (S3/S4) en el nivel 1 | Cobertura de stakeholders | Aceptar | Se agregó “Directiva / Comisión de vigilancia” |
| 5 | Tras el borrador IA, una flecha Aplicación → Base de datos no tenía etiqueta | Relaciones etiquetadas (2) | Modificar | Se agregó “Lee y escribe … - SQL” |

## Resultado del contraste

- **Aceptado:** cobertura de stakeholders S1, S3 y S4 en el nivel 1; separación estricta de niveles.
- **Modificado:** etiquetas de relación (hallazgos 1 y 5) y nombre del contenedor de aplicación (hallazgo 3).
- **Rechazado:** sugerencia de representar a los 69 socios como actores individuales (no interactúan directamente con el sistema; su concern se canaliza por la secretaria y el corte impreso).

**Evidencia de render:** ambos archivos se abrieron en GitHub y en un editor Mermaid; los bloques se mostraron sin errores de sintaxis.
