# Guía rápida de verificación de la entrega

**Hito H3 · v0.3.1** — Cómo comprobar en cinco minutos que el repositorio cumple lo que
declara la entrega de SEM03.

Esta guía sirve para dos cosas: que un integrante nuevo pueda auditar el repositorio sin
preguntar a nadie, y que quien evalúe pueda contrastar la evidencia sin confiar en el
resumen del equipo.

---

## 1. Qué se verifica

| Afirmación de la entrega | Dónde se comprueba | Resultado esperado |
|---|---|---|
| `main` está protegida | GitHub → **Settings → Branches** | Regla sobre `main` con 1 aprobación y CI obligatoria |
| Los cambios entran por *pull request* | GitHub → **Pull requests** | PR fusionados, ninguno con push directo |
| Cada PR tiene revisión de otra persona | PR → pestaña **Conversation**, bloque de revisiones | Al menos una aprobación distinta del autor |
| Las versiones están etiquetadas | GitHub → **Releases** | `v0.1.0`, `v0.2.0`, `v0.3.0` y `v0.3.1` |
| No hay credenciales en el árbol | Buscador del repositorio (`/` o `t`) | 0 resultados para `31enero2026` |
| La integración continua pasa | GitHub → **Actions** | Última ejecución en verde sobre `main` |

---

## 2. Verificación con el navegador

No requiere instalar nada.

1. **Protección de la rama.** `Settings → Branches → Branch protection rules`. Debe
   existir una regla para `main` con *Require a pull request before merging*, al menos
   una aprobación y *Require status checks to pass*.
2. **Etiquetas.** Menú lateral derecho de la portada → **Releases**. Cada versión debe
   apuntar a su commit y tener notas.
3. **Revisiones.** Abre cualquier PR fusionado → pestaña **Conversation**. Al final
   aparece quién aprobó y cuándo. El autor nunca aparece como revisor de su propio PR.
4. **Secretos.** En la portada, toca la lupa (o la tecla `t`) y busca `31enero2026`.
   El buscador no debe devolver ningún archivo del código.

---

## 3. Verificación desde la terminal

```bash
git clone https://github.com/bolimirme16/modulo-gestion-31-de-enero
cd modulo-gestion-31-de-enero

# Historia del hito: debe mostrar los commits del hito en orden
git log --oneline --graph v0.2.0..v0.3.1

# Etiqueta entregada y qué contiene
git show v0.3.1 --stat

# Credenciales: la salida debe estar vacía
git grep -n -i "31enero2026" -- .

# Todas las etiquetas con su mensaje
git tag -n1
```

Si `git grep` devuelve alguna línea, hay un secreto versionado y la entrega no debe
considerarse válida hasta corregirlo.

---

## 4. Verificación de la protección por API

Sin salir de la terminal, con la API pública de GitHub:

```bash
curl -s https://api.github.com/repos/bolimirme16/modulo-gestion-31-de-enero/branches/main/protection
```

Debe aparecer `"required_pull_request_reviews"` con
`"required_approving_review_count": 1`, `"enforce_admins": {"enabled": true}` y
`"allow_force_pushes": {"enabled": false}`.

> Esta consulta puede requerir autenticación dependiendo de la configuración de la
> organización. La respuesta obtenida el 01/11/2026 está archivada en
> [`docs/evidencias/09-proteccion-de-main.txt`](evidencias/09-proteccion-de-main.txt).

---

## 5. Resultado de la última verificación

| Comprobación | Resultado | Fecha |
|---|---|---|
| Regla de protección sobre `main` | Cumple | 01/11/2026 |
| PR fusionados con revisión cruzada | Cumple (8 en el hito) | 01/11/2026 |
| Etiquetas SemVer con Release | Cumple (4 etiquetas) | 01/11/2026 |
| Credenciales en el árbol | Cumple (0 coincidencias) | 01/11/2026 |
| Integración continua | Cumple (34 pruebas) | 01/11/2026 |

---

## 6. Si algo no coincide

Abre un *issue* con la plantilla de defecto (`.github/ISSUE_TEMPLATE/`), indicando:

- qué comprobación falló,
- el comando o la ruta exacta,
- la salida obtenida y la esperada.

Un desajuste entre lo que declara la entrega y lo que muestra el repositorio es un
defecto de trazabilidad y debe quedar registrado como tal, no corregido en silencio.
