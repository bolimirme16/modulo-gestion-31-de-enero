## Qué cambia

<!-- Describa el cambio en una o dos frases. -->

## Por qué

<!-- Problema o necesidad que resuelve. Indique el issue relacionado. -->

Closes #

## Tipo de cambio

- [ ] `feat` — funcionalidad nueva
- [ ] `fix` — corrección de un defecto
- [ ] `docs` — documentación
- [ ] `test` — pruebas
- [ ] `refactor` — cambio interno sin alterar comportamiento
- [ ] `chore` / `ci` / `build` — mantenimiento, integración continua o empaquetado

## Cómo se verificó

- [ ] `spectral lint api/openapi.yaml` sin errores
- [ ] `ruff check src tests scripts` limpio
- [ ] `bandit -q -r src -x src/generated -ll` sin hallazgos medios o altos
- [ ] `pytest -q` en verde (indique el número de pruebas)
- [ ] `python scripts/build_docs.py --out site` sin enlaces rotos
- [ ] Revisión manual de la interfaz, si aplica

Evidencia (salida, captura o ruta en `docs/evidencias/`):

## Lista de verificación del autor

- [ ] La rama se creó desde `main` actualizado
- [ ] El mensaje de commit sigue Conventional Commits
- [ ] No se subieron bases `.db`, credenciales ni datos personales reales
- [ ] La documentación afectada quedó actualizada
- [ ] La matriz `docs/05-trazabilidad.md` se actualizó si cambiaron HU, CA, E o ADR
- [ ] El `CHANGELOG.md` se actualizó, si el cambio es visible para el usuario

## Lista de verificación del revisor

- [ ] El cambio corresponde al issue y no incluye modificaciones ajenas
- [ ] La CI está en verde
- [ ] No hay datos sensibles en el diff
- [ ] Aprobado con el botón **Approve**
