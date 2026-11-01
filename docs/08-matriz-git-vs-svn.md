# Matriz comparativa Git vs SVN

- **Propósito:** fundamentar la selección del sistema de control de versiones (SCM) del proyecto
- **Decisión asociada:** [ADR-004](03-adr/ADR-004-seleccion-git-como-scm.md)
- **Fecha:** 01/11/2026

## 1. Criterio de la comparación

La comparación se hace sobre las siete dimensiones que exige la actividad, aplicadas al contexto
real del proyecto: un equipo de cuatro personas, presupuesto **$0**, una sola estación de trabajo
para la operadora y un repositorio que debe servir como **evidencia evaluable** de trabajo
colaborativo.

Las referencias base son **Chacon y Straub (2014)**, para el modelo distribuido de Git, y
**Collins-Sussman, Fitzpatrick y Pilato (2011)**, para el modelo centralizado de Subversion.

## 2. Matriz

| Dimensión | Git | Subversion (SVN) | Efecto en este proyecto |
|---|---|---|---|
| **Modelo de versionado** | **Distribuido**: cada clon es un repositorio completo con todo el historial; el servidor es un par más (Chacon & Straub, 2014, cap. 1). | **Centralizado**: existe un único repositorio con historia; el cliente solo guarda la copia de trabajo (Collins-Sussman et al., 2011, cap. 1). | El modelo distribuido permite que cada integrante trabaje y consulte el historial sin red, condición del equipo. |
| **Historial** | Grafo acíclico dirigido (DAG) de *commits* identificados por **SHA**; el historial es inmutable y verificable. | Serie de revisiones numeradas (`r1`, `r2`, …) sobre el árbol del servidor; cada revisión es un *snapshot* del árbol completo. | El SHA permite citar evidencia exacta en el informe (`f99cd76`, `e64fc60`); un número de revisión global no distingue autoría por rama. |
| **Ramas** | Punteros de bajo costo: crear, mover y borrar una rama es una operación local instantánea. | **Directorios** dentro del repositorio (`/trunk`, `/branches/*`, `/tags/*`); la rama es una copia del árbol en el servidor (Collins-Sussman et al., 2011, cap. 4). | Las ramas cortas del hito duraron horas y se borraron sin costo; en SVN cada una habría dejado un directorio permanente. |
| **Trabajo sin conexión** | Total: `commit`, `branch`, `log`, `diff` y `merge` funcionan sin red; solo `push` y `fetch` la requieren. | Parcial: la copia de trabajo permite editar y comparar, pero `commit`, `log` y cualquier operación de historial exigen el servidor. | El equipo trabaja en horarios distintos y sin red garantizada; en SVN un corte de conexión bloquea el registro del avance. |
| **Permisos** | Por repositorio y por rama, mediante reglas del servicio de alojamiento (protección de `main`, revisores obligatorios). | Permisos **por ruta** del árbol (`svn:authorization`), más finos que Git a nivel de archivo, pero dependientes de un servidor propio. | La protección de `main` en GitHub cubre la necesidad real: impedir el push directo y exigir revisión. |
| **Rendimiento** | Operaciones locales en memoria; `status`, `diff` y `log` no tocan la red. | Cada operación de historial consulta el servidor; el rendimiento depende de la latencia y de la carga del servidor central. | Con conexión doméstica variable, las operaciones locales son más predecibles. |
| **Ecosistema** | Estándar de facto: GitHub, GitLab, CI integrada, plantillas de PR, CODEOWNERS, *releases* y etiquetas verificables. | Maduro y estable, con herramientas sólidas (TortoiseSVN, VisualSVN), pero con menor oferta de servicios gratuitos e integración con CI moderna. | El hito exige PR con revisión cruzada, CI obligatoria y etiquetas SemVer: Git los ofrece sin costo en GitHub. |

## 3. Lectura de la matriz

Ninguna de las siete dimensiones favorece a SVN **en este contexto**. SVN gana en un punto
concreto —el control de permisos por ruta— pero ese control exige administrar un servidor propio,
lo que choca con la restricción de presupuesto $0 y con la ausencia de un administrador de
sistemas en el equipo.

Las tres dimensiones decisivas son:

1. **Trabajo sin conexión**, porque el equipo no tiene conectividad garantizada.
2. **Ramas de bajo costo**, porque el flujo aprobado en `CONTRIBUTING.md` se basa en ramas cortas
   y PR; en SVN cada rama es un directorio permanente en el servidor.
3. **Ecosistema**, porque la evaluación exige evidencia verificable de revisión cruzada, CI en
   verde y etiquetas SemVer, y GitHub las ofrece de forma nativa y gratuita.

## 4. Cuándo aplicaría Subversion

SVN seguiría siendo la elección correcta en escenarios que este proyecto **no** presenta:

- **Permisos por archivo o por carpeta** dentro de un mismo árbol, con auditoría centralizada de
  quién puede leer o escribir cada ruta, y sin depender de reglas del servicio de alojamiento.
- **Activos binarios grandes y cambiantes** (documentos, planos, imágenes) en un repositorio
  corporativo centralizado, donde la copia parcial o el bloqueo de archivos (`svn:needs-lock`)
  evita conflictos binarios irresolubles.
- **Organizaciones con un servidor propio obligatorio** por política de datos, que no pueden
  alojar el código en un servicio externo y ya cuentan con el personal para administrarlo.
- **Equipos que migran desde un SCM centralizado** y necesitan continuidad operativa antes que un
  cambio de modelo de trabajo.

## 5. Conclusión

Git es la elección del proyecto. La matriz no lo favorece por popularidad, sino porque tres de las
siete dimensiones —trabajo sin conexión, costo de rama y ecosistema de revisión— son exactamente
las que el flujo de trabajo del equipo necesita, y porque la única ventaja real de SVN (permisos
por ruta) queda fuera del alcance de un equipo sin servidor propio.

## Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion:
For Subversion 1.7*. O'Reilly Media. https://svnbook.red-bean.com
