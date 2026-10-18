# Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”

**Módulo 8 · Automatización de proceso de software (UPEC) · Actividad autónoma Semana 1**
**Hito:** H1 · **Versión:** v0.1.0 · **Fecha:** 18/10/2026

Repositorio de la aplicación de escritorio (100 % offline) para la administración de socios, reuniones, caja y auditoría de la asociación, junto con su documentación. El **dossier de arquitectura** se elabora conforme a ISO/IEC/IEEE 42010:2022 e ISO/IEC 25010:2023.

## Estructura del repositorio

```
.
├─ app.py, escritorio.py          # Aplicación Flask + escritorio (pywebview/waitress)
├─ templates/, static/, resources/ # Vistas, estilos e imágenes
├─ iniciar.bat, verificar.bat      # Ejecución (código) y verificación
├─ requirements.txt                # Dependencias de Python
├─ *.spec                          # Empaquetado PyInstaller
├─ docs/                           # ENTREGABLE · Dossier de arquitectura (SEM01)
│  ├─ 00-Dossier-de-arquitectura.md
│  ├─ 01-contexto-y-drivers.md
│  ├─ 02-vistas-c4/                # C4 nivel 1 y 2 (como código) + revisión cruzada
│  ├─ 03-adr/                      # ADR-001, ADR-002, ADR-003 y matriz de decisión
│  ├─ 04-registro-ia.md            # Registro de uso de IA
│  └─ proyecto/                    # Documentación técnica del sistema
│     ├─ 01-requerimientos-y-procesos.md
│     ├─ 02-arquitectura-y-diseno.md
│     ├─ 03-calidad-pruebas-despliegue.md
│     ├─ 04-manual-de-uso.md
│     └─ 05-manual-de-uso-rapido.md
```

## Entregable SEM01 — Dossier de arquitectura

| Pieza | Ruta |
|-------|------|
| Dossier consolidado | [`docs/00-Dossier-de-arquitectura.md`](docs/00-Dossier-de-arquitectura.md) |
| Contexto, stakeholders, restricciones, drivers y escenarios | [`docs/01-contexto-y-drivers.md`](docs/01-contexto-y-drivers.md) |
| Vistas C4 nivel 1 y 2 (como código) | [`docs/02-vistas-c4/`](docs/02-vistas-c4/) |
| Revisión cruzada de consistencia | [`docs/02-vistas-c4/revision-cruzada.md`](docs/02-vistas-c4/revision-cruzada.md) |
| ADR-001, ADR-002, ADR-003 y matriz de decisión | [`docs/03-adr/`](docs/03-adr/) |
| Registro de uso de IA | [`docs/04-registro-ia.md`](docs/04-registro-ia.md) |

## Trazabilidad S → D → E → ADR → vista

| Escenario | Driver | ADR que lo respalda | Vista C4 |
|-----------|--------|---------------------|----------|
| E1 Consistencia financiera | D1 | ADR-001, ADR-002, ADR-003 | Nivel 2: Aplicación ↔ Base de datos |
| E2 Seguridad y datos | D2 | ADR-002 | Nivel 2: Aplicación (login + auditoría) |
| E3 Facilidad de cambio | D3 | ADR-002, ADR-003 | Nivel 2: Aplicación |
| E4 Operabilidad offline | D4 | ADR-003 | Nivel 2: Splash → Servidor → Ventana |
| E5 Desempeño de consulta | D5 | ADR-002 | Nivel 2: Aplicación ↔ Impresora |
| E6 Tolerancia a fallos y respaldo | D1, D5 | ADR-001, ADR-003 | Nivel 2: Base de datos ↔ USB |

## Ejecución

- **Recomendada (programa):** ver [`docs/proyecto/05-manual-de-uso-rapido.md`](docs/proyecto/05-manual-de-uso-rapido.md).
- **Desde código:** `iniciar.bat` (requiere Python y `pip install -r requirements.txt`).

## Equipo

Alejandra Valeria Lucero Burbano · José Miguel Guerrero Tapia · Bolívar Alexander Valenzuela Mejía
Docente: MSc. José Luis Rodríguez
