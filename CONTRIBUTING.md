# Guía de contribución

Este documento define **cómo se trabaja en este repositorio**. Su objetivo es que cualquier
cambio sea trazable: que se sepa quién lo hizo, por qué, quién lo revisó y cómo se verificó.

Proyecto: **Sistema de Gestión Automatizada y Auditoría — Asociación “31 de Enero Narciza de Jesús”**
Módulo 8 · Automatización de proceso de software · UPEC

---

## 1. Roles

| Rol | Responsabilidad | Integrante |
|-----|-----------------|------------|
| Mantenedor | Administra ramas protegidas, etiquetas y releases; aprueba cambios estructurales | Bolívar Alexander Valenzuela Mejía |
| Revisor | Revisa los PR de los demás y deja constancia de la aprobación | Todo el equipo (rotativo) |
| Contribuidor | Propone cambios mediante rama + PR; nunca empuja directo a `main` | Todo el equipo |

**Regla de oro:** nadie aprueba su propio cambio. Cada PR requiere la revisión de **otra**
persona del equipo.

---

## 2. Modelo de ramas

Se usa un modelo **trunk-based** simplificado, adecuado a un equipo pequeño y a entregas semanales.

```
main                      ← siempre estable y entregable
 └── tipo/descripcion-breve   ← una rama por cambio
```

| Rama | Uso |
|------|-----|
| `main` | Versión estable. Protegida: no admite push directo. |
| `feat/<tema>` | Funcionalidad nueva |
| `fix/<tema>` | Corrección de un defecto |
| `docs/<tema>` | Documentación |
| `chore/<tema>` | Mantenimiento, configuración, dependencias |
| `test/<tema>` | Pruebas |

Reglas:

- La rama se crea **desde `main` actualizado**.
- Vive lo mínimo necesario; al fusionarse, se elimina.
- El nombre va en minúsculas, sin acentos ni espacios: `docs/gobernanza`, `fix/cierre-caja`.

---

## 3. Convención de mensajes de commit

Se adopta **Conventional Commits 1.0.0**, con alcance entre paréntesis.

```
<tipo>(<alcance>): <descripción en imperativo, minúscula, sin punto final>

[cuerpo opcional: por qué del cambio, no qué]

[pie opcional: Refs #12 / BREAKING CHANGE: ...]
```

| Tipo | Cuándo se usa |
|------|---------------|
| `feat` | Nueva funcionalidad para el usuario |
| `fix` | Corrección de un defecto |
| `docs` | Solo documentación |
| `test` | Pruebas nuevas o corregidas |
| `refactor` | Cambio interno sin alterar el comportamiento |
| `chore` | Configuración, dependencias, herramientas |
| `ci` | Integración continua |
| `build` | Empaquetado o dependencias de construcción |
| `perf` | Mejora de rendimiento |

Alcances del proyecto: `api`, `reglas`, `ui`, `db`, `tests`, `docs`, `ci`, `repo`, `gobernanza`, `release`.

Ejemplos válidos:

```
feat(api): agregar endpoint de cierre de caja
fix(reglas): corregir redondeo de la multa por falta
docs(gobernanza): reglas de contribución y codeowners
ci(repo): fijar versión de Spectral en el flujo de validación
```

Ejemplos **no** válidos: `cambios`, `arreglos varios`, `Update README.md`, `asdf`.

---

## 4. Ciclo de un cambio

1. **Abrir un issue** que describa el problema o la necesidad.
2. **Crear la rama** desde `main`:
   ```bash
   git switch main
   git pull origin main
   git switch -c docs/gobernanza
   ```
3. **Commitear** siguiendo la convención del apartado 3.
4. **Verificar en local** antes de subir (ver apartado 6).
5. **Empujar y abrir el PR**:
   ```bash
   git push -u origin docs/gobernanza
   ```
   El PR debe completar la plantilla: qué cambia, por qué y cómo se verificó.
6. **Revisión**: otra persona del equipo revisa, comenta y aprueba. Si pide cambios, se
   corrigen en la misma rama.
7. **Fusión**: *Squash and merge* para dejar un commit limpio por cambio.
8. **Limpieza**: se borra la rama remota.

---

## 5. Reglas de revisión

El revisor comprueba, como mínimo:

- [ ] El cambio hace lo que dice el issue y nada más.
- [ ] No se subieron datos personales, bases `.db`, credenciales ni rutas absolutas.
- [ ] La CI está en verde (Spectral + Ruff + pytest).
- [ ] La documentación afectada quedó actualizada.
- [ ] El mensaje del commit sigue la convención.

Una revisión se registra con el botón **Approve** de GitHub. El comentario “ok” sin aprobación
formal no cuenta como revisión.

---

## 6. Verificación local (obligatoria antes del PR)

```bash
pip install -r requirements-dev.txt

spectral lint api/openapi.yaml     # contrato OpenAPI
ruff check src tests               # análisis estático
pytest                             # pruebas unitarias, de integración y BDD
```

Ningún PR se fusiona con la CI en rojo.

---

## 7. Versionado y liberaciones

Se usa **SemVer 2.0.0**: `MAYOR.MENOR.PARCHE`.

| Cambio | Incremento |
|--------|------------|
| Ruptura de compatibilidad | MAYOR |
| Funcionalidad nueva compatible | MENOR |
| Corrección compatible | PARCHE |

Cada hito del módulo se publica como una etiqueta anotada y un *release* en GitHub:

```bash
git switch main
git pull origin main
git tag -a v0.3.0 -m "v0.3.0 - repositorio gobernado"
git push origin v0.3.0
```

El `CHANGELOG.md` se actualiza **en el mismo PR** que introduce el cambio, no después.

---

## 8. Datos sensibles

El sistema maneja cédulas y estados de cuenta de personas reales. Por tanto:

- La base de datos (`*.db`, `*.sqlite3`) **nunca** se versiona.
- No se incluyen capturas con datos reales en `docs/`.
- Los ejemplos y pruebas usan datos ficticios.
- Un incidente se reporta según `SECURITY.md`.

---

## 9. Definition of Done

Un cambio está terminado cuando:

1. El código y la documentación están en la rama.
2. La CI pasa en verde.
3. Otro integrante aprobó el PR.
4. Se fusionó a `main` con *squash*.
5. El `CHANGELOG.md` refleja el cambio, si es visible para el usuario.
