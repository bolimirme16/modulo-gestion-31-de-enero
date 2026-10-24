
const { Given, When, Then } = require('@cucumber/cucumber');
const assert = require('node:assert/strict');
const { login } = require('../../src/login');

let email;
let password;
let resultado;

Given('que el usuario registrado tiene el correo {string}', function (correo) {
  email = correo;
});

When('inicia sesión con la contraseña {string}', function (contrasena) {
  password = contrasena;
  resultado = login(email, password);
});

Then('el inicio de sesión debe ser exitoso', function () {
  assert.equal(resultado.success, true);
  assert.equal(resultado.page, 'dashboard');
});

Then('el inicio de sesión debe ser rechazado', function () {
  assert.equal(resultado.success, false);
  assert.equal(resultado.message, 'Credenciales inválidas');
});
