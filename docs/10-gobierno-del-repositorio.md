# 10 · Gobierno del repositorio

**Proyecto:** Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”
**Módulo 8 · Automatización de proceso de software · UPEC**
**Hito H3 · v0.3.0 · 01/11/2026** — Repositorio gobernado (SEM03)

---

## 1. Propósito

Este documento describe **cómo se gobierna el repositorio** del proyecto: quién puede cambiar
qué, con qué procedimiento, con qué verificación y con qué evidencia. El objetivo no es
decorativo: es que cualquier persona pueda reconstruir la historia de una decisión sin
preguntar a sus autores.

El gobierno se apoya en el proceso de **gestión de la configuración** de ISO/IEC/IEEE 12207:2017
y en las directrices de ISO 10007:2017. Ambos exigen cuatro cosas que aquí se implementan de forma
verificable: identificar los elementos de configuración, controlar los cambios, registrar el
estado y auditar la conformidad.

---

## 2. Situación inicial (diagnóstico)

Antes de esta semana el repositorio ya contenía el producto y la documentación de los hitos H1 y
H2, pero **no tenía reglas escritas**. La auditoría encontró:

| Hallazgo | Consecuencia |
|----------|--------------|
| Sin `CONTRIBUTING.md` | El flujo de trabajo existía en la práctica, no como norma |
| Sin `CODEOWNERS` ni revisión obligatoria | Cualquier integrante podía fusionar sin revisión |
| Sin `LICENSE`, `CHANGELOG.md`, `SECURITY.md` | Sin marco de uso, historial de versiones ni canal de reporte |
| Sin `.gitattributes` ni `.editorconfig` | Riesgo de diffs por finales de línea en Windows |
| Rama `valery/toolchain` ya fusionada y sin borrar | Desorden visible en el remoto |
| Commits iniciales sin convención | Historias heterogéneas (`Sistema gestion socios v1.2.0`) |

Estos hallazgos se corrigieron en el hito H3 mediante siete ramas temáticas, cada una con su
propio *pull request* y revisión cruzada. La rama `valery/toolchain` se conserva sin borrar por
decisión del equipo: documenta la entrega de H2 y su borrado no aporta evidencia adicional.

---

## 3. ¿Por qué se gobernó el repositorio existente y no se creó uno nuevo?

La consigna de la actividad indica que **se puede ordenar el repositorio usando las convenciones
de Git**. No pide un repositorio distinto.

Crear uno nuevo habría tenido tres costos:

1. **Pérdida de trazabilidad.** Las etiquetas `v0.1.0` (dossier de arquitectura) y `v0.2.0`
   (cadena CASE) viven en este repositorio. Un repositorio nuevo empezaría sin ellas y la cadena
   de evidencia S → D → E → ADR → vista quedaría partida en dos lugares.
2. **Duplicación de la configuración.** Habría que recrear la CI, los permisos del equipo, las
   reglas de protección y los enlaces ya entregados al docente.
3. **Señal equivocada.** Un proyecto que cambia de repositorio a mitad de curso sugiere
   inestabilidad, no gobierno.

Gobernar el repositorio existente demuestra exactamente lo que la actividad busca: que el equipo
es capaz de **ordenar** lo que ya construyó.

---

## 4. Modelo de gobierno

### 4.1 Roles

| Rol | Responsabilidad | Integrante |
|-----|-----------------|------------|
| Mantenedor | Protección de ramas, etiquetas, *releases*, revisión de cambios estructurales | Bolívar A. Valenzuela M. |
| Revisor | Aprobación formal de los PR de los demás | Rotativo entre los tres integrantes |
| Contribuidor | Propone cambios por rama y PR; nunca empuja a `main` | Todo el equipo |

Regla estructural: **nadie aprueba su propio cambio**.

### 4.2 Ramas

Modelo *trunk-based* simplificado: `main` siempre estable y una rama de vida corta por cambio.
La nomenclatura es `tipo/descripcion-breve` (`feat/`, `fix/`, `docs/`, `chore/`, `test/`).

Se eligió este modelo frente a Git Flow porque el equipo es de tres personas y las entregas son
semanales: mantener `develop` y ramas de `release` habría añadido ceremonia sin beneficio.

### 4.3 Commits

Se adopta **Conventional Commits 1.0.0** con alcance: `tipo(alcance): descripción`.
Los tipos permitidos y los alcances del proyecto están enumerados en `CONTRIBUTING.md`.

El mensaje responde a *por qué*, no a *qué*: el *qué* ya lo muestra el diff.

### 4.4 Revisión y fusión

Todo cambio entra por *pull request* con la plantilla del repositorio, que obliga a declarar el
alcance, el issue relacionado y la verificación ejecutada. La fusión es **squash**, de modo que
`main` conserva un commit por cambio y no el ruido intermedio.

### 4.5 Versionado y liberaciones

**SemVer 2.0.0** (`MAYOR.MENOR.PARCHE`) con etiqueta anotada y *release* en GitHub.
Cada hito del módulo corresponde a una versión: `v0.1.0` (H1), `v0.2.0` (H2), `v0.3.0` (H3).

### 4.6 Protección de la rama principal

Configuración aplicada en GitHub sobre `main`:

- Push directo bloqueado.
- Obligatorio abrir *pull request*.
- Obligatoria **1 aprobación** de otro integrante.
- Se descartan las aprobaciones anteriores cuando se sube un commit nuevo.
- Obligatorio resolver las conversaciones del PR antes de fusionar.
- Bloqueados el *force push* y la eliminación de la rama.
- Las reglas aplican también al administrador (**Do not allow bypassing**).
- Obligatorio que la CI (`Spectral + Ruff + pytest`) esté en verde.

Esta configuración es la que convierte las reglas escritas en reglas **exigibles**: sin ella,
`CONTRIBUTING.md` sería una recomendación.

La regla vigente se puede comprobar en cualquier momento sin abrir la interfaz:

```bash
gh api repos/bolimirme16/modulo-gestion-31-de-enero/branches/main/protection
```

La salida esperada está guardada en `docs/evidencias/09-proteccion-de-main.txt`.

### 4.7 Gestión de secretos

Una auditoría posterior al cierre detectó dos debilidades en el código del producto y se
corrigieron en el mismo hito:

| Hallazgo | Riesgo | Corrección |
|----------|--------|------------|
| `app.secret_key` con valor literal en `app.py` | Cualquiera con acceso al repositorio podía firmar cookies de sesión | La clave se lee de `SECRET_KEY` o se genera con `secrets.token_urlsafe(48)` en `clave_sesion.key`, fuera del control de versiones |
| Contraseña inicial `secretaria / 31enero2026` escrita en el código, los manuales y la pantalla de login | Credencial compartida y pública en cinco archivos | Se genera al azar en el primer arranque y se escribe una sola vez en `clave_inicial.txt`; la documentación ya no reproduce ninguna clave |

`.gitignore` excluye `clave_sesion.key`, `clave_inicial.txt`, `.env`, `*.pem` y `*.key`. La
verificación es reproducible con:

```bash
git grep -n -i "secret_key\|31enero2026" -- . ':!docs/10-gobierno-del-repositorio.md'
```

que no debe devolver coincidencias fuera de este documento.

> **Decisión registrada — visibilidad del repositorio.** GitHub no aplica protección de ramas
> ni *rulesets* a repositorios **privados** en el plan gratuito: la propia interfaz advierte que
> las reglas «no se aplicarán hasta pasar a una organización con GitHub Team». Para que la
> protección fuera real y no solo declarativa se cambió la visibilidad a **pública**, después de
> comprobar que el historial no contiene bases de datos ni datos personales reales (`*.db` está
> excluido desde el primer commit y los ejemplos usan cédulas ficticias). La auditoría de
> credenciales se hizo después y su resultado se documenta en §4.7. La alternativa habría sido
> pagar GitHub Team o aceptar reglas no aplicadas; ninguna de las dos se consideró adecuada para
> el alcance del proyecto.

---

## 5. Estructura normalizada

```
.
├─ .github/
│  ├─ CODEOWNERS                     # Propietarios por área
│  ├─ pull_request_template.md       # Plantilla obligatoria de PR
│  ├─ ISSUE_TEMPLATE/                # Tarea y defecto
│  └─ workflows/ci.yml               # Spectral + Ruff + pytest
├─ CONTRIBUTING.md                   # Reglas de trabajo
├─ CHANGELOG.md                      # Historial de versiones
├─ SECURITY.md                       # Reporte de vulnerabilidades
├─ LICENSE                           # MIT
├─ .gitattributes                    # Finales de línea y binarios
├─ .editorconfig                     # Estilo de edición
├─ api/  src/  tests/                # Producto
└─ docs/                             # Documentación y evidencias
```

---

## 6. Protección de datos personales

El sistema administra cédulas, cuotas y estados de cuenta de personas reales. El gobierno trata
ese riesgo como un elemento de configuración más:

- Las bases `*.db` y `*.sqlite3` están en `.gitignore` y nunca se versionan.
- Las pruebas y ejemplos usan datos ficticios.
- No se incluyen capturas con información real en `docs/`.
- El contrato OpenAPI expone `socioId` (UUID) y deja la cédula como `writeOnly`.
- Los incidentes se reportan según `SECURITY.md`.

---

## 7. Trazabilidad regla → evidencia

| Regla | Dónde se declara | Cómo se verifica |
|-------|------------------|------------------|
| Nadie empuja a `main` | `CONTRIBUTING.md` §2 | Protección de rama en GitHub |
| Un commit por cambio, con formato | `CONTRIBUTING.md` §3 | `git log --oneline` |
| Revisión de otra persona | `CONTRIBUTING.md` §1 y §5 | Historial de revisiones de cada PR |
| CI obligatoria | `.github/workflows/ci.yml` | Estado del *check* en cada PR |
| Propietarios por área | `.github/CODEOWNERS` | Revisores solicitados automáticamente |
| Versión publicada | `CHANGELOG.md` + etiqueta | `git tag -l` y *release* en GitHub |
| Sin datos personales | `.gitignore` + `SECURITY.md` | `git ls-files` sin `.db` |

---

## 8. Aporte de cada integrante

El historial del repositorio permite atribuir cada cambio a su autor. En el hito H3:

| Integrante | Rama | Aporte |
|------------|------|--------|
| Bolívar A. Valenzuela M. | `chore/gobernanza`, `chore/higiene`, `docs/matriz-git-svn`, `fix/dependencias-flask`, `practica/conflicto-a` | `CONTRIBUTING.md`, `LICENSE`, `CODEOWNERS`, plantillas de PR e issue, este documento, protección de `main`, `.gitattributes`, `.editorconfig`, matriz Git vs SVN, ADR-004, revisión de dependencias y el conflicto deliberado |
| José Miguel Guerrero T. | `docs/changelog`, `docs/aporte-jose` | `CHANGELOG.md` con el historial H1–H3, `SECURITY.md` y el registro de participación individual |
| Valery Lucero B. | `valery/toolchain` (hito H2) | Mapa de *toolchain* e historias de usuario. Sin cambios propios en H3 |

Cada rama se integró mediante un *pull request* revisado por otro integrante, de modo que el
aporte individual es visible tanto en los commits como en las revisiones.

> **Registro honesto.** En H3 solo dos integrantes produjeron cambios: la tercera integrante no
> participó en este hito. La tabla lo declara en lugar de atribuirle trabajo ajeno, porque una
> atribución falsa sería un defecto de auditoría más grave que la ausencia misma. El historial de
> `git log` y de la API de GitHub es la fuente de verdad y contradice cualquier atribución
> inventada.

---

## 9. Resultados

- Siete *pull requests* fusionados con revisión cruzada (y dos más del hito anterior).
- `main` protegida: sin push directo y con CI obligatoria, también para el administrador.
- Ramas de trabajo conservadas tras la fusión (`chore/*`, `docs/*`, `fix/*`, `practica/*`) y las
  dos de hitos anteriores (`valery/toolchain`, `contratos-api-bdd`): se mantienen como evidencia
  de auditoría, no como trabajo pendiente.
- Ninguna credencial en el repositorio: clave de sesión generada en el primer arranque y
  contraseña inicial aleatoria (ver §4.7).
- Versión `v0.3.0` publicada con notas de liberación.
- Documentación de gobierno completa y enlazada desde el `README`.

---

## 10. Referencias

International Organization for Standardization. (2017). *ISO 10007:2017 Quality management —
Guidelines for configuration management*. ISO.

ISO/IEC/IEEE. (2017). *ISO/IEC/IEEE 12207:2017 Systems and software engineering — Software life
cycle processes*. ISO.

Preston-Werner, T. (2013). *Semantic Versioning 2.0.0*. https://semver.org/
