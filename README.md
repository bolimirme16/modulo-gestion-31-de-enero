# Dossier de arquitectura — Sistema de Gestión 31 de Enero

**Módulo 8 · Automatización de proceso de software (UPEC) · Actividad autónoma Semana 1**
**Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
**Hito:** H1 · **Versión:** v0.1.0 · **Fecha:** 18/10/2026

Este repositorio contiene el **dossier de arquitectura** del proyecto, conforme a ISO/IEC/IEEE 42010:2022 e ISO/IEC 25010:2023. El código y la documentación técnica previa viven en `DOCUMENTACION/`; el dossier de esta actividad vive en `docs/`.

## Contenido

| Pieza | Ruta |
|-------|------|
| Contexto, stakeholders, restricciones, drivers y escenarios | [`docs/01-contexto-y-drivers.md`](docs/01-contexto-y-drivers.md) |
| Vistas C4 nivel 1 y 2 (como código) | [`docs/02-vistas-c4/`](docs/02-vistas-c4/) |
| Revisión cruzada de consistencia | [`docs/02-vistas-c4/revision-cruzada.md`](docs/02-vistas-c4/revision-cruzada.md) |
| ADR-001, ADR-002, ADR-003 y matriz de decisión | [`docs/03-adr/`](docs/03-adr/) |
| Registro de uso de IA | [`docs/04-registro-ia.md`](docs/04-registro-ia.md) |

## Trazabilidad S → D → E → ADR → vista

| Escenario | Driver | ADR que lo respalda | Vista C4 |
|-----------|--------|---------------------|----------|
| E1 Consistencia financiera | D1 | ADR-001, ADR-002, ADR-003 | Nivel 2: Aplicación → Base de datos |
| E2 Seguridad y datos | D2 | ADR-002 | Nivel 2: Aplicación (login + auditoría) |
| E3 Facilidad de cambio | D3 | ADR-002, ADR-003 | Nivel 2: Aplicación |
| E4 Operabilidad offline | D4 | ADR-003 | Nivel 2: Splash → Servidor → Ventana |
| E5 Desempeño de consulta | D5 | ADR-002 | Nivel 2: Aplicación → Impresora |
| E6 Tolerancia a fallos y respaldo | D1, D5 | ADR-001, ADR-003 | Nivel 2: Base de datos → USB |

## Equipo

Alejandra Valeria Lucero Burbano · José Miguel Guerrero Tapia · Bolívar Alexander Valenzuela Mejía
Docente: MSc. José Luis Rodríguez
