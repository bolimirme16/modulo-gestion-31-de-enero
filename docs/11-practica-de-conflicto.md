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

Integrar a `main` al menos una vez al día o antes de cada revisión.
