
function login(email, password) {
  if (
    email === "usuario@ejemplo.com" &&
    password === "ClaveSegura123"
  ) {
    return {
      success: true,
      message: "Inicio de sesión exitoso",
      page: "dashboard"
    };
  }

  return {
    success: false,
    message: "Credenciales inválidas",
    page: "login"
  };
}

module.exports = { login };
