# ADR-004 — Selección de Git como sistema de control de versiones

- **Estado:** Aceptada
- **Fecha:** 01/11/2026
- **Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
- **Decisores:** Equipo de desarrollo (S6)
- **Tipo de decisión:** decisión de **herramienta de infraestructura** (condiciona el flujo de trabajo y la evidencia del módulo)

## Contexto

El repositorio del proyecto debe funcionar como **repositorio gobernado**: estructura documentada,
historial convencional, ramas cortas, *pull requests* con revisión cruzada, conflicto deliberado
documentado, `main` protegida y versiones SemVer alineadas a los hitos.

El equipo cumple una restricción económica estricta (**presupuesto $0**, R3) y trabaja sin
conectividad garantizada, en horarios distintos y desde estaciones separadas. No hay un
administrador de sistemas dedicado ni un servidor propio disponible.

La comparación completa de las siete dimensiones está en
[`docs/08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md); este ADR registra la decisión que se
deriva de ella.

## Decisión

Adoptar **Git** como sistema de control de versiones, alojado en **GitHub** (repositorio público,
plan gratuito), con este modelo de trabajo:

- **Ramas cortas** creadas desde `main` y fusionadas por *pull request* el mismo día.
- **`main` protegida**: sin push directo, una aprobación de otra persona, conversaciones resueltas
  y la verificación `Spectral + Ruff + pytest` en verde como condición de fusión.
- **Commits convencionales** (Conventional Commits) y etiquetas anotadas `v0.1.0`, `v0.2.0` y
  `v0.3.0` sobre los commits de cada hito.
- **Revisión cruzada obligatoria**: quien abre el PR no puede aprobarlo.

## Alternativa considerada: Subversion (SVN)

Subversion se evaluó como alternativa real, no como descarte de trámite. Su modelo centralizado
ofrece **permisos por ruta** dentro de un mismo árbol (`svn:authorization`), algo que Git no tiene
de forma nativa, y un control de versiones de activos binarios más predecible mediante bloqueo de
archivos (Collins-Sussman et al., 2011).

Descartarla se justifica por tres razones concretas:

1. **Operación sin red.** En SVN, `commit`, `log` y cualquier consulta de historial requieren el
   servidor; el equipo no tiene conectividad garantizada y trabaja en franjas horarias distintas.
2. **Costo de rama.** Cada rama es un directorio permanente en el servidor; el flujo aprobado se
   basa en ramas que viven horas y se borran.
3. **Costo de infraestructura.** Sostener SVN exige un servidor propio y alguien que lo administre,
   lo que contradice la restricción de presupuesto $0 y la ausencia de un administrador.

## Consecuencias

**A favor**

- Operaciones de historial y de rama **locales**, independientes de la red.
- Ramas de costo cero, que hacen viable el flujo de rama corta descrito en `CONTRIBUTING.md`.
- Revisión cruzada, CI y etiquetas verificables sin costo en GitHub, lo que produce la evidencia
  que la evaluación exige (PR aprobados por una persona distinta del autor, *checks* en verde).
- Historial inmutable identificado por SHA, que permite citar evidencia exacta en el informe.

**En contra**

- **Sin permisos por ruta**: el control de acceso se delega en las reglas del servicio de
  alojamiento, que actúan por repositorio y por rama, no por archivo.
- Dependencia de un servicio externo (GitHub) para la revisión y la CI; una caída del servicio
  detiene la fusión, aunque no el trabajo local.
- Curva de aprendizaje mayor que la de un SCM centralizado para quien viene de SVN.
- Los binarios grandes se versionan completos; si el proyecto incorporara muchos, habría que
  evaluar Git LFS o replantear la decisión.

## En qué caso aplicaría SVN

Este ADR quedaría revisado si el proyecto cambiara en alguno de estos sentidos:

- La asociación exigiera que el código resida en un **servidor propio** por política de datos y
  contara con personal para administrarlo.
- Se necesitara **permisos por archivo o carpeta** con auditoría centralizada, más finos que la
  protección por rama.
- El repositorio pasara a concentrar **activos binarios grandes y cambiantes** que requieran
  bloqueo de archivos para evitar conflictos irresolubles.
- El equipo se integrara a una organización que ya opera SVN y la continuidad pesara más que el
  cambio de modelo de trabajo.

## Vínculo

- **Matriz comparativa:** [`docs/08-matriz-git-vs-svn.md`](../08-matriz-git-vs-svn.md), siete
  dimensiones con apoyo en Chacon y Straub (2014) y Collins-Sussman et al. (2011).
- **Reglas derivadas:** [`CONTRIBUTING.md`](../../CONTRIBUTING.md) (modelo de ramas y revisión),
  [`.github/CODEOWNERS`](../../.github/CODEOWNERS) (revisores por área) y
  [`docs/10-gobierno-del-repositorio.md`](../10-gobierno-del-repositorio.md) (trazabilidad de cada
  regla).
- **Evidencia de aplicación:** PR #5 (gobernanza), PR #6 (changelog y seguridad), PR #7 (conflicto
  deliberado resuelto en `e64fc60`) y PR #8 (higiene del repositorio).

## Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion:
For Subversion 1.7*. O'Reilly Media. https://svnbook.red-bean.com
