# Política de seguridad

## Alcance

Este repositorio contiene el código y la documentación del Sistema de Gestión de la Asociación
“31 de Enero Narciza de Jesús”. El sistema opera **de forma local y sin conexión a internet**,
pero administra datos personales de socios (nombres, cédulas, cuotas y estados de cuenta).

## Versiones soportadas

| Versión | Soporte |
|---------|---------|
| 0.3.x | Sí — versión vigente |
| 0.2.x | Solo correcciones críticas |
| 0.1.x | No |

## Qué se considera una vulnerabilidad

- Acceso a datos de un socio sin autenticación previa.
- Exposición de cédulas o estados de cuenta en registros, mensajes de error o capturas.
- Inclusión de credenciales, rutas absolutas o bases de datos en el control de versiones.
- Inyección SQL en las consultas del módulo de socios.
- Manipulación del cierre de caja o de los saldos sin registro de auditoría.

## Qué **no** se considera una vulnerabilidad

- La ausencia de HTTPS en la ejecución local (el servicio escucha solo en `127.0.0.1`).
- El acceso físico al equipo donde corre la aplicación.
- La falta de autenticación multifactor, fuera del alcance del producto.

## Cómo reportar

1. **No abra un issue público** con el detalle del problema.
2. Escriba al mantenedor del repositorio indicando: versión afectada, pasos para reproducir e
   impacto estimado.
3. Recibirá confirmación en un plazo de 48 horas.
4. La corrección se desarrolla en una rama privada y se publica como versión de parche.

## Manejo de datos

- Las bases `*.db` y `*.sqlite3` **nunca** se versionan.
- Las pruebas y los ejemplos usan datos ficticios.
- No se adjuntan capturas con información real en `docs/`.
- El contrato OpenAPI expone `socioId` (UUID) y trata la cédula como campo de solo escritura.
- Antes de cada *release* se revisa el diff en busca de datos personales.

## Dependencias

Las dependencias se fijan en `requirements.txt` y `requirements-dev.txt`. Antes de cada hito se
revisa que no haya versiones con vulnerabilidades conocidas en las librerías utilizadas
(Flask, pytest, openapi-generator y Spectral CLI).
