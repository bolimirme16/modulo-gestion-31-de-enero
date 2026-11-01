# Registro de participación individual — SEM03

- **Integrante:** José Miguel Guerrero Tapia
- **Hito:** H3 · v0.3.0 · Repositorio gobernado
- **Período:** 25/10/2026 – 01/11/2026

## 1. Pull requests abiertos

| PR | Rama | Aporte | Estado |
|---|---|---|---|
| **#6** | `docs/changelog` | `CHANGELOG.md` con historial de versiones (Keep a Changelog + SemVer), `LICENSE` (MIT) y `SECURITY.md` | fusionado en `77ba4a1` (head `813cdd4`) |
| **#16** | `docs/aporte-jose` | Este registro de participación individual | en revisión |

## 2. Revisiones cruzadas realizadas

| PR revisado | Autor | Fecha | Resultado |
|---|---|---|---|
| **#5** `chore/gobernanza` | Bolívar Valenzuela | 31/10/2026 | Aprobado |
| **#15** `fix/dependencias-flask` | Bolívar Valenzuela | 01/11/2026 | Aprobado |
| **#13** `docs/matriz-git-svn` | Bolívar Valenzuela | 01/11/2026 | Aprobado |
| **#8** `chore/higiene` | Bolívar Valenzuela | 01/11/2026 | Aprobado |

Ninguna de estas revisiones es del propio autor del PR: es la regla de revisión cruzada que exige
la protección de `main`.

## 3. Verificación de la integración continua

Cada PR aprobado se comprobó contra la verificación obligatoria `Spectral + Ruff + pytest` antes
de fusionar. En el PR #15 la verificación incluyó además la consulta a la API de OSV sobre las
dependencias fijadas, que encontró cuatro avisos sobre Flask 3.1.0 y cero sobre 3.1.3.

## 4. Trazabilidad

- Los cambios de este documento entran por una **rama independiente** (`docs/aporte-jose`) y un
  *pull request* dirigido a `main`, nunca por push directo.
- Los PR **#7** y **#16** están vinculados a su issue mediante `Closes #n`. Los PR **#5** y **#6**
  se fusionaron antes de que existieran sus issues, así que el vínculo se registró a posteriori
  (el issue #9 se cerró con la referencia al `42dcaff`).
- La fusión se hace por *squash*, de modo que cada PR deja **un** commit en `main` con su número.

## 5. Estado

Documento presentado como aporte de documentación del hito SEM03, dentro del flujo
issue → rama → PR → revisión cruzada → fusión descrito en `CONTRIBUTING.md`.
