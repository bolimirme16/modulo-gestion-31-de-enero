# C4 nivel 1 — Contexto del sistema (evidencia ADR-01)

Sistema: Módulo Gestión 31 de Enero. Sin tecnologías en este nivel.
Nombres consistentes con el ensayo y los ADR.

```mermaid
flowchart LR
  SEC(["Secretaria<br/>[Persona]"]) --> SIS[["Módulo Gestión 31 de Enero<br/>[Sistema]"]]
  SIS --> IMP[("Impresora<br/>[Sistema externo]<br/>comprobantes y cortes")]
  SIS --> USB[("USB<br/>[Sistema externo]<br/>respaldo .db")]
```

## Relaciones (verbo + propósito)

- Secretaria → Módulo: dirige reunión mensual, cobra, consulta, audita y respalda.
- Módulo → Impresora: imprime comprobantes CMP-fecha y cortes con logo, firmas y sello.
- Módulo → USB: exporta respaldo `.db` con fecha.

Fuente: `DOCUMENTO2 §2 Nivel 1`.
