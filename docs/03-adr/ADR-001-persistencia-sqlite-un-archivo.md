# ADR-001 — Persistencia en un único archivo SQLite local

- **Estado:** Aceptada
- **Fecha:** 18/10/2026
- **Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
- **Decisores:** Equipo de desarrollo (S6) con la secretaria (S1)

## Contexto

El sistema es monousuario y 100 % offline (R4), con presupuesto $0 (R3) y 69 socios (R6). Necesita persistir socios, asistencia, café, mensualidades, caja, reuniones y auditoría con **saldos exactos** (E1, driver D1) y **trazabilidad** (E2, driver D2). Debe poder respaldarse y restaurarse sin conocimientos técnicos (E6).

## Decisión

Usar **SQLite** con **un único archivo** `asociacion.db`, sin ORM (`sqlite3` directo, consultas explícitas), con restricciones `UNIQUE(cedula, fecha)` y `UNIQUE(cedula, periodo)`, claves foráneas activas y baja lógica (`estado`) en lugar de borrado físico.

## Alternativas descartadas

- **MySQL / PostgreSQL local:** exige instalar y operar un servidor de base de datos; contradice R3 (costo) y R4 (simplicidad offline).
- **Excel / CSV:** sin transacciones ni restricciones de unicidad; riesgo alto de duplicados e inconsistencias en E1.

## Consecuencias

- **A favor:** cero instalación; el respaldo es copiar/descargar **un archivo** (E6); las restricciones `UNIQUE` y las transacciones locales garantizan E1 sin coordinar otros componentes; cero licencias (R3).
- **En contra:** acoplamiento al motor SQLite y límite práctico de escritura concurrente (irrelevante en monousuario); si la asociación creciera a operación multiusuario o en red, habría que migrar el motor y el modelo de despliegue.

## Vínculo

- Drivers **D1, D2**; escenarios **E1, E2, E6**; restricciones **R3, R4, R6**.
- Vista C4 nivel 2: relación **Aplicación → Base de datos · SQL** y **Base de datos → USB · respaldo**.
- Evidencia en el repositorio: modelo de datos (7 tablas) y prueba de integridad (9 chequeos).
