#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lanzador de escritorio: splash con logo + servidor waitress + ventana interna fullscreen.
Doble clic en iniciar.bat. No muestra URLs ni consola técnica a la secretaria."""
import os
import sys
import threading
import time
import tkinter as tk
import urllib.request

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
_cand = os.path.join(BASE_DIR, "resources", "logo_asociacion.png")
if not os.path.exists(_cand):
    _cand = os.path.join(BASE_DIR, "_internal", "resources", "logo_asociacion.png")
LOGO = _cand
VINO = "#5e0a0a"
VINO_CLARO = "#8a1414"
DORADO = "#e8b73a"
CREMA = "#fdf6e3"
URL = "http://127.0.0.1:5000"
TITULO = "Asociación 31 de Enero Narciza de Jesús"
MIN_SPLASH = 6  # segundos mínimos visibles del splash

import app as sistema  # noqa: E402


class Splash:
    """Pantalla completa vinotinto con barra dorada animada (canvas propio, sin ttk)."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TITULO)
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=VINO)
        self.progreso = 0  # 0..100 (lo mueve el hilo de trabajo)
        self.puntos = 0    # animación de "…"
        self.mensaje = "Iniciando…"
        self.cerrado = False

        centro = tk.Frame(self.root, bg=VINO)
        centro.place(relx=0.5, rely=0.5, anchor="center")
        try:
            img = tk.PhotoImage(file=LOGO).subsample(2, 2)  # 812px -> ~400px
            self._img = img
            tk.Label(centro, image=img, bg=VINO,
                     highlightthickness=0, bd=0).pack(pady=(0, 12))
        except Exception:
            tk.Label(centro, text="🏠", font=("Arial", 90), bg=VINO, fg=CREMA).pack()
        tk.Label(centro, text="ASOCIACIÓN 31 DE ENERO\nNARCIZA DE JESÚS",
                 font=("Arial", 24, "bold"), fg=CREMA, bg=VINO, justify="center").pack()
        tk.Label(centro, text=f"Sistema de gestión de socios  •  Versión {sistema.VERSION}",
                 font=("Arial", 11), fg=DORADO, bg=VINO).pack(pady=(6, 16))
        self.msg = tk.Label(centro, text=self.mensaje, font=("Arial", 12),
                            fg=CREMA, bg=VINO)
        self.msg.pack(pady=(0, 8))
        # barra de progreso dibujada a mano: riel + relleno dorado + brillo móvil
        self.ancho = 420
        self.lienzo = tk.Canvas(centro, width=self.ancho, height=16, bg=VINO_CLARO,
                               highlightthickness=0, bd=0)
        self.lienzo.pack()
        self.relleno = self.lienzo.create_rectangle(0, 0, 0, 16, fill=DORADO, outline="")
        self.brillo = self.lienzo.create_rectangle(0, 0, 40, 16, fill="#ffe9a8", outline="",
                                                  stipple="gray25")
        self.porc = tk.Label(centro, text="0%", font=("Arial", 10, "bold"),
                             fg=DORADO, bg=VINO)
        self.porc.pack(pady=(6, 0))
        tk.Label(self.root, text="© Asociación 31 de Enero Narciza de Jesús",
                 font=("Arial", 9), fg="#d9a5a5", bg=VINO).place(relx=0.5, rely=0.97, anchor="center")
        self._brillo_x = 0
        self._animar()
        self.root.update()

    def _animar(self):
        if self.cerrado:
            return
        # relleno según progreso real
        w = self.ancho * min(max(self.progreso, 0), 100) / 100.0
        self.lienzo.coords(self.relleno, 0, 0, w, 16)
        # brillo dorado barriendo la barra (siempre se mueve)
        self._brillo_x = (self._brillo_x + 9) % (self.ancho + 80) - 40
        self.lienzo.coords(self.brillo, self._brillo_x, 0, self._brillo_x + 40, 16)
        # puntos suspensivos animados
        self.puntos = (self.puntos + 1) % 4
        base = self.mensaje.rstrip(".")
        self.msg.config(text=base + "." * self.puntos)
        self.porc.config(text=f"{int(min(max(self.progreso, 0), 100))}%")
        self.root.after(60, self._animar)

    def paso(self, texto, pct=None):
        self.mensaje = texto
        if pct is not None:
            self.progreso = pct

    def cerrar(self):
        self.cerrado = True
        try:
            self.root.destroy()
        except Exception:
            pass


def servidor_listo(timeout=20):
    ini = time.time()
    while time.time() - ini < timeout:
        try:
            with urllib.request.urlopen(URL + "/login", timeout=2) as r:
                if r.status == 200:
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def abrir_ventana():
    """Ventana interna fullscreen. Plan B: Edge/Chrome modo app si no hay WebView2."""
    try:
        import webview
        webview.create_window(TITULO, URL, fullscreen=True)
        webview.start()
        return True
    except Exception as e:
        print(f"pywebview no disponible ({e}), usando navegador modo app…")
    import shutil
    import subprocess
    for exe in ("msedge", "chrome"):
        ruta = shutil.which(exe)
        if ruta:
            subprocess.Popen([ruta, f"--app={URL}"])
            return True
    import webbrowser
    webbrowser.open(URL)
    return False


def _trabajar(splash, estado):
    """Hilo de fondo: la animación del splash sigue viva en el hilo principal."""
    try:
        splash.paso("Iniciando base de datos…", 8)
        sistema.init_db()
        splash.paso("Cargando módulos del sistema…", 30)
        from waitress import serve
        hilo = threading.Thread(target=serve, kwargs={"app": sistema.app, "host": "127.0.0.1",
                                                     "port": 5000, "_quiet": True},
                                daemon=True)
        hilo.start()
        splash.paso("Verificando datos…", 55)
        t0 = time.time()
        ok = servidor_listo()
        # completar mínimo de tiempo y progreso de forma animada
        while time.time() - t0 < MIN_SPLASH or splash.progreso < 100:
            splash.progreso = min(100, splash.progreso + 4)
            if splash.progreso >= 100 and time.time() - t0 >= MIN_SPLASH:
                break
            time.sleep(0.08)
        estado["ok"] = ok
    except Exception as e:  # noqa: BLE001
        estado["error"] = str(e)
    finally:
        estado["fin"] = True


def main():
    splash = Splash()
    estado = {"fin": False, "ok": False, "error": None}
    threading.Thread(target=_trabajar, args=(splash, estado), daemon=True).start()

    def _vigilar():
        if estado["fin"]:
            splash.cerrar()
            return
        splash.root.after(150, _vigilar)

    _vigilar()
    splash.root.mainloop()  # la animación corre aquí hasta que termina el trabajo
    if not estado["ok"]:
        print("Arranque fallido:", estado.get("error") or "servidor sin respuesta")
        return 1
    abrir_ventana()
    return 0


if __name__ == "__main__":
    sys.exit(main())
