# Práctica de conflicto deliberado

Ejercicio de las sesiones 7 y 8 del módulo: dos ramas modifican **la misma línea** del mismo
archivo para provocar un conflicto de fusión y dejar registrada su resolución con número de
rama, commit y pull request.

## Procedimiento seguido

1. `practica/conflicto-a` crea este archivo con la regla acordada.
2. `practica/conflicto-b` parte de esa base y reescribe la regla.
3. `practica/conflicto-a` también reescribe la misma línea, con otra redacción.
4. Al fusionar `b` sobre `a`, Git marca el conflicto en esta línea.
5. La resolución se registra en el commit de fusión y el resultado entra por *pull request*.

## Regla acordada por el equipo

Integrar a `main` al menos una vez al día o antes de cada revisión, salvo cambios de emergencia.

## Resolución del conflicto

| Rama | Redacción que propuso |
|------|----------------------|
| `practica/conflicto-a` | Integrar a `main` al menos una vez al día, salvo cambios de emergencia. |
| `practica/conflicto-b` | Integrar a `main` al menos una vez al día o antes de cada revisión. |

Se conservaron las tres condiciones de las dos propuestas: la frecuencia mínima diaria, el
disparador de la revisión y la excepción por emergencia. Ninguna rama impuso su redacción: la
regla final es la suma de ambas, revisada por escrito antes de fusionar.

## Por qué se provocó el conflicto

Un conflicto no es un error, es información: dos cambios tocaron la misma línea. Lo que evita
el conflicto no es la herramienta, sino la **duración de la rama**. En este ejercicio las dos
ramas vivieron minutos, por lo que el conflicto se detectó y resolvió en el mismo bloque de
trabajo; si hubieran vivido semanas, la misma línea habría arrastrado cambios de otros archivos
y la resolución habría exigido reconstruir el contexto.
