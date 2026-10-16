# 01 · Contexto y drivers arquitectónicos

**Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
**Módulo 8 · Automatización de proceso de software · Actividad autónoma Semana 1 — Dossier de arquitectura**
**Versión:** v0.1.0 (hito H1) · **Fecha:** 18/10/2026
**Norma de referencia:** ISO/IEC/IEEE 42010:2022 (stakeholders → concerns → vistas) y ISO/IEC 25010:2023 (atributos de calidad).

> Los identificadores **S** (stakeholders), **R** (restricciones), **D** (drivers) y **E** (escenarios) se mantienen **sin cambios** en las vistas C4 y en los ADR para conservar la trazabilidad.

---

## 1. El caso

La Asociación “31 de Enero Narciza de Jesús” es una asociación de vivienda con 69 socios como máximo. Sus registros se llevaban en hojas físicas y cuadernos: cada último sábado del mes la secretaria tomaba lista al inicio, servía el café a mitad de reunión y cobraba las mensualidades al final, anotando todo a mano. Esto producía deudas poco claras, comprobantes inexistentes y cortes de caja difíciles de auditar.

El sistema digitaliza ese flujo con una sola operadora (la secretaria), **100 % local y offline**, costo cero en software y hardware:

- **Casos de uso:** gestionar socios; dirigir la reunión mensual (asistencia con multa, café por comisiones, mensualidades); consultar el estado de cuenta por cédula con comprobante imprimible; operar caja chica con corte; auditar movimientos; verificar integridad y respaldar; cerrar sesión y programa.
- **Elementos del sistema:** nómina de socios, asistencia/multas, café y rifas por comisión, mensualidades, caja chica, auditoría, comprobantes y cortes.
- **Sistemas externos:** impresora (comprobantes y cortes) y USB (respaldo).
- **Restricción de alcance:** solo gestión de socios y dinero de la asociación; no incluye contabilidad externa, nómina ni pagos en línea.

---

## 2. Stakeholders y concerns

Un *concern* es un interés del stakeholder sobre el sistema, **aún no un requisito ni una solución técnica**.

| ID | Stakeholder | Rol | Concerns principales | Influencia |
|----|-------------|-----|----------------------|------------|
| S1 | Secretaria | Operadora única del sistema y administradora funcional | Cobrar y cerrar la reunión sin errores; saldos correctos; operar sin conocimientos técnicos; proteger los datos de los socios | Alta |
| S2 | Socios / Asamblea (69) | Aportan dinero y reciben servicios | Que su pago quede registrado; comprobante claro de lo que deben; trato justo en café y multas; transparencia del corte | Alta |
| S3 | Directiva (presidencia/tesorería) | Decide y rinde cuentas | Que la caja cuadre; obtener el corte y reportes; cumplir el estatuto; costo mínimo | Media |
| S4 | Comisión de vigilancia | Auditoría interna | Rastrear quién hizo qué y cuándo; que no se borre el historial | Media |
| S5 | Responsable de protección de datos | Vela por el cumplimiento | Uso lícito de cédulas y datos personales; trazabilidad de accesos | Media |
| S6 | Equipo de desarrollo | Construye y mantiene | Facilidad de cambio; despliegue sencillo; bajo costo; pocas dependencias | Media |

**Conflicto de concerns (negociación):** S1 prioriza **rapidez** al cobrar en la cola final; S4/S5 priorizan **trazabilidad y control**. Se resuelve registrando automáticamente cada acción (auditoría) sin pasos manuales para la secretaria.

---

## 3. Restricciones y supuestos

| ID | Tipo | Restricción | Origen | Negociable |
|----|------|-------------|--------|------------|
| R1 | Legal | Los datos personales (cédulas, domicilio, teléfono) se tratan conforme a la LOPDP (Ecuador) | Normativa (verificar artículos en la fuente oficial) | No |
| R2 | Negocio | Una sola sesión mensual (último sábado); una reunión no admite dos cobros de café/mensualidad para el mismo socio y periodo; rotación de comisiones de 10 grupos | Estatuto / Asamblea | No |
| R3 | Económica | Presupuesto **$0** para software y hardware (solo open-source y equipos existentes) | Directiva | Parcial |
| R4 | Técnica | Operación en una sola PC con Windows, **monousuario** y **sin internet** | Infraestructura de la secretaría | Parcial |
| R5 | Organizacional | Equipo pequeño (3–4 personas) y plazo del módulo | Planificación del módulo | No |
| R6 | Negocio | Máximo **69 socios**; no se borra historial (baja lógica) | Estatuto / Asamblea | No |

**Supuestos adoptados** (a validar si cambia el contexto): la secretaria es la única operadora; no habrá pagos en línea; el respaldo se hace a un USB al cerrar cada reunión; la impresora es la de la oficina.

---

## 4. Drivers arquitectónicos

Los drivers son los factores que, si cambian, obligarían a cambiar la estructura del sistema. Se priorizan por **importancia** y **dificultad de lograrlos** (ISO/IEC 25010:2023).

| ID | Driver | Tipo (ISO 25010) | Origen | Importancia | Dificultad |
|----|--------|------------------|--------|-------------|------------|
| D1 | Consistencia financiera: multas, café y mensualidades calculados de forma exacta y con cierre que congela lo actuado | Fiabilidad | S1, S2, R2, R6 | Alta | Alta |
| D2 | Protección de datos personales y trazabilidad de accesos | Seguridad | S5, R1 | Alta | Media |
| D3 | Facilidad de cambio (tarifas y reglas en un único punto) y mantenibilidad | Mantenibilidad / Flexibilidad | S6, R3 | Media | Media |
| D4 | Operación local offline, de un solo usuario y sin instalación de dependencias | Usabilidad / Portabilidad | S1, R4 | Alta | Media |
| D5 | Desempeño y disponibilidad durante la reunión (consulta y cierre ágiles) | Eficiencia de desempeño / Disponibilidad | S1, S3 | Media | Baja |
| D6 | Función clave: corte de caja y comprobante imprimible con logo, firmas y sello | Adecuación funcional | S2, S3, R2 | Alta | Media |

**Priorización (importancia × dificultad):** D1 (Alta/Alta) → D2, D4, D6 (Alta/Media) → D3 (Media/Media) → D5 (Media/Baja). Los drivers de alta importancia y dificultad alta o media son los que más pesan en las decisiones.

---

## 5. Escenarios de calidad

Cada escenario tiene **seis partes** y **una sola** medida numérica comprobable. Los IDs E1–E6 se conservan en las vistas y los ADR.

### E1 — Consistencia financiera · driver D1

| Parte | Contenido |
|-------|-----------|
| Fuente | Secretaria |
| Estímulo | Cierra la sesión del último sábado del mes |
| Entorno | Reunión mensual normal, 69 socios, sin internet |
| Artefacto | Módulo Reunión (cálculo de multas/café/mensualidades) y cierre de sesión |
| Respuesta | Calcula los totales, aplica las reglas ($5,00 falta; café $1,50 turno y $3,00 resto; cuota $25,00), guarda y bloquea la edición |
| Medida | **0 inconsistencias** en el corte y **100 %** de saldos exactos; cierre en **≤ 2 s** |

### E2 — Seguridad · driver D2

| Parte | Contenido |
|-------|-----------|
| Fuente | Usuario no autenticado |
| Estímulo | Abre el programa o solicita una ruta protegida |
| Entorno | Operación normal |
| Artefacto | Capa de autenticación (login + `login_required`) |
| Respuesta | Deniega el acceso, redirige a `/login` y registra el intento en auditoría |
| Medida | **100 %** de accesos no autenticados denegados y registrados en **≤ 1 s** |

### E3 — Facilidad de cambio · driver D3

| Parte | Contenido |
|-------|-----------|
| Fuente | Directiva |
| Estímulo | Pide cambiar la cuota mensual o el monto del café |
| Entorno | Desarrollo |
| Artefacto | Capa de reglas financieras centralizada |
| Respuesta | El cambio se hace en un único punto sin tocar otras reglas ni pantallas |
| Medida | **≤ 1 día-persona** y **0 cambios** en los módulos de asistencia, consulta y caja |

### E4 — Usabilidad / operabilidad offline · driver D4

| Parte | Contenido |
|-------|-----------|
| Fuente | Secretaria |
| Estímulo | Abre el sistema en una PC nueva sin internet |
| Entorno | Sin conexión, PC con Windows |
| Artefacto | Ejecutable + splash + ventana interna (pywebview) |
| Respuesta | Abre en ventana propia, permite iniciar sesión y operar |
| Medida | Arranque **≤ 6 s**; `/login` responde **200** sin internet; **0** pasos de instalación de dependencias |

### E5 — Desempeño · driver D5

| Parte | Contenido |
|-------|-----------|
| Fuente | Secretaria |
| Estímulo | Consulta por cédula en la cola final (hasta 69 consultas seguidas) |
| Entorno | Reunión, cola final |
| Artefacto | Módulo Consulta |
| Respuesta | Muestra la ficha con lo que debe y lo pagado, más el comprobante |
| Medida | **95 %** de las consultas respondidas en **≤ 1 s** con 69 socios |

### E6 — Disponibilidad / tolerancia a fallos · drivers D1, D5 *(escenario nuevo)*

| Parte | Contenido |
|-------|-----------|
| Fuente | Fallo de energía o de disco |
| Estímulo | Corte durante la reunión o archivo de datos dañado |
| Entorno | Operación normal, sin internet |
| Artefacto | Persistencia SQLite + respaldo + verificación de integridad |
| Respuesta | No se pierden datos; al reabrir se detectan anomalías; el respaldo es restaurable |
| Medida | **0 registros perdidos** tras el reinicio; **9 de 9** chequeos de integridad; respaldo descargado en **≤ 5 s** |

> **E6 es nuevo:** aparece al comparar estilos (Práctica 03), al reconocer el riesgo de perder datos en un equipo local sin red (relacionado con D1 y D5).

---

## 6. Trazabilidad driver → escenario

| Driver | Escenarios |
|--------|-----------|
| D1 Consistencia financiera | E1, E6 |
| D2 Protección de datos / trazabilidad | E2 |
| D3 Facilidad de cambio | E3 |
| D4 Operación offline / usabilidad | E4 |
| D5 Desempeño / disponibilidad | E5, E6 |
| D6 Corte y comprobante | E1, E5 |

Todos los drivers quedan cubiertos por al menos un escenario; E1–E6 se representan en las vistas C4 (`docs/02-vistas-c4/`) y se respaldan en los ADR (`docs/03-adr/`).
