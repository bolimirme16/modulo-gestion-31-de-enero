# Manual rápido de uso — Asociación “31 de Enero Narciza de Jesús” (v1.2.0)

> Guía operativa resumida. La versión extendida está en [`04-manual-de-uso.md`](04-manual-de-uso.md).

## Forma recomendada: programa (EXE)

1. Copiar la carpeta `dist/Modulo Gestion 31 DE ENERO NARCIZA DE JESUS` a un lugar con escritura (Documentos o USB).
2. Doble clic en `Modulo Gestion 31 DE ENERO NARCIZA DE JESUS.exe` (tiene el logo). Sale el splash vinotinto con el logo (~6 s) y abre en pantalla completa. No necesita Python ni muestra direcciones web.
3. La base `asociacion.db` se crea junto al ejecutable. Respaldo = copiar ese archivo.

## Forma alternativa: desde código

1. Doble clic en `iniciar.bat` (requiere Python + `pip install -r requirements.txt`).

## Uso diario (igual en ambas)

1. **Login:** usuario `secretaria` / clave `31enero2026`. Cámbiela en Config.
2. **Socios:** cédula de 10 dígitos; los montos aceptan punto o coma (25.50 o 25,50). N.º y orden alfabéticos automáticos (sin digitar).
3. **Reunión (último sábado):** generar asistencia/café/mensualidad, cobrar y, al final, *Terminar sesión y guardar* (bloquea la edición; Reabrir solo para corregir). Extraordinarios: otra fecha + título, solo pasa lista.
4. **Consulta** por cédula: comprobante formal con logo, firmas y espacio para sello.
5. **Caja:** columna Comprobante/Obs (N.º de factura). Corte con logo para imprimir.
6. **Auditoría:** filtra por fecha + cédula + tipo. Reporte con logo.
7. **Config:** integridad (9 chequeos), descargar respaldo `.db`, clave y logo.
8. **Cerrar:** botón rojo (Cerrar programa, arriba a la derecha) apaga todo.

**Respaldo:** copiar `asociacion.db` a USB cada reunión.
