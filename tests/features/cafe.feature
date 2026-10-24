# language: es
Característica: Cobro del servicio de café según el grupo de rotación (HU-03)
  Como Secretaria de la Asociación
  Quiero cobrar el café según la comisión responsable de la reunión
  Para que el grupo de turno pague $1,50 y el resto de grupos pague $3,00

  Antecedentes:
    Dado una base de datos local vacía
    Y una reunión mensual abierta con grupo de turno 4

  Esquema del escenario: La tarifa depende del grupo del socio
    Dado un socio activo de cédula "0400000001" en el grupo <grupo_socio>
    Cuando registro el cobro del café
    Entonces la tarifa aplicada es de <tarifa> dólares

    Ejemplos:
      | grupo_socio | tarifa |
      | 4           | 1.50   |
      | 1           | 3.00   |
      | 10          | 3.00   |
