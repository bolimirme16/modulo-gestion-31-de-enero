# ADR-003 — Estilo: monolito web local monousuario de código abierto

- **Estado:** Aceptada
- **Fecha:** 18/10/2026
- **Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
- **Decisores:** Equipo de desarrollo (S6) con la secretaria (S1) y la directiva (S3)
- **Tipo de decisión:** decisión de **estilo arquitectónico** (una de las más difíciles de cambiar)

## Contexto

La asociación requiere **0 inconsistencias** en el corte (E1, driver D1), protección de datos y trazabilidad (E2, D2), operación **offline** en una sola PC (E4, D4), respaldo recuperable (E6), con un equipo de 3–4 personas (R5) y presupuesto **$0** (R3). La matriz ponderada (`matriz-de-decision.md`, paso 4) compara tres estilos y favorece **A1 con 4,60** frente a A2 (3,00) y A3 (2,40).

## Decisión

Adoptar un **monolito web local monousuario** de código abierto:

- **Aplicación:** Python + Flask en un único `app.py` con plantillas Jinja2 (MVC simplificado, sin ORM).
- **Servidor:** waitress en hilo, en la misma PC (:5000), sin consola.
- **Ventana:** pywebview (WebView2/Edge) en pantalla completa, sin exponer URLs.
- **Arranque:** splash con tkinter; **datos:** SQLite en un archivo `asociacion.db`.
- **Empaque:** PyInstaller (onedir) con icono; **gráficos:** CSS `conic-gradient` (offline).

## Alternativas descartadas

- **A2 Cliente-servidor con base de datos en red:** mejora el control central de acceso, pero contradice R3/R4 (servidor, instalación y red) y baja a 3,00; no aporta valor para una sola operadora.
- **A3 Microservicios en la nube:** ofrece mejor facilidad de cambio, pero su costo operativo y la consistencia distribuida son desproporcionados para el equipo y el contexto (2,40); exige internet, contra R4.

## Consecuencias

- **A favor:** protege E1 con una transacción local; E4 con operación 100 % offline; E6 con respaldo de un solo archivo; costo $0 (R3). Un solo despliegue que opera una sola persona (R5).
- **En contra:** menor escalabilidad y sin despliegue independiente por dominio; acoplamiento de persistencia, lógica e interfaz en un ejecutable; si la asociación pasara a multiusuario o multi-oficina, habría que **redefinir límites y despliegue** (punto de sensibilidad de la matriz).

## Vínculo

- Drivers **D1, D3, D4, D6**; escenarios **E1, E3, E4, E6**; restricciones **R3, R4, R5**.
- **Matriz ponderada** (`docs/03-adr/matriz-de-decision.md`): A1 = 4,60; A2 = 3,00; A3 = 2,40; sensibilidad: A1 se mantiene si la operación sigue siendo local.
- **Vista C4 nivel 2** (`docs/02-vistas-c4/c4-nivel2-contenedores.md`): el diagrama vigente **es** el estado posterior a esta decisión (un proceso Flask + un archivo SQLite; sin broker ni servicios separados).

## Actualización de vistas

El nivel 2 se revisó tras la decisión y **se mantiene** (la arquitectura de contenedores no cambia entre las alternativas respecto de lo ya representado para el monolito). Se deja constancia en este ADR de que la vista sigue vigente para la versión v0.1.0.
