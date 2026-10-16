# ADR-001 — Monolito web local monousuario de código abierto

- **Estado:** Aceptada
- **Fecha:** 16/10/2026
- **Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”

## Contexto

Asociación de 69 socios, una sola operadora (secretaría), operación el último sábado del mes,
100 % offline y presupuesto $0 en software (RNF-01, RNF-02, RNF-03, RNF-06).
Drivers: costo operativo mínimo y operabilidad sin internet ni instalación de motores.
Ver `DOCUMENTO1` (RNF-01/02/03/06) y `DOCUMENTO2 §1`.

## Decisión

Monolito web local autocontenido: Python + Flask en un único `app.py`,
SQLite en un solo archivo `asociacion.db`, servidor waitress en hilo,
splash tkinter fullscreen, ventana pywebview (WebView2/Edge) fullscreen
sin URLs visibles, empaquetado PyInstaller onedir con icono.
Gráficos con CSS `conic-gradient` (offline, cero dependencias).

## Alternativas descartadas

- Nube / MySQL / PostgreSQL: exigen servidor, instalación y administración; 69 socios no lo justifican.
- Microservicios: red, concurrencia y observabilidad distribuida injustificadas para un monousuario secuencial.
- Electron: exige Node y pesa +150 MB.
- Tkinter puro: impresión de comprobantes pobre frente a HTML/CSS.

## Consecuencias

- A favor: respaldo = copiar/descargar 1 archivo `.db`; doble clic sin Python;
  impresión perfecta con logo, firmas y sello; $0 licencias.
  Protege **mantenibilidad** y **compatibilidad operativa** (ISO/IEC 25010:2023).
- En contra: escalado por partes limitado; acoplamiento en un solo ejecutable;
  migrar a distribuido obligaría a redefinir límites y despliegue (costo de cambio: muy caro).

## Vínculo

- RNF-01/02/03/06; C4 nivel 1 (contexto) y nivel 2 (contenedores) en `docs/02-vistas-c4/`.
- Escenario E1: arranque offline ≤ 6 s, `/login` 200 sin internet, respaldo `.db` con fecha.
- Evidencia: `DOCUMENTO2 §1` (tabla de 7 decisiones), `§2` (C4 N1/N2);
  pruebas P-12 (respaldo), P-14 (EXE splash → ventana → `/login` 200), P-15 (splash fullscreen).
