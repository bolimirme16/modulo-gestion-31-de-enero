# 09 · Informe final: arquitectura, cadena CASE, versionamiento y automatización

**Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
**Módulo 8 · Automatización de proceso de software · Actividad autónoma Semana 4 — Informe, repositorio y pipeline**
**Versión:** v0.4.0 (hito H4) · **Fecha:** 06/11/2026
**Equipo:** Bolívar Alexander Valenzuela Mejía · José Miguel Guerrero Tapia · Alejandra Valeria Lucero Burbano
**Normas de referencia:** ISO/IEC/IEEE 42010:2022, ISO/IEC 25010:2023, ISO/IEC/IEEE 12207:2017, ISO/IEC 14102:2008 y NIST SP 800-218 (SSDF).

> Este informe **enlaza** los artefactos del repositorio en lugar de copiarlos. Cada afirmación verificable remite al archivo, al *commit* o al *run* que la respalda.

---

## (a) Resumen del caso y alcance

La Asociación “31 de Enero Narciza de Jesús” administra 69 socios con registros en papel: lista de asistencia, café por comisiones, mensualidades y caja chica. El sistema digitaliza ese flujo en una aplicación **100 % local y offline**, para una sola operadora (la secretaria), con presupuesto cero y sin instalación de dependencias en la PC de la asociación.

El alcance de esta entrega no es añadir funcionalidad de negocio, sino **cerrar el proyecto de punta a punta**: dejar el repositorio gobernado, el pipeline de integración continua con puertas de calidad, el informe integrador y la matriz de trazabilidad que permite defender cada decisión con evidencia. El resultado es el hito **v0.4.0**, etiquetado sobre el extremo de `main`, con cinco versiones SemVer (`v0.1.0` a `v0.4.0`) y un historial donde cada cambio entró por *pull request*.

**Resultado verificable:** 36 pruebas en verde, lint limpio, análisis estático sin hallazgos medios o altos, contrato OpenAPI sin errores ni advertencias, documentación construida con enlaces internos válidos y una falla de pipeline provocada y corregida en 59 segundos.

| Dato del cierre | Valor | Fuente |
| :--- | :--- | :--- |
| Versión entregada | `v0.4.0` | *Release* del repositorio |
| Pruebas automatizadas | 36 en verde | [`docs/evidencias/11-falla-provocada.txt`](evidencias/11-falla-provocada.txt) |
| Puertas de calidad | 5 (lint, SAST, OpenAPI, pruebas, docs) | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| Duración del pipeline | ≈ 30 s | Run `42045483208` |
| Cobertura de trazabilidad | 7 HU y 6 escenarios sin eslabones rotos | [`docs/05-trazabilidad.md`](05-trazabilidad.md) |

---

## (b) Arquitectura: drivers, escenarios y decisiones

El dossier de arquitectura ([`docs/00-Dossier-de-arquitectura.md`](00-Dossier-de-arquitectura.md)) y el contexto ([`docs/01-contexto-y-drivers.md`](01-contexto-y-drivers.md)) definen seis *drivers* y seis escenarios de calidad con una medida numérica cada uno. La arquitectura es un **monolito Flask montado sobre SQLite**, ejecutado en una ventana de escritorio con `pywebview` y servido por `waitress`.

### Drivers y su prioridad

| Driver | Atributo (ISO/IEC 25010) | Importancia | Decisión que lo atiende |
| :--- | :--- | :---: | :--- |
| **D1** Consistencia financiera | Fiabilidad | Alta | Reglas centralizadas + cierre bloqueante (ADR-002) |
| **D2** Protección de datos y trazabilidad | Seguridad | Alta | Minimización de cédula en la API + auditoría (ADR-002) |
| **D3** Facilidad de cambio | Mantenibilidad | Media | Tarifas en un único módulo (ADR-002) |
| **D4** Operación local offline | Portabilidad / usabilidad | Alta | Monolito local monousuario (ADR-003) |
| **D5** Desempeño durante la reunión | Eficiencia | Media | SQLite con índices y consultas acotadas (ADR-001) |
| **D6** Corte y comprobante | Adecuación funcional | Alta | Cierre transaccional y plantilla imprimible (ADR-002) |

### Escenarios de calidad

| Escenario | Medida | Dónde se verifica |
| :--- | :--- | :--- |
| **E1** Consistencia financiera | 0 inconsistencias; saldos exactos; cierre ≤ 2 s | [`tests/test_e1_multa.py`](../tests/test_e1_multa.py), [`tests/test_cierre.py`](../tests/test_cierre.py) |
| **E2** Seguridad y datos | 100 % de accesos no autenticados denegados | [`docs/10-gobierno-del-repositorio.md`](10-gobierno-del-repositorio.md) |
| **E3** Facilidad de cambio | ≤ 1 día-persona; 0 cambios en otros módulos | [`src/reglas.py`](../src/reglas.py) |
| **E4** Operación offline | Arranque ≤ 6 s; `/login` 200 sin internet | [`docs/proyecto/05-manual-de-uso-rapido.md`](proyecto/05-manual-de-uso-rapido.md) |
| **E5** Desempeño de consulta | 95 % de consultas ≤ 1 s con 69 socios | [`tests/test_api.py`](../tests/test_api.py) |
| **E6** Tolerancia a fallos | 0 registros perdidos; 9 de 9 chequeos | [`tests/test_sistema.py`](../tests/test_sistema.py) |

### Decisiones principales

| ADR | Decisión | Alternativa descartada | Consecuencia dominante |
| :--- | :--- | :--- | :--- |
| [ADR-001](03-adr/ADR-001-persistencia-sqlite-un-archivo.md) | SQLite en un solo archivo | Servidor de base de datos | Copia de respaldo trivial; escritura serializada |
| [ADR-002](03-adr/ADR-002-reglas-financieras-cierre-auditoria.md) | Reglas financieras y cierre en una capa única | Cálculos dispersos en las vistas | Un solo punto de cambio y pruebas deterministas |
| [ADR-003](03-adr/ADR-003-monolito-local-monousuario.md) | Monolito local monousuario | Microservicios o nube | Cero infraestructura; sin escalabilidad horizontal |
| [ADR-004](03-adr/ADR-004-seleccion-git-como-scm.md) | Git + GitHub como SCM | Subversion | Ramas baratas y CI gratuito; sin permisos por ruta |

La consecuencia crítica de ADR-003 es que **no hay despliegue continuo clásico**: la “entrega” es una etiqueta sobre `main` y el binario se genera con PyInstaller. Esa restricción condiciona las métricas DORA de la sección (f) y se declara explícitamente para no presentar cifras engañosas.

---

## (c) Cadena CASE: del requisito al artefacto

El mapa de toolchain ([`docs/06-mapa-toolchain.md`](06-mapa-toolchain.md)) prioriza diez tareas con el producto frecuencia × esfuerzo × riesgo. Las tres de mayor puntaje concentran la automatización:

| Tarea | Puntaje | Herramienta | Categoría | Verificación |
| :--- | :---: | :--- | :--- | :--- |
| **T7** Pruebas de consistencia financiera | 100 | pytest + pytest-bdd | Lower CASE | 36 pruebas en el pipeline |
| **T4** Validación del contrato OpenAPI | 64 | Spectral 6.17.0 | Upper CASE | `--fail-severity=warn` |
| **T6** Generación de *stubs* y documentación | 48 | OpenAPI Generator 7.26.0 | Lower CASE | [`src/generated/`](../src/generated/) |

La selección no se hizo por popularidad: la matriz de evaluación ([`docs/08-matriz-evaluacion-seleccion.md`](08-matriz-evaluacion-seleccion.md)) puntúa cada alternativa con seis criterios ponderados (fidelidad al contrato, esfuerzo, calidad, integración, costo y riesgo). OpenAPI Generator obtuvo 90/100 frente a 70/100 del asistente de IA, y pytest-bdd 90/100 frente a 68/100 de Cucumber.js. La razón decisiva en ambos casos fue la **integración con el resto de la cadena**, no la funcionalidad aislada.

El flujo completo queda así: HU y Gherkin → contrato OpenAPI → *stubs* y documentación → implementación en `src/reglas.py` y `src/app.py` → pruebas unitarias, de integración y BDD → pipeline → etiqueta SemVer. Cada eslabón tiene un archivo y un comando reproducible; el detalle está en [`docs/09-informe-cadena-case.md`](09-informe-cadena-case.md) y en [`docs/05-trazabilidad.md`](05-trazabilidad.md).

---

## (d) Versionamiento: flujo, conflicto y decisión Git vs SVN

### Flujo de ramas

El flujo está en [`CONTRIBUTING.md`](../CONTRIBUTING.md): `issue → rama corta → commits convencionales → PR → revisión → CI en verde → squash a main → etiqueta`. Las ramas viven horas o días, nunca semanas; el *merge* es por *squash* para conservar un historial lineal y legible.

La protección de `main` se verificó por API y exige: **una aprobación**, `dismiss_stale_reviews`, `enforce_admins`, conversaciones resueltas, *check* `Spectral + Ruff + pytest` en verde, sin *force push* y sin borrado. La evidencia está en [`docs/evidencias/09-proteccion-de-main.txt`](evidencias/09-proteccion-de-main.txt) y [`docs/evidencias/13-proteccion-y-checks.txt`](evidencias/13-proteccion-y-checks.txt).

### Conflicto deliberado

En el PR #7 se provocó un conflicto real entre dos ramas que editaban la misma regla de integración. El reporte [`docs/11-practica-de-conflicto.md`](11-practica-de-conflicto.md) documenta causa, marcadores, resolución y prevención; la resolución quedó en el *commit* `e64fc60`. La lección no fue “resolver el conflicto”, sino **reducir su probabilidad**: ramas cortas, dueños por área en [`.github/CODEOWNERS`](../.github/CODEOWNERS) y cambios pequeños.

### Git vs SVN

La matriz de siete dimensiones ([`docs/08-matriz-git-vs-svn.md`](08-matriz-git-vs-svn.md)) y el [ADR-004](03-adr/ADR-004-seleccion-git-como-scm.md) sostienen la elección de Git. El argumento decisivo no es la popularidad: es que **el historial y las ramas son locales**, lo que permite trabajar sin conectividad garantizada, y que GitHub ofrece revisión y CI sin costo. SVN aplicaría si la asociación exigiera un servidor propio con permisos por ruta, si el repositorio concentrara binarios grandes con necesidad de bloqueo, o si el equipo se integrara a una organización que ya opera SVN.

### Versiones

| Etiqueta | Hito | Contenido | Fecha |
| :--- | :--- | :--- | :--- |
| `v0.1.0` | H1 | Dossier de arquitectura | 18/10/2026 |
| `v0.2.0` | H2 | Cadena CASE y especificación | 23/10/2026 |
| `v0.3.0` | H3 | Repositorio gobernado | 01/11/2026 |
| `v0.3.1` | H3 | Parche de seguridad (credenciales fuera del código) | 01/11/2026 |
| `v0.4.0` | H4 | Pipeline CI, informe final y trazabilidad | 06/11/2026 |

---

## (e) Automatización: pipeline y *quality gates*

El pipeline ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)) se ejecuta en cada *push* a `main` y en cada *pull request*. Tiene **permisos mínimos** (`contents: read`), `persist-credentials: false`, *timeout* de 15 minutos, concurrencia que cancela ejecuciones obsoletas y acciones fijadas por versión (`checkout@v4`, `setup-python@v5`, `setup-node@v4`, `upload-artifact@v4`). No usa secretos.

### Puertas de calidad

| # | Puerta | Comando | Criterio de fallo |
| :---: | :--- | :--- | :--- |
| 1 | Lint | `ruff check src tests scripts` | Cualquier hallazgo |
| 2 | Análisis estático de seguridad | `bandit -q -r src -x src/generated -ll` | Hallazgo medio o alto |
| 3 | Contrato OpenAPI | `spectral lint api/openapi.yaml --fail-severity=warn` | Error o advertencia |
| 4 | Pruebas | `pytest -q` | Cualquier prueba roja |
| 5 | Build de documentación | `python scripts/build_docs.py --out site` | Enlace interno roto |
| 6 | Artefacto | `actions/upload-artifact@v4` | Documentación no generada |

El *check* obligatorio conserva el nombre **`Spectral + Ruff + pytest`** por continuidad con la protección de `main`; dentro del mismo trabajo se ejecutan las seis puertas. La documentación construida se publica como artefacto `documentacion-html` durante siete días.

### Falla provocada y corregida

La evidencia completa está en [`docs/evidencias/11-falla-provocada.txt`](evidencias/11-falla-provocada.txt).

1. El *commit* `74cf8d2` agregó [`tests/test_e1_multa.py`](../tests/test_e1_multa.py) con un valor esperado incorrecto ($4,00 en lugar de $5,00).
2. El run [`42045339641`](https://github.com/bolimirme16/modulo-gestion-31-de-enero/actions/runs/42045339641) falló en el paso de pruebas: la puerta **detuvo el cambio**, como debía.
3. El *commit* `e949bc0` corrigió el valor y añadió la verificación del corte de caja.
4. El run [`42045483208`](https://github.com/bolimirme16/modulo-gestion-31-de-enero/actions/runs/42045483208) quedó en verde en **59 segundos** desde el cierre del run rojo (85 segundos desde su inicio).

Ese ciclo rojo → verde es la demostración de que el pipeline no es decorativo: **bloquea de verdad**.

---

## (f) Métricas aproximadas tipo DORA

Las métricas se calcularon con la API de GitHub (repositorio público) y el historial de Git. No hay servidor de producción: se declara que “despliegue” significa **publicación de una etiqueta anotada sobre `main`**, no un despliegue a usuarios finales. Los datos y el procedimiento completo están en [`docs/evidencias/12-metricas-dora.txt`](evidencias/12-metricas-dora.txt).

| Métrica | Definición aplicada | Fórmula | Resultado |
| :--- | :--- | :--- | :--- |
| **Frecuencia de despliegue** | Etiquetas publicadas por semana | `n.º de tags / semanas del periodo` | **5 tags en 19 días ≈ 1,8 por semana** |
| **Lead time for changes** | Tiempo entre apertura y fusión del PR | `mediana(merged_at − created_at)` | **6,7 h** (11 PR fusionados antes del cierre) |
| **Change failure rate (CI)** | Runs fallidos sobre runs totales | `runs con conclusion=failure / runs` | **1 de 41 ≈ 2,4 %** |
| **Change failure rate (releases)** | Versiones que requirieron corrección | `versiones con parche / versiones` | **1 de 5 = 20 %** (`v0.3.1`) |
| **MTTR (pipeline)** | Del run rojo al run verde | `fin del verde − fin del rojo` | **59 s** |
| **MTTR (incidente)** | De la versión afectada al parche | `v0.3.1 − v0.3.0` | **26 min** |

### Cómo se obtuvieron

```bash
# PR fusionados: número, apertura y fusión
GET /repos/bolimirme16/modulo-gestion-31-de-enero/pulls?state=all&per_page=100

# Ejecuciones del workflow
GET /repos/bolimirme16/modulo-gestion-31-de-enero/actions/workflows/ci.yml/runs?per_page=100

# Fechas de las etiquetas
git log -1 --format='%h %cI' v0.1.0 v0.2.0 v0.3.0 v0.3.1 v0.4.0
```

El *lead time* se calculó con la mediana y no con la media porque un PR de 21,7 h (el primero del hito H3, abierto antes de tener revisores disponibles) distorsiona el promedio. La mediana describe mejor el comportamiento típico. La tasa de fallo se informa de dos maneras porque un fallo de pipeline no equivale a un fallo de producto: el 2,4 % mide la salud del CI y el 20 % mide la calidad de las versiones publicadas.

**Lectura crítica de las cifras.** Con 5 versiones y 12 PR, la muestra es demasiado pequeña para inferencia estadística; las métricas son **indicativas**, no concluyentes. Además, el proyecto no tiene usuarios concurrentes ni despliegue continuo, por lo que la frecuencia de despliegue mide el ritmo de hitos académicos, no la capacidad de entregar valor a producción. Se presentan porque la rúbrica las exige y porque obligan a mirar el proceso con datos, pero **no se usan para afirmar un nivel de madurez DevOps que el contexto no permite**.

---

## (g) Uso responsable de inteligencia artificial

El registro completo está en [`docs/04-registro-ia.md`](04-registro-ia.md). Para esta semana se añadió la revisión del workflow generado con una lista de verificación explícita:

| Verificación | Resultado | Evidencia |
| :--- | :--- | :--- |
| ¿Permisos mínimos? | Sí: `contents: read` | `ci.yml`, líneas 10–11 |
| ¿Acciones fijadas por versión? | Sí: `@v4`, `@v5`; Spectral `@6.17.0` | `ci.yml` |
| ¿Sin secretos? | Sí: no usa `secrets.*`; auditoría limpia | [`evidencias/10-auditoria-de-secretos.txt`](evidencias/10-auditoria-de-secretos.txt) |
| ¿Se ejecutó de verdad? | Sí: runs `42045339641` y `42045483208` | [`evidencias/11-falla-provocada.txt`](evidencias/11-falla-provocada.txt) |
| ¿Sin datos personales? | Sí: solo cédulas ficticias en pruebas | `tests/` |

La IA se usó como **borrador y revisor**, nunca como autoridad. Se aceptó su propuesta de estructura del pipeline y del script de build; se modificó el orden de las puertas para que el lint falle antes que las pruebas (feedback más rápido); se rechazó una propuesta de usar `pull_request_target`, porque ejecuta código del PR con permisos del repositorio base y amplía la superficie de ataque. También se rechazó fijar acciones por rama (`@main`), práctica que la rúbrica penaliza.

El criterio de verificación no fue “parece correcto”, sino **ejecutar**: pytest, Ruff, Bandit, Spectral y el build de documentación. Un workflow que no se ejecuta no está verificado.

---

## (h) Análisis crítico y lecciones aprendidas

### Qué funcionó

1. **Un solo contrato como fuente de verdad.** `api/openapi.yaml` alimenta documentación, *stubs*, *mock* y pruebas. Cambiar el contrato y olvidar el código se detecta en el pipeline.
2. **El pipeline como conversación, no como trámite.** La falla provocada demostró que el *check* bloquea el *merge*; sin esa prueba, la protección de `main` sería una captura de pantalla.
3. **Trazabilidad explícita.** La matriz [`docs/05-trazabilidad.md`](05-trazabilidad.md) obliga a que cada HU tenga escenario, ADR, artefacto, commit y paso de pipeline. Los identificadores coinciden entre documentos y código.
4. **Build de documentación con enlaces validados.** El script [`scripts/build_docs.py`](../scripts/build_docs.py) convierte 25 documentos y falla si un enlace interno se rompe; la documentación dejó de ser un subproducto que se degrada sola.

### Qué no funcionó o quedó débil

1. **La revisión cruzada depende de la disponibilidad de las personas.** Con tres integrantes en horarios distintos, la aprobación se convirtió en el cuello de botella del *lead time*. El pipeline tarda 30 segundos; conseguir una revisión puede tardar horas.
2. **La cobertura no es una puerta todavía.** Se ejecutan 36 pruebas, pero no se mide el porcentaje de cobertura ni se exige un umbral. Un pipeline verde no garantiza que las ramas de error estén probadas.
3. **Bandit excluye el código generado.** `src/generated/` no se analiza porque es salida de OpenAPI Generator; se acepta el riesgo, pero se documenta.
4. **Las métricas DORA son proxies.** Sin despliegue real, la frecuencia de despliegue mide hitos, no valor entregado. El *change failure rate* por *runs* mezcla fallos de infraestructura con fallos de código.
5. **El pipeline no prueba concurrencia ni rendimiento.** Las medidas de E5 y E6 se verifican con pruebas funcionales, no con pruebas de carga; el contexto monousuario lo justifica, pero el límite debe decirse.

### Qué cambiaríamos

| Mejora | Por qué | Cómo se verificaría |
| :--- | :--- | :--- |
| Umbral de cobertura (`pytest-cov ≥ 80 %`) | Convertir la cobertura en puerta, no en dato | Paso nuevo en `ci.yml` |
| Caché de Spectral | Evitar `npm install -g` en cada ejecución | `actions/cache` con clave por versión |
| Pruebas de rendimiento con 69 socios | Respaldar E5 con una medida real | `pytest-benchmark` con umbral ≤ 1 s |
| Revisión con *code owners* obligatorios | Reducir el tiempo de espera y la subjetividad | `require_code_owner_reviews: true` |
| Firma de *commits* o *tags* | Elevar la integridad del historial | `git tag -s` y verificación en CI |

### Límites del proceso

El sistema es **monousuario, offline y de escritorio**: no hay alta disponibilidad, ni escalado, ni observabilidad en producción. El pipeline verifica el código, no el comportamiento en la PC de la secretaria. La protección de `main` y las etiquetas SemVer aportan gobernanza, pero no sustituyen una revisión humana profunda. Y la calidad del informe depende de que los artefactos enlazados sigan existiendo: por eso el build de documentación es también una prueba de integridad documental.

---

## Reproducción

```bash
git clone https://github.com/bolimirme16/modulo-gestion-31-de-enero
cd modulo-gestion-31-de-enero

pip install -r requirements-dev.txt

ruff check src tests scripts
bandit -q -r src -x src/generated -ll
npx --yes @stoplight/spectral-cli@6.17.0 lint api/openapi.yaml --fail-severity=warn
pytest -q
python scripts/build_docs.py --out site
```

El resultado esperado es: lint limpio, Bandit sin hallazgos medios o altos, Spectral con 0 errores y 0 advertencias, 36 pruebas en verde y 25 documentos construidos sin enlaces rotos.

---

## Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Collins-Sussman, B., Fitzpatrick, B. W., & Pilato, C. M. (2011). *Version control with Subversion: For Subversion 1.7*. O’Reilly Media. https://svnbook.red-bean.com

Conventional Commits. (s. f.). *Conventional Commits 1.0.0*. https://www.conventionalcommits.org/es/v1.0.0/

Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The science of lean and DevOps*. IT Revolution Press.

Fowler, M. (2024). *Continuous integration*. martinfowler.com. https://martinfowler.com/articles/continuousIntegration.html

GitHub. (s. f.). *GitHub Actions documentation*. https://docs.github.com/actions

Humble, J., & Farley, D. (2010). *Continuous delivery: Reliable software releases through build, test, and deployment automation*. Addison-Wesley.

Nygard, M. (2011, 15 de noviembre). *Documenting architecture decisions*. Cognitect Blog. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions

Preston-Werner, T. (s. f.). *Semantic Versioning 2.0.0*. https://semver.org/lang/es/

Souppaya, M., Scarfone, K., & Dodson, D. (2022). *Secure software development framework (SSDF) version 1.1* (NIST Special Publication 800-218). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-218
