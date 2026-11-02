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

## Causa del conflicto

Git detecta un conflicto cuando dos ramas modifican **la misma línea** del mismo archivo desde su
ancestro común. El ancestro es `ef47452`; a partir de él, `practica/conflicto-a` cambió la línea
en `c63833d` y `practica/conflicto-b` la cambió en `4196d2b`. Al fusionar, Git no puede decidir
cuál de las dos redacciones es la correcta y no elige por su cuenta: se detiene y delega la
decisión.

```
$ git merge practica/conflicto-b
Auto-merging docs/11-practica-de-conflicto.md
CONFLICT (content): Merge conflict in docs/11-practica-de-conflicto.md
Automatic merge failed; fix conflicts and then commit the result.
```

## Marcadores que dejó Git

Git anotó el archivo con las tres marcas estándar: `<<<<<<<` abre el bloque de **nuestra** rama,
`=======` separa las dos versiones y `>>>>>>>` cierra el bloque de **su** rama.

```
<<<<<<< HEAD
Integrar a `main` al menos una vez al día, salvo cambios de emergencia.
=======
Integrar a `main` al menos una vez al día o antes de cada revisión.
>>>>>>> practica/conflicto-b
```

## Resolución del conflicto

| Rama | Redacción que propuso |
|------|----------------------|
| `practica/conflicto-a` | Integrar a `main` al menos una vez al día, salvo cambios de emergencia. |
| `practica/conflicto-b` | Integrar a `main` al menos una vez al día o antes de cada revisión. |

Se conservaron las tres condiciones de las dos propuestas: la frecuencia mínima diaria, el
disparador de la revisión y la excepción por emergencia. Ninguna rama impuso su redacción: la
regla final es la suma de ambas, revisada por escrito antes de fusionar. La resolución se registró
en el commit de fusión `e64fc60`, y el archivo final no conserva ningún marcador.

## Cada caso tenía una sola respuesta correcta

Ninguna de las dos redacciones era errónea: cada una expresaba una condición que el equipo
necesitaba. Por eso la resolución no fue «elegir una» sino «conservar las tres condiciones en una
sola frase». Esa es la diferencia entre resolver un conflicto y descartar el trabajo de alguien.

## Cómo prevenirlo

Un conflicto no se previene con la herramienta, sino con **disciplina de integración**. Las cinco
medidas que el equipo adoptó:

1. **Ramas cortas.** La rama vive horas, no semanas. El conflicto aparece cuando el contexto aún
   está fresco y la resolución cuesta minutos, no una reconstrucción.
2. **Integrar `main` en la rama antes de abrir el PR.** Detecta el conflicto en el entorno de
   quien lo provocó, no en el de quien revisa (es lo que hace `update-branch` en GitHub).
3. **Commits atómicos.** Un cambio por commit permite identificar qué línea se tocó y por qué;
   un commit que mezcla cinco cambios obliga a leer el diff completo para resolver una línea.
4. **Un tema por rama.** Si dos ramas tocan el mismo archivo por razones distintas, el conflicto
   es inevitable; si cada rama toca solo su tema, la superposición se reduce al mínimo.
5. **Acuerdo escrito antes de editar.** Cuando dos personas trabajan sobre la misma regla, el
   texto se acuerda primero y se edita después; el conflicto deja de ser una negociación a
   ciegas bajo presión.

## Por qué se provocó el conflicto

Un conflicto no es un error, es información: dos cambios tocaron la misma línea. Lo que evita
el conflicto no es la herramienta, sino la **duración de la rama**. En este ejercicio las dos
ramas vivieron minutos, por lo que el conflicto se detectó y resolvió en el mismo bloque de
trabajo; si hubieran vivido semanas, la misma línea habría arrastrado cambios de otros archivos
y la resolución habría exigido reconstruir el contexto.
