# 03 · Priorización de escenarios y matriz de decisión ponderada

**Actividad:** comparar al menos **dos alternativas** de estilo arquitectónico frente a los escenarios de calidad y explicitar el trade-off (Práctica 03, pasos 1–5).
**Base de cálculo:** cada calificación va de **1 (peor) a 5 (mejor)** y se ubica en la rúbrica del final; el total ponderado = Σ (peso × calificación) / 100.

---

## Paso 1 · Priorizar los escenarios

| Escenario | Driver | Impacto en el negocio | Costo de cambiarlo después | Prioridad |
|-----------|--------|-----------------------|----------------------------|-----------|
| E1 Consistencia financiera | D1 | Alto: un saldo mal calculado rompe la confianza y el corte | Alto: atraviesa datos, reglas y comprobantes | 1 |
| E2 Seguridad y datos personales | D2 | Alto: cédulas y datos personales; riesgo legal (LOPDP) | Alto: afecta todos los puntos de entrada | 2 |
| E4 Operabilidad offline | D4 | Alto: si no abre sin internet, no hay reunión | Medio: depende del empaquetado y la ventana | 3 |
| E6 Tolerancia a fallos y respaldo | D1, D5 | Alto: perder la caja del mes es inaceptable | Medio: depende de dónde y cómo se persista | 4 |
| E3 Facilidad de cambio | D3 | Medio: cambian tarifas de vez en cuando | Bajo: se puede preparar después | 5 |
| E5 Desempeño de consulta | D5 | Medio: molesta en la cola, pero no bloquea | Bajo: se corrige con índices | 6 |

---

## Paso 2 · Alternativas de estilo

| ID | Alternativa | Descripción | Costo operativo |
|----|-------------|-------------|-----------------|
| A1 | **Monolito web local monousuario** | Una sola aplicación (Flask) con una sola base de datos (SQLite) y ventana interna (pywebview); 100 % offline, empaquetada como ejecutable | Bajo: un despliegue y un proceso; $0 licencias |
| A2 | **Cliente-servidor con base de datos en red** | Cliente de escritorio/navegador que llama a un servidor con MySQL/PostgreSQL en la red de la asociación | Medio: requiere un servidor de base de datos y red de la PC |
| A3 | **Microservicios en la nube** | Servicios pequeños independientes (socios, reunión, caja, auditoría), cada uno con su base de datos, desplegados en internet | Alto: varios despliegues, red entre servicios y dependencia de internet |

---

## Paso 3 · Criterios y pesos (derivados de los escenarios y restricciones)

| N.º | Criterio | Origen | Peso | Cómo se evalúa |
|-----|----------|--------|------|----------------|
| 1 | Consistencia financiera | E1 · D1 | **25 %** | Capacidad de garantizar 0 inconsistencias en el corte con poca complejidad |
| 2 | Seguridad y datos personales | E2 · D2 · R1 | **15 %** | Puntos de control de acceso, auditoría y superficie expuesta |
| 3 | Operabilidad offline en PC única | E4 · D4 · R4 | **20 %** | Funcionar sin internet ni instalación de dependencias |
| 4 | Tolerancia a fallos y respaldo | E6 · D1/D5 | **15 %** | Aislamiento del fallo y facilidad de respaldo/restauración |
| 5 | Facilidad de cambio | E3 · D3 | **10 %** | Cambios necesarios para modificar una tarifa o una regla |
| 6 | Desempeño y costo operativo | E5 · D5 · R3/R5 | **15 %** | Latencia en la consulta y carga de operación para un equipo pequeño |
| | **Total** | | **100 %** | |

---

## Paso 4 · Matriz ponderada

| Criterio | Peso | A1 | A2 | A3 |
|----------|------|----|----|----|
| 1. Consistencia financiera (E1) | 25 % | 5 | 4 | 2 |
| 2. Seguridad y datos personales (E2) | 15 % | 4 | 5 | 3 |
| 3. Operabilidad offline en PC única (E4) | 20 % | 5 | 1 | 1 |
| 4. Tolerancia a fallos y respaldo (E6) | 15 % | 4 | 3 | 4 |
| 5. Facilidad de cambio (E3) | 10 % | 4 | 3 | 5 |
| 6. Desempeño y costo operativo (E5) | 15 % | 5 | 2 | 1 |
| **Total ponderado (de 5)** | **100 %** | **4,60** | **3,00** | **2,40** |

### Justificación de cada calificación (observable)

| Criterio | Justificación |
|----------|---------------|
| 1. Consistencia (E1) | **A1 (5):** una transacción local en SQLite aplica las restricciones `UNIQUE` y calcula saldos sin coordinar componentes. **A2 (4):** la base central permite transacción, pero exige operar el servidor. **A3 (2):** exige coordinar servicios (transacción distribuida/saga) para cuadrar la caja. |
| 2. Seguridad (E2) | **A1 (4):** un solo punto de login y auditoría; superficie pequeña. **A2 (5):** control central de acceso y roles. **A3 (3):** más servicios expuestos y más credenciales entre ellos. |
| 3. Operabilidad offline (E4) | **A1 (5):** abre y opera **sin internet** con doble clic. **A2 (1):** depende de la red y de un servidor de base de datos. **A3 (1):** depende de internet. |
| 4. Fallos y respaldo (E6) | **A1 (4):** respaldo = copiar 1 archivo; el fallo afecta a la PC local. **A2 (3):** respaldo del servidor central, pero un fallo del servidor detiene la operación. **A3 (4):** aísla fallos por servicio, pero el respaldo se reparte entre varias bases. |
| 5. Facilidad de cambio (E3) | **A1 (4):** reglas en un único `app.py`; un solo despliegue. **A2 (3):** cambio acotado pero con redespliegue del servidor. **A3 (5):** servicio independiente por dominio. |
| 6. Desempeño y costo (E5) | **A1 (5):** consulta local indexada y $0 licencias; la opera una persona. **A2 (2):** requiere servidor y su administración. **A3 (1):** varios servicios y habilidades que exceden al equipo (R5). |

---

## Paso 5 · Trade-offs y análisis de sensibilidad (ATAM simplificado)

### Riesgos de la alternativa ganadora (A1)

| Riesgo | Escenario | Mitigación |
|--------|-----------|------------|
| Pérdida de datos si falla el disco local | E6 | Respaldo `.db` al USB al cerrar + verificación de integridad (9 chequeos) |
| Un saldo mal cargado contamina el historial | E1 | Cierre bloqueante con reapertura controlada + auditoría |
| Crecimiento a multiusuario o multi-oficina | E4 | Se revisa la decisión si cambia el contexto (ver sensibilidad) |

### Análisis de sensibilidad

Se mueven los dos pesos más discutibles: **operabilidad offline (criterio 3)** y **facilidad de cambio (criterio 5)**.

| Alternativa | Pesos base (offline 20 %, cambio 10 %) | Pesos alternos (offline 5 %, cambio 25 %) |
|-------------|----------------------------------------|-------------------------------------------|
| A1 Monolito local | **4,60** | **4,45** |
| A2 Cliente-servidor en red | 3,00 | 3,30 |
| A3 Microservicios en la nube | 2,40 | 3,00 |

**Lectura:** con los pesos base gana **A1 (4,60)** por amplio margen. Si la asociación adoptara internet y varios dispositivos (bajando el peso de “offline” y subiendo el de “facilidad de cambio”), A1 **sigue ganando (4,45)**, pero la ventaja se reduce de 1,60 a 1,15 puntos sobre A2. **Punto de sensibilidad:** la decisión depende de que la operación siga siendo **local y monousuario**; si ese supuesto cambia, A2 se vuelve competitivo y la decisión debe revisarse.

**Trade-off explícito:** A1 **sacrifica escalabilidad y cambio por dominio** (que ofrecería A3) y **la centralización del acceso en red** (que ofrecería A2) a cambio de consistencia, operación offline y costo/operación mínimos —lo correcto para 69 socios con una sola operadora y presupuesto $0 (R3, R4, R5).

---

## Rúbrica de calificación (1 a 5)

| Criterio | 5 (mejor) | 3 (intermedio) | 1 (peor) |
|----------|-----------|----------------|----------|
| 1. Consistencia (E1) | Una transacción local garantiza 0 inconsistencias sin coordinar componentes | Requiere coordinar componentes (sagas/compensaciones) | No se puede garantizar la medida |
| 2. Seguridad (E2) | Un solo punto de control y auditoría; poca superficie | Control en varios puntos; auditoría a consolidar | Control disperso, sin registro central |
| 3. Offline (E4) | Abre y opera sin internet, sin instalar dependencias | Requiere red local o algún componente externo | No funciona sin internet/servidor |
| 4. Fallos y respaldo (E6) | Respaldo de 1 artefacto y fallo aislado | Respaldo posible pero con componente extra que operar | El fallo detiene la operación o se pierden avisos/datos |
| 5. Facilidad de cambio (E3) | Cambio en un componente que se despliega solo | Cambio acotado, con redespliegue completo | Cambio disperso |
| 6. Desempeño y costo (E5) | Consulta local ágil; lo opera una persona con $0 | Un componente adicional operable | Varios servicios y habilidades que exceden al equipo |

> En el criterio 6, un **5** significa **el menor costo y la menor carga**, no el mayor.
