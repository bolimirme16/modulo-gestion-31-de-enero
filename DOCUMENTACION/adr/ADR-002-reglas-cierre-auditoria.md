# ADR-002 — Reglas financieras centralizadas con cierre bloqueante y auditoría

- **Estado:** Aceptada
- **Fecha:** 16/10/2026
- **Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”

## Contexto

Reglas heterogéneas y auditables: multa $5,00 por falta; café $1,50 comisión de turno
(rotación de 10 grupos desde oct-2026) y $3,00 resto; cuota $25,00 desde 2026-10
con abonos parciales y deuda inicial por socio; comprobante `CMP-fecha` imprimible;
cierre mensual que congela lo actuado; bitácora filtrable.
Ver `DOCUMENTO1` (RF-05/06/07/08/12/13) y `DOCUMENTO2 §3–§4`.

## Decisión

Capa de servicio centralizada (`comision_de_orden`, `comision_turno_para_fecha`,
`ultimo_sabado`, `deuda_socio`, `reordenar_alfabetico`, `parse_monto`);
tabla `reuniones` (`ABIERTA/CERRADA`) que al cerrar bloquea cargos y pagos
(con reapertura solo para corregir); sin ORM (sqlite3 directo, 7 tablas);
`UNIQUE(cedula, fecha)` y `UNIQUE(cedula, periodo)`, FK activas, baja lógica;
auditoría con filtros fecha + cédula + tipo; `/integridad` con 9 chequeos.

## Alternativas descartadas

- Lógica dispersa en plantillas/rutas: cálculos inconsistentes entre pantallas.
- Borrado físico de socios/movimientos: rompe historial y comprobantes emitidos.
- Edición libre post-cierre: invalida cortes de caja y auditoría.

## Consecuencias

- A favor: saldos deterministas; 0 comprobantes contradictorios;
  100 % de acciones `CERRAR`/`PAGO` trazables; errores detectables (huérfanos, sobrepagos).
  Protege **fiabilidad** y **seguridad** (ISO/IEC 25010:2023) + adecuación funcional del comprobante.
- En contra: cambiar una tarifa altera historial (exige migración de datos);
  exige disciplina de único punto de cambio (costo de cambio: caro).

## Vínculo

- RF-05/06/07/08/12/13; escenarios E2 (cobro y cierre) y E3 (trazabilidad).
- C4 nivel 3 (Socios, Reunión, Consulta, Caja, Auditoría, Config) + modelo ER 7 tablas.
- Evidencia: `DOCUMENTO2 §2 N3`, `§3`, `§4`;
  pruebas P-04 (falta=$5, café turno $1,50, mensualidad $25),
  P-06 (cierre bloquea / reabrir corrige), P-08 (orden alfabético),
  P-11 (huérfano + sobrepago → REVISAR).
