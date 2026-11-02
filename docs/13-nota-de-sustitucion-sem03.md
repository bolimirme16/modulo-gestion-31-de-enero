# Nota de sustitución de participación — SEM03

**Hito:** H3 · v0.3.0 (parche v0.3.1) · Repositorio gobernado
**Período:** 25/10/2026 – 01/11/2026
**Fecha de la nota:** 01/11/2026

---

## 1. Hecho

Durante el hito H3 la integrante **Valery Lucero B.** no dispuso de acceso a internet
más allá de mensajería (WhatsApp). GitHub, el clon del repositorio, la edición de
archivos y la revisión de *pull requests* requieren conexión desde un navegador o un
cliente Git; ninguno de esos medios estuvo disponible para ella en el período.

En consecuencia **no abrió ningún pull request ni realizó ninguna revisión** en este
hito. Su único PR del módulo es el **#1**, `valery/toolchain`, fusionado el 23/10/2026
dentro del hito anterior (v0.2.0).

## 2. Autorización

Ante la imposibilidad de participar, la integrante **pidió expresamente al equipo que
asumiera su parte** para no perjudicar la entrega grupal. El equipo aceptó y deja
constancia aquí.

Esta nota no atribuye a la integrante ningún trabajo que no haya realizado. Su función
es la contraria: **impedir que el historial del repositorio sugiera una participación
que no existió**.

## 3. Qué se hizo y quién lo hizo

| Actividad | Responsable real |
|---|---|
| Gobernanza, CODEOWNERS y plantillas (PR #5) | Bolívar Valenzuela |
| Higiene del repositorio (PR #8) | Bolívar Valenzuela |
| Matriz Git vs SVN y ADR-004 (PR #13) | Bolívar Valenzuela |
| Revisión de dependencias con OSV (PR #15) | Bolívar Valenzuela |
| Conflicto deliberado y su resolución (PR #7) | Bolívar Valenzuela |
| Corrección de seguridad y del gobierno (PR #20) | Bolívar Valenzuela |
| Changelog, licencia y seguridad (PR #6) | José Miguel Guerrero |
| Registro de participación individual (PR #16) | José Miguel Guerrero |

Ninguna de estas filas se atribuye a Valery Lucero. La tabla de la sección 8 de
`docs/10-gobierno-del-repositorio.md` dice lo mismo.

## 4. Efecto sobre la rúbrica

La rúbrica de la actividad autónoma de la semana 3 pide, dentro del criterio de 30 %,
que **cada integrante** tenga al menos dos *pull requests* y dos revisiones cruzadas.

- **Bolívar Valenzuela:** 6 PR (#5, #7, #8, #13, #15, #20) y 2 revisiones (#6, #16). Cumple.
- **José Miguel Guerrero:** 2 PR (#6, #16) y 5 revisiones (#5, #7, #8, #13, #15). Cumple.
- **Valery Lucero:** 0 PR y 0 revisiones en H3. **No cumple**, y esta nota lo declara.

El equipo asume la consecuencia en la calificación de ese criterio antes que presentar
una participación que no ocurrió. Se deja a criterio del docente aceptar o no la
sustitución descrita en la sección 2.

## 5. Declaración de cumplimiento y solicitud

El entregable grupal está completo. Los seis criterios de la rúbrica tienen evidencia
verificable en el repositorio:

- **Estructura:** `README.md`, `CONTRIBUTING.md`, `.gitignore` y plantillas de issue y de PR.
- **Historial:** commits atómicos en Conventional Commits desde v0.1.0 y los ocho PR del hito
  vinculados a su issue con `Closes #n`.
- **Ramas y revisión:** ramas cortas, revisión cruzada en todos los PR y conflicto deliberado
  documentado con causa, marcadores, resolución y prevención.
- **Versiones:** v0.1.0, v0.2.0 y v0.3.0 sobre los commits de cada hito, más el parche v0.3.1.
- **Gobierno y seguridad:** `main` protegida, dependencias revisadas con OSV y auditoría de
  secretos con sus dos hallazgos corregidos.
- **Matriz y ADR:** siete dimensiones con dos referencias en APA y ADR-004 completo.

La parte asignada a la tercera integrante **no quedó vacía**: la asumió el equipo con su
autorización expresa y está entregada dentro de los mismos PR. No hay trabajo del hito sin
hacer. La causa es una limitación de conectividad acreditada —acceso únicamente a mensajería
durante todo el período—, no desinterés ni abandono.

**Solicitud al evaluador:** que al calificar se valore el entregable terminado y la
sustitución autorizada, y que una circunstancia de conectividad ajena al equipo no penalice a
quienes asumieron esa carga y la declararon por escrito en lugar de simularla.

El mínimo individual de dos PR y dos revisiones no se cumple para ella y no se simula. Esta
declaración no pretende alterar el historial: pide que se pondere el contexto antes de aplicar
la penalización, con los hechos a la vista para que la decisión sea informada.

## 6. Alcance de esta nota en el repositorio

El repositorio se entrega con la etiqueta **v0.3.1** sobre el commit `243db60`, que es
el estado verificado de `main` en el momento de la entrega. Esta nota viaja en la rama
`docs/cierre-sem03` y en el PR #22, pendiente de revisión; no altera el commit entregado.

---

**Declaración del equipo:** la información de esta nota es exacta y verificable contra
el historial de GitHub (`/pulls?state=all` y `/pulls/{n}/reviews`).
