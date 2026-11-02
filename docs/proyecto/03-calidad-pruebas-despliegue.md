# DOCUMENTO 3 — Calidad, Pruebas y Despliegue

**Proyecto:** Módulo Gestión 31 de Enero Narciza de Jesús — **Versión:** 1.2.0

---

## 1. Pruebas

**Estrategia:** pruebas funcionales automatizadas con el cliente de pruebas de Flask
(datos reales de extremo a extremo: crear socio → generar reunión → cobrar → cerrar),
más verificación manual de interfaz e impresión. Sin frameworks externos: solo
biblioteca estándar + `test_client`.

### Casos ejecutados (todos ✅ en v1.2.0)

| ID | Caso | Resultado esperado | Resultado |
|----|------|--------------------|-----------|
| P-01 | Últimos sábados oct/nov/dic-2026 | 31, 28, 26 | ✅ |
| P-02 | Comisiones órdenes 1,7,8,63,64,69 | C1,C1,C2,C9,C10,C10 | ✅ |
| P-03 | Rotación oct-26→nov→dic→ago-27 | C1,C2,C3,C1 | ✅ |
| P-04 | Flujo reunión: falta=$5, café turno $1.50, mensualidad $25 | Multa DEBE; café 1.50; 3 mensualidades $75 | ✅ |
| P-05 | Cédulas inválidas (`123`, letras, verificador mal) | Rechazo/advertencia | ✅ |
| P-06 | Cierre bloquea edición; reabrir permite corregir | Bloqueo + reapertura | ✅ |
| P-07 | Montos `25,50`/`$ 25,50` vs `25..50`/`2.5.5`/`abc` | Acepta / rechaza con mensaje | ✅ |
| P-08 | Orden alfabético (Zumba/Abad/Mora) | Abad=1, Mora=2, Zumba=3 | ✅ |
| P-09 | Extra 2026-10-15: café/mens bloqueados, solo lista | Bloqueo + tabla oculta | ✅ |
| P-10 | Rutas sin login → 302 a `/login`; login ok → 200 | Protección total | ✅ |
| P-11 | Integridad detecta huérfano + sobrepago | Badges REVISAR | ✅ |
| P-12 | Respaldo descarga `.db` con fecha | 200 + attachment | ✅ |
| P-13 | Dashboard: 5 pasteles `conic-gradient` + barras top 5 | Render con datos | ✅ |
| P-14 | EXE: splash → ventana interna → `/login` 200, logo 1 MB | Sin Edge externo; BD junto al exe | ✅ |
| P-15 | Splash fullscreen + animación sin congelar | `fullscreen=1`, barra animada | ✅ |

**Integridad continua (en la app):** `/integridad` ejecuta 9 chequeos (límite 69, cédulas,
orden 1..N, N° únicos, huérfanos ×3, valores raros, caja, `quick_check`).

## 2. Despliegue

### Entornos

| Entorno | Descripción |
|---------|-------------|
| Desarrollo | Carpeta fuente + `python app.py` / `escritorio.py`; BD `asociacion.db` local |
| Entrega (producción) | `dist/Modulo Gestion 31 DE ENERO NARCIZA DE JESUS/` en PC de secretaria o USB |

### Construcción del EXE (reproducible)

```powershell
pyinstaller --noconfirm --clean --onedir --noconsole `
  --name "Modulo Gestion 31 DE ENERO NARCIZA DE JESUS" `
  --icon "resources\logo.ico" `
  --add-data "templates;templates" --add-data "static;static" --add-data "resources;resources" `
  --hidden-import waitress --hidden-import webview --hidden-import clr --hidden-import bottle `
  escritorio.py
```

Guardado en `Modulo Gestion 31 DE ENERO NARCIZA DE JESUS.spec` para reconstruir con
`pyinstaller <nombre>.spec`.

### Instalación en destino (checklist)

1. Carpeta del EXE en lugar con escritura (Documentos o USB). 2. WebView2 presente
   (Windows 10/11 lo trae; si no, instalador gratuito Microsoft). 3. Doble-clic al EXE.
4. Login con `secretaria` y la clave de `clave_inicial.txt`, y cambiarla en Config. 5. Verificar integridad.
6. Primera carga de los 69 socios.

### Respaldo y rollback

- **Respaldo:** Config → Descargar respaldo (`.db` con fecha) o copiar `asociacion.db` al USB
  cada reunión. **Rollback:** reemplazar el `.db` por la copia anterior con el programa cerrado.
- Sin CI/CD: despliegue manual por carpeta; cada versión se entrega como carpeta nueva
  (v1.0.0 inicial, v1.1.0 escritorio+splash, v1.2.0 exe+pasteles+integridad).
