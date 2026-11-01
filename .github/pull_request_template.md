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
- [ ] `ruff check src tests` limpio
- [ ] `pytest` en verde (indique el número de pruebas)
- [ ] Revisión manual de la interfaz, si aplica

Evidencia (salida, captura o ruta en `docs/evidencias/`):

## Lista de verificación del autor

- [ ] La rama se creó desde `main` actualizado
- [ ] El mensaje de commit sigue Conventional Commits
- [ ] No se subieron bases `.db`, credenciales ni datos personales reales
- [ ] La documentación afectada quedó actualizada
- [ ] El `CHANGELOG.md` se actualizó, si el cambio es visible para el usuario

## Lista de verificación del revisor

- [ ] El cambio corresponde al issue y no incluye modificaciones ajenas
- [ ] La CI está en verde
- [ ] No hay datos sensibles en el diff
- [ ] Aprobado con el botón **Approve**
