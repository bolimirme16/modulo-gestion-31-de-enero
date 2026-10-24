# language: es
Característica: Control de asistencia y multas por inasistencia (HU-02)
  Como Secretaria de la Asociación
  Quiero tomar lista en la reunión mensual
  Para aplicar la multa fija de $5,00 a los socios ausentes sin justificación

  Antecedentes:
    Dado una base de datos local vacía
    Y una reunión mensual abierta con grupo de turno 4

  Escenario: La inasistencia no justificada genera una multa de $5,00
    Dado un socio activo de cédula "0404445556" en el grupo 4
    Cuando registro su asistencia como "AUSENTE"
    Entonces la multa aplicada es de 5.00 dólares

  Escenario: La asistencia presente no genera multa
    Dado un socio activo de cédula "0401112223" en el grupo 4
    Cuando registro su asistencia como "PRESENTE"
    Entonces la multa aplicada es de 0.00 dólares

  Escenario: La asistencia justificada no genera multa
    Dado un socio activo de cédula "0401112224" en el grupo 4
    Cuando registro su asistencia como "JUSTIFICADO"
    Entonces la multa aplicada es de 0.00 dólares
