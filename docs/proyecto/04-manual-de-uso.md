# DOCUMENTO 4 — Manual de Uso

**Módulo Gestión 31 de Enero Narciza de Jesús — v1.2.0** (también distribuido como
`README_USO.txt` resumido)

---

## 1. Abrir y cerrar

1. Doble clic en **Modulo Gestion 31 DE ENERO NARCIZA DE JESUS.exe** (tiene el logo).
   Aparece el splash vinotinto con el logo (~6 segundos) y el sistema abre en pantalla completa.
2. Ingrese con el usuario **secretaria** y la clave que el sistema generó en **clave_inicial.txt** (misma carpeta del programa). Cámbiela en ⚙ Config.
3. Para salir use el botón rojo **⏻ Cerrar programa** (arriba a la derecha) o la X.
   Apague el PC solo cuando vea "Programa cerrado ✅".

## 2. Primera vez: registrar los 69 socios

Socios → complete cédula (10 dígitos), nombres, apellidos, fecha (calcula la edad),
estado civil (lista), domicilio y teléfono. Si arrastra deuda anterior, póngala en
*Deuda inicial* (acepta `25.50` o `25,50`). El **N° y el orden se asignan solos por
orden alfabético** y definen la comisión de café (C1–C9 de 7, C10 de 6).

## 3. Reunión del último sábado (flujo operativo)

1. **Inicio:** Reunión → elija el sábado en la lista → *Paso 1: Generar asistencia* →
   marque Presente/Permiso/Falta (falta = multa $5) y cobre multas con *Cobrar $5*.
2. **Medio:** *Paso 2: Generar café* → la comisión en turno paga **$1.50**, el resto
   **$3.00** → *Cobrar* uno por uno; el impago queda en rojo.
3. **Final:** *Paso 3: Generar mensualidades $25* → cobre en la cola (acepta abonos,
   ej. `10,50`); registre gastos en Caja si los hubo.
4. **Cierre:** botón verde **🔒 TERMINAR SESIÓN Y GUARDAR** → la sesión se bloquea
   (use *Reabrir* solo para corregir) y queda el total cobrado.
5. **Extraordinarios:** ponga otra fecha + *Guardar título* (ej. "Bingo solidario"):
   solo pasa lista, sin café ni mensualidad.

## 4. Consulta, caja, auditoría y respaldo

- **Consulta:** escriba la cédula → comprobante N° `CMP-fecha` con lo que debe por rubro
  y lo pagado → *Imprimir* (sale logo, firmas y espacio de sello).
- **Caja:** anote gastos con su N° de factura en *Comprobante/Obs*; filtre por mes e
  *Imprima el corte* para firmarlo.
- **Auditoría:** filtre por fecha + cédula + tipo (ej. `CERRAR`, `PAGO`).
- **Config:** verifique la **integridad** (todo debe salir OK), **descargue el respaldo
  .db** al USB, cambie la clave y actualice el logo si cambia.

## 5. Solución de problemas

| Síntoma | Solución |
|---------|----------|
| No abre / error WebView2 | Instale WebView2 gratuito de Microsoft; mientras tanto el sistema abre Edge modo app |
| "Cédula inválida" | Debe tener 10 números; si avisa del verificador, revísela (igual se guarda) |
| "Monto inválido" | Use `25.50` o `25,50`; nada de doble punto ni letras |
| Reunión bloqueada | Está cerrada: pulse *Reabrir* para corregir y vuelva a terminarla |
| Olvidó la clave | Reinstale la carpeta de entrega: el sistema genera una clave nueva en **clave_inicial.txt**. No se pierde nada si tiene respaldo |
| PC nuevo | Copie la carpeta del programa + pegue su último `.db` como `asociacion.db` |
