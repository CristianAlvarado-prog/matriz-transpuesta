"""
Matriz Transpuesta - Versión 3 (matrices cuadradas N x N: 2x2, 3x3 y 4x4)
Acepta enteros, decimales y fracciones (ej.: 3, 2.5, 1/2, -1/2)
------------------------------------------------
Python + Tkinter (no requiere instalar nada extra). Funciona en Windows y Mac.

Ejecutar:
    python matriz_transpuesta_v2.py      (Windows)
    python3 matriz_transpuesta_v2.py     (Mac)
"""

from fractions import Fraction
import sys
import tkinter as tk
from tkinter import messagebox, ttk

TAMANOS = (2, 3, 4)  # matrices cuadradas N x N permitidas

# Fuente según el sistema operativo
if sys.platform.startswith("win"):
    FUENTE = "Segoe UI"
elif sys.platform == "darwin":
    FUENTE = "Helvetica Neue"
else:
    FUENTE = "DejaVu Sans"

# Paleta de colores
C_FONDO = "#eef1f8"
C_HEADER = "#1f2a5a"
C_SUBTITULO = "#b8c4ee"
C_ACENTO = "#3b5bdb"
C_ACENTO_H = "#2f49b3"
C_VERDE = "#2f9e5b"
C_VERDE_H = "#25804a"
C_GRIS = "#6b7280"
C_GRIS_H = "#565c68"
C_TARJETA = "#ffffff"
C_BORDE = "#dde3f0"
C_TEXTO = "#1f2937"
C_CELDA_RES = "#e6f7ec"


# ----------------------------------------------------------------------
# Lógica (esto es lo importante del proyecto)
# ----------------------------------------------------------------------
def transponer(matriz):
    """Devuelve la transpuesta: el elemento A[i][j] pasa a T[j][i]."""
    filas = len(matriz)
    columnas = len(matriz[0])
    resultado = []
    for j in range(columnas):
        nueva_fila = []
        for i in range(filas):
            nueva_fila.append(matriz[i][j])
        resultado.append(nueva_fila)
    return resultado


# ----------------------------------------------------------------------
# Elementos visuales reutilizables
# ----------------------------------------------------------------------
class Boton(tk.Label):
    """Botón plano con efecto al pasar el mouse (se ve igual en Windows y Mac)."""

    def __init__(self, master, texto, comando, color, hover):
        super().__init__(master, text=texto, bg=color, fg="white",
                         font=(FUENTE, 12, "bold"), padx=20, pady=9,
                         cursor="hand2")
        self.color = color
        self.hover = hover
        self.bind("<Enter>", lambda e: self.config(bg=self.hover))
        self.bind("<Leave>", lambda e: self.config(bg=self.color))
        self.bind("<Button-1>", lambda e: comando())


def dibujar_corchete(canvas, lado, alto, color):
    canvas.delete("all")
    if lado == "izq":
        puntos = [10, 3, 3, 3, 3, alto - 3, 10, alto - 3]
    else:
        puntos = [2, 3, 9, 3, 9, alto - 3, 2, alto - 3]
    canvas.create_line(*puntos, width=3, fill=color)


def armar_matriz(marco, filas, cols, fabrica, color_fondo, color_corchete):
    """Dibuja una matriz con corchetes [ ] y devuelve la lista de celdas."""
    for w in marco.winfo_children():
        w.destroy()

    izq = tk.Canvas(marco, width=13, bg=color_fondo, highlightthickness=0)
    centro = tk.Frame(marco, bg=color_fondo)
    der = tk.Canvas(marco, width=13, bg=color_fondo, highlightthickness=0)
    izq.grid(row=0, column=0, sticky="ns")
    centro.grid(row=0, column=1, padx=4)
    der.grid(row=0, column=2, sticky="ns")

    celdas = []
    for i in range(filas):
        fila = []
        for j in range(cols):
            celda = fabrica(centro)
            celda.grid(row=i, column=j, padx=4, pady=4, ipady=6)
            fila.append(celda)
        celdas.append(fila)

    marco.update_idletasks()
    alto = centro.winfo_reqheight()
    for canvas, lado in ((izq, "izq"), (der, "der")):
        canvas.config(height=alto)
        dibujar_corchete(canvas, lado, alto, color_corchete)
    return celdas


# ----------------------------------------------------------------------
# Aplicación
# ----------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matriz Transpuesta")
        self.configure(bg=C_FONDO)
        self.geometry("900x720")
        self.minsize(800, 680)

        self.entradas = []
        self._crear_interfaz()
        self.crear_matriz()

    # ---------------- interfaz ----------------
    def _tarjeta(self, padre, titulo):
        tarjeta = tk.Frame(padre, bg=C_TARJETA, highlightbackground=C_BORDE,
                           highlightthickness=1)
        tk.Label(tarjeta, text=titulo, bg=C_TARJETA, fg=C_HEADER,
                 font=(FUENTE, 13, "bold")).pack(anchor="w", padx=16, pady=(12, 6))
        return tarjeta

    def _crear_interfaz(self):
        # Encabezado
        encabezado = tk.Frame(self, bg=C_HEADER)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="Matriz Transpuesta", bg=C_HEADER, fg="white",
                 font=(FUENTE, 24, "bold")).pack(pady=(16, 0))
        tk.Label(encabezado, text="Matrices cuadradas N × N  (2×2, 3×3 y 4×4)   ·   A  →  Aᵀ",
                 bg=C_HEADER, fg=C_SUBTITULO,
                 font=(FUENTE, 12)).pack(pady=(2, 16))

        cuerpo = tk.Frame(self, bg=C_FONDO)
        cuerpo.pack(fill="both", expand=True, padx=24, pady=14)

        # Tarjeta 1: tamaño
        t1 = self._tarjeta(cuerpo, "1.  Elige el tamaño de la matriz")
        t1.pack(fill="x")
        fila_tam = tk.Frame(t1, bg=C_TARJETA)
        fila_tam.pack(anchor="w", padx=16, pady=(0, 14))

        tk.Label(fila_tam, text="Tamaño (N × N)", bg=C_TARJETA, fg=C_TEXTO,
                 font=(FUENTE, 12)).pack(side="left")
        self.var_tam = tk.StringVar(value="3 × 3")
        combo = ttk.Combobox(fila_tam, textvariable=self.var_tam, width=7,
                             state="readonly", justify="center",
                             values=[f"{n} × {n}" for n in TAMANOS],
                             font=(FUENTE, 13))
        combo.pack(side="left", padx=(8, 22), ipady=2)
        combo.bind("<<ComboboxSelected>>", lambda e: self.crear_matriz())

        Boton(fila_tam, "Crear matriz", self.crear_matriz,
              C_ACENTO, C_ACENTO_H).pack(side="left", padx=(0, 10))
        Boton(fila_tam, "Cargar ejemplo", self.cargar_ejemplo,
              C_GRIS, C_GRIS_H).pack(side="left")

        # Tarjetas 2 y 3: matriz original y resultado (lado a lado)
        centro = tk.Frame(cuerpo, bg=C_FONDO)
        centro.pack(fill="both", expand=True, pady=14)
        centro.columnconfigure(0, weight=1, uniform="col")
        centro.columnconfigure(1, weight=1, uniform="col")
        centro.rowconfigure(0, weight=1)

        t2 = self._tarjeta(centro, "2.  Escribe la matriz  A")
        t2.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.marco_orig = tk.Frame(t2, bg=C_TARJETA)
        self.marco_orig.pack(expand=True, padx=16, pady=(4, 16))

        t3 = self._tarjeta(centro, "3.  Resultado  Aᵀ")
        t3.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.marco_res = tk.Frame(t3, bg=C_TARJETA)
        self.marco_res.pack(expand=True, padx=16, pady=(4, 6))
        self.lbl_info = tk.Label(t3, text="", bg=C_TARJETA, fg=C_GRIS,
                                 font=(FUENTE, 11, "italic"))
        self.lbl_info.pack(pady=(0, 12))

        # Botones principales
        fila_botones = tk.Frame(cuerpo, bg=C_FONDO)
        fila_botones.pack()
        Boton(fila_botones, "Transponer", self.calcular,
              C_VERDE, C_VERDE_H).pack(side="left", padx=8)
        Boton(fila_botones, "Limpiar", self.limpiar,
              C_GRIS, C_GRIS_H).pack(side="left", padx=8)

        # Paso a paso
        t4 = self._tarjeta(cuerpo, "Paso a paso")
        t4.pack(fill="x", pady=(14, 0))
        self.txt_pasos = tk.Text(t4, height=5, bg=C_TARJETA, fg=C_TEXTO,
                                 font=(FUENTE, 11), relief="flat", wrap="word",
                                 state="disabled", highlightthickness=0)
        self.txt_pasos.pack(fill="x", padx=16, pady=(0, 12))

        self.bind("<Return>", lambda evento: self.calcular())

    # ---------------- utilidades ----------------
    def _leer_dimensiones(self):
        try:
            n = int(self.var_tam.get().split()[0])
        except (ValueError, IndexError):
            n = 0
        if n not in TAMANOS:
            messagebox.showerror("Error", "El tamaño debe ser 2×2, 3×3 o 4×4.")
            return None
        return n, n

    def _escribir_pasos(self, texto):
        self.txt_pasos.config(state="normal")
        self.txt_pasos.delete("1.0", tk.END)
        self.txt_pasos.insert("1.0", texto)
        self.txt_pasos.config(state="disabled")

    def _resultado_vacio(self):
        for w in self.marco_res.winfo_children():
            w.destroy()
        tk.Label(self.marco_res, text="Aquí aparecerá\nla matriz transpuesta",
                 bg=C_TARJETA, fg=C_GRIS, font=(FUENTE, 12, "italic")
                 ).pack(pady=30)
        self.lbl_info.config(text="")
        self._escribir_pasos("Escribe los números de la matriz y presiona «Transponer».")

    def _crear_entrada(self, padre):
        return tk.Entry(padre, width=7, justify="center", font=(FUENTE, 14),
                        bg="white", fg=C_TEXTO, relief="flat",
                        highlightthickness=2, highlightbackground="#c7d0e8",
                        highlightcolor=C_ACENTO, insertbackground=C_TEXTO)

    def _crear_celda_resultado(self, padre):
        return tk.Label(padre, width=7, font=(FUENTE, 14, "bold"),
                        bg=C_CELDA_RES, fg=C_VERDE_H, relief="flat",
                        highlightthickness=2, highlightbackground="#b9e2c7")

    # ---------------- acciones ----------------
    def crear_matriz(self):
        dims = self._leer_dimensiones()
        if dims is None:
            return
        filas, columnas = dims
        self.entradas = armar_matriz(self.marco_orig, filas, columnas,
                                     self._crear_entrada, C_TARJETA, C_ACENTO)
        self._resultado_vacio()
        self.entradas[0][0].focus_set()

    def cargar_ejemplo(self):
        self.var_tam.set("3 × 3")
        self.crear_matriz()
        ejemplo = [[2, 0, 1], [-1, 3, 4], [5, 7, -2]]
        for i in range(3):
            for j in range(3):
                self.entradas[i][j].insert(0, str(ejemplo[i][j]))
        self.calcular()

    def calcular(self):
        if not self.entradas:
            return

        matriz = []
        for i, fila in enumerate(self.entradas):
            valores = []
            for j, caja in enumerate(fila):
                texto = caja.get().replace(" ", "").replace(",", ".")
                if texto == "":
                    messagebox.showwarning(
                        "Falta un dato",
                        f"Llena la casilla de la fila {i + 1}, columna {j + 1}.")
                    caja.focus_set()
                    return
                try:
                    Fraction(texto)  # valida enteros, decimales y fracciones
                except ZeroDivisionError:
                    messagebox.showerror(
                        "Dato inválido",
                        f"El denominador no puede ser 0 "
                        f"(fila {i + 1}, columna {j + 1}).")
                    caja.focus_set()
                    return
                except ValueError:
                    messagebox.showerror(
                        "Dato inválido",
                        f"'{texto}' no es válido. Usa enteros, decimales o "
                        f"fracciones como 1/2 o -1/2 "
                        f"(fila {i + 1}, columna {j + 1}).")
                    caja.focus_set()
                    return
                valores.append(texto)
            matriz.append(valores)

        resultado = transponer(matriz)
        filas_o, cols_o = len(matriz), len(matriz[0])

        celdas = armar_matriz(self.marco_res, len(resultado), len(resultado[0]),
                              self._crear_celda_resultado, C_TARJETA, C_VERDE)
        for i, fila in enumerate(resultado):
            for j, valor in enumerate(fila):
                celdas[i][j].config(text=valor)

        self.lbl_info.config(
            text=f"Original {filas_o}×{cols_o}   →   Transpuesta {cols_o}×{filas_o}")

        lineas = []
        for i, fila in enumerate(matriz):
            numeros = ", ".join(fila)
            lineas.append(f"Fila {i + 1} de A  [{numeros}]   →   Columna {i + 1} de Aᵀ")
        self._escribir_pasos("\n".join(lineas))

    def limpiar(self):
        for fila in self.entradas:
            for caja in fila:
                caja.delete(0, tk.END)
        self._resultado_vacio()
        if self.entradas:
            self.entradas[0][0].focus_set()


if __name__ == "__main__":
    App().mainloop()
