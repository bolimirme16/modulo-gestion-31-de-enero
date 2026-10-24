"""Pruebas BDD (Gherkin) derivadas de los criterios de aceptación — tarea T7.

Los escenarios viven en `tests/features/` y son la versión ejecutable de los
criterios de aceptación redactados en `docs/07-historias-y-criterios.md`. Se
ejecutan con pytest-bdd sobre la capa de reglas (`src/reglas.py`), sin datos
personales reales.
"""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

import reglas

scenarios("features")


@pytest.fixture
def ctx():
    """Contexto mutable compartido por los pasos del escenario."""
    return {}


# --- Antecedentes -------------------------------------------------------------
@given("una base de datos local vacía")
def _base_vacia(ctx):
    ctx["conn"] = reglas.conectar(":memory:")


@given(parsers.parse("una reunión mensual abierta con grupo de turno {grupo:d}"))
def _reunion_abierta(ctx, grupo):
    ctx["reunion"] = reglas.abrir_reunion(ctx["conn"], "2026-10-31", grupo_turno=grupo)


# --- Dado ---------------------------------------------------------------------
@given(parsers.parse('un socio activo de cédula "{cedula}" en el grupo {grupo:d}'))
def _socio_activo(ctx, cedula, grupo):
    ctx["socio"] = reglas.crear_socio(ctx["conn"], cedula, "Socio de prueba BDD", grupo)


# --- Cuando -------------------------------------------------------------------
@when(parsers.parse('registro su asistencia como "{estado}"'))
def _registrar_asistencia(ctx, estado):
    ctx["resultado"] = reglas.registrar_asistencia(
        ctx["conn"], ctx["reunion"]["reunionId"], ctx["socio"]["socioId"], estado
    )


@when("registro el cobro del café")
def _registrar_cafe(ctx):
    ctx["resultado"] = reglas.registrar_cafe(
        ctx["conn"], ctx["reunion"]["reunionId"], ctx["socio"]["socioId"]
    )


# --- Entonces -----------------------------------------------------------------
@then(parsers.parse("la multa aplicada es de {multa:f} dólares"))
def _verificar_multa(ctx, multa):
    assert ctx["resultado"]["multa"] == multa


@then(parsers.parse("la tarifa aplicada es de {tarifa:f} dólares"))
def _verificar_tarifa(ctx, tarifa):
    assert ctx["resultado"]["tarifa"] == tarifa
