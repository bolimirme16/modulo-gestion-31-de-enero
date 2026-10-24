# Especificación de Historias de Usuario y Criterios de Aceptación BDD (Gherkin)

**Proyecto:** Sistema de Gestión Automatizada y Auditoría para la Asociación "31 de Enero Narciza de Jesús"  
**Módulo:** Módulo 8 - Automatización de proceso de software (Maestría en Ingeniería de Software - UPEC)  
**Artefacto:** `docs/07-historias-y-criterios.md`  
**Versión:** v0.2.0 (Hito H2 - Cadena CASE)  
**Trazabilidad:** Dossier de Arquitectura v0.1.0 (`docs/01-contexto-y-drivers.md`, `docs/03-adr/`)  

---

## 1. Matriz de Trazabilidad Requisitos - Arquitectura - Pruebas BDD

La siguiente matriz establece la alineación punto a punto entre los requerimientos del negocio, los escenarios de calidad definidos en el Dossier de Arquitectura, las decisiones de diseño (ADR), las historias de usuario (HU), los endpoints definidos en OpenAPI y las tareas del mapa de toolchain (`docs/06-mapa-toolchain.md`).

| ID HU | Historia de Usuario | Escenario Dossier | Atributo de Calidad / Regla de Negocio | Endpoint OpenAPI | ADR Vinculado | Tarea Toolchain |
| :--- | :--- | :---: | :--- | :--- | :---: | :---: |
| **HU-01** | Registro y Mantenimiento de Socios | R6, D2 | Máximo 69 socios, unicidad de cédula, baja lógica sin borrado físico. | `POST /socios`<br>`GET /socios/{socioId}` | ADR-001, ADR-002 | T1, T2, T6, T7 |
| **HU-02** | Control de Asistencia y Registro de Multas | E1, E2, D1 | Multa fija de $5.00 por inasistencia no justificada a la reunión mensual. | `POST /reuniones/{id}/asistencia` | ADR-001, ADR-002 | T1, T2, T6, T7 |
| **HU-03** | Gestión de Cobro de Servicio de Café | E1, D1, R2 | Tarifas de café: $1.50 para grupo en turno (1 de 10) y $3.00 para los demás. | `POST /reuniones/{id}/cafe` | ADR-002 | T1, T6, T7 |
| **HU-04** | Registro de Cuota Mensual y Manejo de Abonos | E1, D1, R2 | Cuota fija de $25.00/mes; cálculo exacto de saldo adeudado y abonos parciales. | `POST /reuniones/{id}/cuotas` | ADR-001, ADR-002 | T1, T6, T7 |
| **HU-05** | Apertura, Arqueo y Cierre Bloqueante de Caja Chica | E1, D1, D6 | Cierre de sesión en ≤ 2 s; congela cobros y previene modificaciones retroactivas. | `POST /reuniones/{id}/cierre`<br>`GET /reuniones/{id}/caja` | ADR-001, ADR-002, ADR-003 | T1, T4, T6, T7 |
| **HU-06** | Consulta de Estado de Cuenta e Impresión de Comprobantes | E5, D4, D6 | Búsqueda por cédula en ≤ 1 s; generación de comprobante con logo, firma y sello. | `GET /socios/{socioId}/comprobante` | ADR-002, ADR-003 | T1, T5, T6 |
| **HU-07** | Respaldo Automatizado y Verificación de Integridad | E6, D1, D5 | Copia de respaldo de `asociacion.db` a USB en ≤ 5 s; 9 chequeos de integridad SQL. | `POST /sistema/respaldo`<br>`GET /sistema/integridad` | ADR-001, ADR-003 | T1, T7, T8 |

> **Nota de minimización de datos (R1 / LOPDP):** el contrato `api/openapi.yaml` **no**
> expone la cédula. Los recursos se identifican con `socioId` (UUID interno) y la
> identificación se acepta únicamente como campo `writeOnly` en el alta de socios; por
> eso la consulta es `GET /socios/{socioId}` y no `GET /socios/{cedula}`. La relación
> entre la columna de cédula y el `socioId` ocurre solo dentro de la base local.

---

## 2. Historias de Usuario y Especificaciones Ejecutables en Gherkin

---

### **HU-01: Registro y Mantenimiento de Ficha de Socio**

* **Como** Secretaria de la Asociación "31 de Enero Narciza de Jesús",
* **Quiero** registrar y actualizar la información de los socios (cédula, nombres, grupo de rotación de café y estado),
* **Para** mantener el padrón de hasta 69 socios actualizado y garantizar la unicidad e integridad de la información personal conforme a la LOPDP.

#### **Criterios de Aceptación (Medidas Numéricas Verificables):**
1. **Límite de capacidad:** El sistema no debe permitir el registro de más de 69 socios activos (Restricción R6).
2. **Unicidad de Identificación:** No se pueden registrar dos socios con el mismo número de cédula (`UNIQUE(cedula)` en SQLite).
3. **Baja Lógica:** Ningún socio es eliminado físicamente de la base de datos; el cambio de estado asigna `activo = false` para preservar la trazabilidad del historial financiero.

```gherkin
# language: es
Característica: HU-01 - Registro y Mantenimiento de Socios
  Como Secretaria de la Asociación
  Quiero gestionar la información del padrón de socios
  Para garantizar la unicidad de identidades y cumplir la restricción de hasta 69 socios

  Antecedente:
    Dado que el sistema de gestión se encuentra operando en entorno local offline
    Y la base de datos "asociacion.db" está inicializada con las tablas correspondientes

  Escenario: Registro exitoso de un nuevo socio
    Dado que el padrón actual cuenta con 68 socios registrados
    Cuando la secretaria ingresa los datos del nuevo socio con cédula "1002345678", nombres "Juan Pérez" y grupo de café 3
    Entonces el socio debe quedar guardado exitosamente con estado "ACTIVO"
    Y el total de socios registrados en el padrón debe ser 69

  Escenario: Rechazo de registro por exceder el límite máximo de 69 socios
    Dado que el padrón actual ya cuenta con 69 socios registrados activos
    Cuando la secretaria intenta registrar a un socio adicional con cédula "1009998887" y nombres "María López"
    Entonces el sistema debe denegar el registro con el código de error 422
    Y debe mostrar el mensaje "Límite máximo alcanzado: la asociación no puede exceder los 69 socios"

  Escenario: Intento de registro con cédula duplicada
    Dado que existe un socio registrado con la cédula "0401234567" y nombres "Carlos Andrade"
    Cuando la secretaria intenta registrar un nuevo socio utilizando la misma cédula "0401234567"
    Entonces el sistema debe rechazar la transacción aplicando la restricción UNIQUE de la base de datos
    Y debe retornar un mensaje indicando "La cédula 0401234567 ya se encuentra registrada en el sistema"

  Escenario: Inactivación de socio mediante baja lógica
    Dado que el socio con cédula "1002345678" tiene estado "ACTIVO" y no registra deudas pendientes
    Cuando la secretaria procesa el retiro del socio del padrón
    Entonces el estado del socio en la base de datos debe cambiar a "INACTIVO"
    Y el registro físico del socio debe permanecer intacto en el historial de auditoría
```

---

### **HU-02: Control de Asistencia y Registro de Multas por Inasistencia**

* **Como** Secretaria de la Asociación,
* **Quiero** tomar lista a los socios durante la reunión mensual del último sábado,
* **Para** registrar automáticamente la asistencia e imponer la multa fija de $5.00 a los socios ausentes sin justificación.

#### **Criterios de Aceptación (Medidas Numéricas Verificables):**
1. **Consistencia de Multa:** Cada inasistencia no justificada genera exactamente un cargo de **$5.00** en el estado de cuenta del socio (Escenario E1).
2. **Restricción de Período:** No se permite registrar más de una asistencia o multa por socio en una misma fecha de reunión (`UNIQUE(cedula, fecha_reunion)`).
3. **Tiempo de Respuesta:** El registro individual o en lote de asistencia debe responder en un tiempo ≤ 1,0 s en la interfaz local.

```gherkin
# language: es
Característica: HU-02 - Control de Asistencia y Multas por Inasistencia
  Como Secretaria de la Asociación
  Quiero tomar asistencia en la reunión del último sábado del mes
  Para aplicar la multa fija de $5.00 a los socios ausentes

  Antecedente:
    Dado que existe una reunión mensual abierta con fecha "2026-10-31"

  Escenario: Registro de asistencia presente para un socio
    Dado que el socio con cédula "0401112223" está registrado como "ACTIVO"
    Cuando la secretaria marca la asistencia del socio "0401112223" como "PRESENTE" en la reunión "2026-10-31"
    Entonces la asistencia debe guardarse con estado "PRESENTE"
    Y el saldo por concepto de multa para este socio en la reunión debe ser $0.00

  Escenario: Generación automática de multa por inasistencia
    Dado que el socio con cédula "0404445556" está registrado como "ACTIVO"
    Cuando la secretaria marca la asistencia del socio "0404445556" como "AUSENTE" sin justificación
    Entonces el sistema debe generar automáticamente un cargo de multa por el valor exacto de $5.00
    Y el saldo adeudado del socio por la reunión "2026-10-31" debe incrementarse en $5.00

  Esquema del escenario: Validación de montos de multa según estado de asistencia
    Dado que el socio con cédula "<cedula>" asiste a la reunión mensual
    Cuando su estado de asistencia es registrado como "<estado_asistencia>"
    Entonces la multa calculada debe ser de <monto_multa> dólares
    Y la respuesta HTTP del sistema debe ser 200 OK

    Ejemplos:
      | cedula     | estado_asistencia | monto_multa |
      | 1001112223 | PRESENTE          | 0.00        |
      | 1002223334 | AUSENTE           | 5.00        |
      | 1003334445 | JUSTIFICADO       | 0.00        |

  Escenario: Prevención de doble registro de asistencia en la misma reunión
    Dado que ya se registró la asistencia del socio "0401112223" en la reunión "2026-10-31"
    Cuando la secretaria intenta registrar nuevamente la asistencia para el socio "0401112223" en la misma fecha
    Entonces el sistema debe denegar la operación devolviendo el código HTTP 409 Conflict
    Y no debe duplicarse el cargo financiero en el libro contable
```

---

### **HU-03: Gestión de Cobro de Servicio de Café y Comisiones**

* **Como** Secretaria de la Asociación,
* **Quiero** calcular y registrar el cobro del servicio de café durante el receso de la reunión,
* **Para** aplicar la tarifa preferencial de $1.50 al grupo de rotación de turno y $3.00 al resto de los socios.

#### **Criterios de Aceptación (Medidas Numéricas Verificables):**
1. **Tarifa Diferenciada:** Si el grupo del socio coincide con el grupo de turno asignado para la reunión (1 al 10), el costo del café es **$1.50**; para cualquier otro grupo, el costo es **$3.00** (Escenario E1, ADR-002).
2. **Registro Único:** Solo se permite un cobro de servicio de café por socio por período mensual.

```gherkin
# language: es
Característica: HU-03 - Cobro del Servicio de Café por Grupos de Rotación
  Como Secretaria de la Asociación
  Quiero aplicar la tarifa correspondiente por el servicio de café en la reunión
  Para cobrar $1.50 al grupo comisionado de turno y $3.00 a los demás socios

  Antecedente:
    Dado que la reunión mensual del "2026-10-31" tiene asignado el Grupo 4 como "GRUPO_TURNO"

  Escenario: Cobro de tarifa reducida a socio perteneciente al grupo de turno
    Dado que el socio con cédula "0405556667" pertenece al "Grupo 4"
    Cuando la secretaria procesa el cobro del café para el socio "0405556667"
    Entonces el sistema debe aplicar la tarifa comisionada de $1.50
    Y debe registrar la transacción en la cuenta del socio por el valor de $1.50

  Escenario: Cobro de tarifa estándar a socio fuera del grupo de turno
    Dado que el socio con cédula "0408889990" pertenece al "Grupo 1"
    Cuando la secretaria procesa el cobro del café para el socio "0408889990"
    Entonces el sistema debe aplicar la tarifa regular de $3.00
    Y debe registrar la transacción en la cuenta del socio por el valor de $3.00

  Esquema del escenario: Verificación del cálculo de tarifa de café según grupo
    Dado que la reunión actual asigna al grupo <grupo_turno> el turno de atención
    Y el socio pertenece al <grupo_socio>
    Cuando se calcula el rubro de café para el socio
    Entonces el monto cobrado debe ser exactamente <tarifa_esperada> dólares

    Ejemplos:
      | grupo_turno | grupo_socio | tarifa_esperada |
      | 4           | 4           | 1.50            |
      | 4           | 1           | 3.00            |
      | 4           | 10          | 3.00            |
      | 8           | 8           | 1.50            |
```

---

### **HU-04: Registro de Cuota Mensual y Manejo de Abonos Parciales**

* **Como** Secretaria de la Asociación,
* **Quiero** registrar el cobro de la mensualidad ordinaria y recibir abonos parciales,
* **Para** mantener actualizados los saldos individuales con cero margen de error financiero.

#### **Criterios de Aceptación (Medidas Numéricas Verificables):**
1. **Monto Fijo de Cuota:** La cuota fija mensual asignada a partir del período `2026-10` es de **$25.00** (Escenario E1, ADR-002).
2. **Abonos Parciales:** El sistema acepta abonos parciales, recalculando el saldo pendiente como `Saldo = Cuota_Total - Suma_Abonos` sin inconsistencias en centavos.
3. **No Sobrepago:** El sistema no permite recibir un abono superior al saldo adeudado del período.

```gherkin
# language: es
Característica: HU-04 - Registro de Cuotas Mensuales y Abonos Parciales
  Como Secretaria de la Asociación
  Quiero registrar la cuota fija mensual de $25.00 y procesar abonos
  Para mantener al día las cuentas individuales con cero inconsistencias de centavos

  Antecedente:
    Dado que el período fiscal activo corresponde a "2026-10" con una cuota mensual establecida de $25.00

  Escenario: Pago completo de la cuota mensual
    Dado que el socio con cédula "0403332221" tiene un saldo pendiente de $25.00 para el período "2026-10"
    Cuando la secretaria registra un pago en efectivo por el valor de $25.00
    Entonces el saldo pendiente del socio para el período "2026-10" debe quedar en $0.00
    Y el estado del rubro "CUOTA_MENSUAL" debe cambiar a "PAGADO"

  Escenario: Registro de abono parcial
    Dado que el socio con cédula "0407776665" tiene un saldo pendiente de $25.00 para el período "2026-10"
    Cuando la secretaria registra un abono parcial de $10.00
    Entonces el sistema debe actualizar el saldo pendiente del socio a exactamente $15.00
    Y el estado del rubro "CUOTA_MENSUAL" debe mantenerse en "PARCIAL"

  Escenario: Rechazo de abono que excede el saldo pendiente
    Dado que el socio con cédula "0407776665" tiene un saldo pendiente de $15.00
    Cuando la secretaria intenta ingresar un abono de $20.00 para esa misma cuota
    Entonces el sistema debe denegar la transacción devolviendo una alerta de sobrepago
    Y el saldo del socio debe permanecer en $15.00 sin modificar los registros de caja
```

---

### **HU-05: Apertura, Arqueo y Cierre Bloqueante de Caja Chica**

* **Como** Secretaria de la Asociación,
* **Quiero** realizar el cierre financiero al finalizar la reunión mensual,
* **Para** consolidar los ingresos por asistencia, café y cuotas, generar el resumen impreso y bloquear la modificación de transacciones del mes en menos de 2 segundos.

#### **Criterios de Aceptación (Medidas Numéricas Verificables):**
1. **Tiempo de Cierre:** El proceso de consolidación y cierre total de la sesión debe ejecutarse en ≤ 2,0 s (Escenario E1).
2. **Inmutabilidad y Cierre Bloqueante:** Una vez cerrada la reunión (`estado = 'CERRADA'`), el sistema rechaza cualquier intento de modificar, agregar o eliminar cobros/asistencias de dicho período (ADR-002).
3. **Consistencia Financiera:** El total consolidado en caja chica debe ser exactamente igual a la suma de `Fondo_Inicial + Cobros_Efectivo - Egresos_Caja` con 0 inconsistencias.

```gherkin
# language: es
Característica: HU-05 - Cierre Bloqueante y Arqueo de Caja Chica
  Como Secretaria de la Asociación
  Quiero ejecutar el cierre bloqueante de la reunión mensual
  Para congelar las transacciones financieras y garantizar la inmutabilidad de los saldos auditorables

  Antecedente:
    Dado que la reunión mensual del "2026-10-31" tiene registradas 69 fichas de asistencia y cobro
    Y el estado actual de la reunión es "ABIERTA"

  Escenario: Ejecución exitosa del cierre bloqueante en tiempo menor a 2 segundos
    Dado que se han cobrado $345.00 en cuotas, $180.00 en café y $25.00 en multas durante la jornada
    Cuando la secretaria presiona el botón "Cerrar Reunión Mensual"
    Entonces el sistema debe procesar el cálculo consolidado en un tiempo máximo de 2.0 segundos
    Y el estado de la reunión "2026-10-31" en la base de datos debe actualizarse a "CERRADA"
    Y el reporte del corte de caja debe reflejar exactamente $550.00 de ingresos totales

  Escenario: Intento de modificación posterior sobre una reunión cerrada
    Dado que la reunión "2026-10-31" tiene el estado "CERRADA"
    Cuando la secretaria intenta registrar un nuevo cobro de cuota para el socio "0401112223" en la reunión "2026-10-31"
    Entonces el sistema debe bloquear la transacción con el código HTTP 403 Forbidden
    Y debe mostrar el mensaje "Operación denegada: La reunión se encuentra CERRADA y congelada para auditoría"
```

---

### **HU-06: Consulta de Estado de Cuenta e Impresión de Comprobante**

* **Como** Socio o Secretaria de la Asociación,
* **Quiero** consultar la ficha de estado de cuenta e imprimir el comprobante detallado,
* **Para** verificar la transparencia de las aportaciones y contar con un respaldo físico con logo, firma y sello.

#### **Criterios de Aceptación (Medidas Numéricas Verificables):**
1. **Tiempo de Búsqueda:** La consulta por cédula entre los 69 socios responde en ≤ 1,0 s (Escenario E5).
2. **Formato de Comprobante:** El comprobante generado incluye el desglose de cuotas, café, multas, firma de la secretaria y sello de la asociación (Driver D6).
3. **Disponibilidad Offline:** La búsqueda y generación opera al 100 % sin conexión a internet (Escenario E4).

```gherkin
# language: es
Característica: HU-06 - Consulta de Ficha e Impresión de Comprobantes
  Como Socio o Secretaria
  Quiero buscar el historial financiero por número de cédula
  Para imprimir el comprobante oficial de pago durante la cola final de la reunión

  Escenario: Búsqueda rápida de estado de cuenta en menos de 1 segundo
    Dado que la base de datos contiene 69 socios registrados con sus historiales
    Cuando la secretaria ingresa la cédula "0401234567" en el módulo de consulta
    Entonces el sistema debe desplegar la ficha completa del socio en un tiempo menor o igual a 1.0 segundo
    Y debe mostrar el desglose exacto de cuotas pagadas, saldo pendiente y multas asignadas

  Escenario: Generación e impresión de comprobante oficial
    Dado que se ha desplegado la ficha de pago del socio "0401234567" para la reunión "2026-10-31"
    Cuando la secretaria hace clic en "Imprimir Comprobante"
    Entonces el sistema debe enviar a la impresora el documento estructurado conteniendo logo, encabezado, tabla de rubros pagados y líneas para firma y sello
    Y debe registrar la emisión del comprobante en la bitácora de auditoría
```

---

### **HU-07: Respaldo Automatizado y Verificación de Integridad de Datos**

* **Como** Responsable de Vigilancia o Equipo Técnico,
* **Quiero** ejecutar la exportación de respaldo del archivo de datos `asociacion.db` hacia una unidad USB y validar los chequeos de integridad,
* **Para** prevenir la pérdida de información ante fallos eléctricos o de disco y garantizar un sistema auditable.

#### **Criterios de Aceptación (Medidas Numéricas Verificables):**
1. **Velocidad de Respaldo:** La copia del archivo `.db` a la unidad USB se completa en un tiempo ≤ 5,0 s (Escenario E6).
2. **Verificación de Integridad:** La rutina de diagnóstico ejecuta 9 chequeos de integridad en SQLite (`PRAGMA integrity_check`) devolviendo 0 errores o corrupción.

```gherkin
# language: es
Característica: HU-07 - Respaldo a USB y Diagnóstico de Integridad
  Como Comisión de Vigilancia
  Quiero respaldar el archivo de datos al finalizar la reunión y comprobar la integridad SQLite
  Para mitigar riesgos de fallo de hardware y garantizar cero pérdidas de datos

  Escenario: Exportación exitosa de respaldo a unidad USB
    Dado que existe una unidad USB conectada en la PC local
    Cuando la secretaria ejecuta la opción "Exportar Respaldo a USB" tras el cierre de caja
    Entonces el archivo "asociacion.db" debe copiarse hacia la unidad externa agregando la marca de tiempo "asociacion_20261031.db"
    Y el proceso completo debe finalizar en un tiempo menor a 5.0 segundos

  Escenario: Ejecución de verificación de integridad de base de datos
    Dado que la aplicación inicia su secuencia de autodiagnóstico
    Cuando el sistema ejecuta los 9 chequeos de integridad de SQLite sobre "asociacion.db"
    Entonces el resultado del diagnóstico debe retornar "ok" sin detectar registros huérfanos ni inconsistencias físicas
```

---

## 3. Instrucciones para la Ejecución Automática con Cucumber.js / Pytest-BDD

Para la ejecución y verificación de estas especificaciones ejecutables en la cadena CASE (Sesión 6):

1. **Directorio del Proyecto:** Guardar los archivos `.feature` dentro de la carpeta `features/` o `tests/features/`.
2. **Ejecución con Node.js / Cucumber.js:**
   ```bash
   npm test
   ```
3. **Ejecución con Python / Pytest-BDD:**
   ```bash
   pytest tests/test_bdd.py -v
   ```
4. **Criterio de Éxito para Integración Continua:**
   * **100 % de escenarios aprobados** (`passed`).
   * **0 inconsistencias** en la ejecución de la lógica financiera local.
