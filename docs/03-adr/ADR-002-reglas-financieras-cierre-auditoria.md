# ADR-002 — Reglas financieras centralizadas, cierre bloqueante y auditoría

- **Estado:** Aceptada
- **Fecha:** 18/10/2026
- **Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
- **Decisores:** Equipo de desarrollo (S6) con la directiva (S3) y la comisión de vigilancia (S4)

## Contexto

Las reglas del dinero son determinantes y auditables: multa de $5,00 por falta; café a $1,50 en la comisión de turno (rotación de 10 grupos desde octubre de 2026) y $3,00 al resto; cuota de $25,00 desde el periodo 2026-10 con abonos parciales; comprobante imprimible con logo, firmas y sello; cierre mensual que congela lo actuado (E1, E5, driver D1/D6). La comisión de vigilancia exige rastrear quién hizo qué (E2, driver D2).

## Decisión

Centralizar las reglas en una **capa de servicio única** dentro de la aplicación (funciones de cálculo de comisión, deuda del socio, validación de cédula y montos, último sábado y reordenamiento alfabético), con:

- tabla `reuniones` en estado **ABIERTA / CERRADA**; al cerrar, se **bloquean cargos y pagos** (reapertura solo para corregir);
- **auditoría** filtrable por fecha + cédula + tipo, que registra usuario y detalle de cada acción;
- **baja lógica** (no se borra historial) y verificación de **integridad** con 9 chequeos.

## Alternativas descartadas

- **Lógica dispersa en plantillas/rutas:** cálculos inconsistentes entre pantallas; imposible garantizar E1.
- **Borrado físico de socios o movimientos:** rompe el historial y los comprobantes ya emitidos (contradice a S4).
- **Edición libre después del cierre:** invalida los cortes de caja y la auditoría.

## Consecuencias

- **A favor:** saldos deterministas y repetibles (E1); 0 comprobantes contradictorios; 100 % de acciones `CERRAR`/`PAGO` trazables (E2); errores detectables (huérfanos, sobrepagos).
- **En contra:** cambiar una tarifa exige una migración controlada porque afecta el historial; centralizar obliga a disciplina de “único punto de cambio” (sin duplicar reglas en la interfaz).

## Vínculo

- Drivers **D1, D2, D6**; escenarios **E1, E2, E5**; restricciones **R1, R2, R6**.
- Vista C4 nivel 2: contenedor **Aplicación → Base de datos** (reglas, unicidad y auditoría sobre SQLite).
- Evidencia en el repositorio: pruebas del flujo de cobro, del bloqueo por cierre y de detección de huérfanos/sobrepagos.
