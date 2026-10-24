
# language: es

@HU-101 @autenticacion
Característica: Inicio de sesión de usuarios registrados

  Escenario: Inicio de sesión con credenciales válidas
    Dado que el usuario registrado tiene el correo "usuario@ejemplo.com"
    Cuando inicia sesión con la contraseña "ClaveSegura123"
    Entonces el inicio de sesión debe ser exitoso

  Escenario: Inicio de sesión con contraseña incorrecta
    Dado que el usuario registrado tiene el correo "usuario@ejemplo.com"
    Cuando inicia sesión con la contraseña "incorrecta"
    Entonces el inicio de sesión debe ser rechazado
