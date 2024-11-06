# ventana1.py
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os

PDF_PREDEFINIDO = "C:/Users/tomiv/OneDrive/Desktop/REGLAMENTO.pdf"
ARCHIVO_RUTA_PDF = "ruta_pdf.txt"

def cargar_ruta_pdf():
    if os.path.exists(ARCHIVO_RUTA_PDF):
        with open(ARCHIVO_RUTA_PDF, "r") as file:
            return file.read().strip()
    return PDF_PREDEFINIDO

def guardar_ruta_pdf(ruta):
    with open(ARCHIVO_RUTA_PDF, "w") as file:
        file.write(ruta)

def abrir_pdf(ventana, archivo_pdf):
    try:
        ventana.archivo_pdf = fitz.open(archivo_pdf)
        ventana.pagina_actual = 0
        mostrar_pagina(ventana, ventana.pagina_actual)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el PDF: {str(e)}")

def mostrar_pagina(ventana, num_pagina):
    try:
        if 0 <= num_pagina < len(ventana.archivo_pdf):
            pagina = ventana.archivo_pdf.load_page(num_pagina)
            pix = pagina.get_pixmap()
            imagen = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            imagen_tk = ImageTk.PhotoImage(imagen)

            # Mantener la referencia a la imagen
            ventana.etiqueta_imagen.image = imagen_tk
            ventana.etiqueta_imagen.config(image=imagen_tk)
            actualizar_estado_pagina(ventana)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la página: {str(e)}")

def actualizar_estado_pagina(ventana):
    ventana.etiqueta_estado.config(text=f"Página {ventana.pagina_actual + 1} de {len(ventana.archivo_pdf)}")

def pagina_anterior(ventana):
    if ventana.pagina_actual > 0:
        ventana.pagina_actual -= 1
        mostrar_pagina(ventana, ventana.pagina_actual)

def pagina_siguiente(ventana):
    if ventana.pagina_actual < len(ventana.archivo_pdf) - 1:
        ventana.pagina_actual += 1
        mostrar_pagina(ventana, ventana.pagina_actual)

def seleccionar_pdf(ventana):
    nuevo_pdf = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if nuevo_pdf:
        abrir_pdf(ventana, nuevo_pdf)
        guardar_ruta_pdf(nuevo_pdf)

def guardar_pdf(ventana):
    if ventana.archivo_pdf:
        guardar_como = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if guardar_como:
            ventana.archivo_pdf.save(guardar_como)
            messagebox.showinfo("Guardado", "PDF guardado con éxito.")
            guardar_ruta_pdf(guardar_como)

def crear_ventana(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Visualizador de PDF")
    ventana.geometry("1365x768")
    ventana.configure(bg="#ff7700")

    frame_principal = tk.Frame(ventana)
    frame_principal.pack(expand=True, fill="both")
    frame_principal.configure(bg="#ff7700")

    frame_visualizacion = tk.Frame(frame_principal)
    frame_visualizacion.pack(side="left", expand=True, fill="both", padx=10, pady=10)
    frame_visualizacion.configure(bg="#ff7700")

    ventana.etiqueta_imagen = tk.Label(frame_visualizacion)
    ventana.etiqueta_imagen.pack(expand=True, fill="both")

    frame_botones = tk.Frame(frame_principal)
    frame_botones.pack(side="right", padx=10, pady=10, fill="y")
    frame_botones.configure(bg="#ff7700")

    boton_seleccionar = tk.Button(frame_botones, text="Seleccionar PDF", command=lambda: seleccionar_pdf(ventana))
    boton_seleccionar.pack(pady=5)

    boton_guardar = tk.Button(frame_botones, text="Guardar PDF", command=lambda: guardar_pdf(ventana))
    boton_guardar.pack(pady=5)

    boton_anterior = tk.Button(frame_botones, text="Página Anterior", command=lambda: pagina_anterior(ventana))
    boton_anterior.pack(pady=5)

    ventana.etiqueta_estado = tk.Label(frame_botones, text="Página 1 de 1", bg="#ff7700")
    ventana.etiqueta_estado.pack(pady=5)

    boton_siguiente = tk.Button(frame_botones, text="Página Siguiente", command=lambda: pagina_siguiente(ventana))
    boton_siguiente.pack(pady=5)

    # Cargar el PDF guardado al iniciar el programa
    ruta_pdf_guardado = cargar_ruta_pdf()
    abrir_pdf(ventana, ruta_pdf_guardado)

    # Función para volver al menú
    def volver_menu():
        ventana.destroy()  # Cierra la ventana actual
        padre.deiconify()  # Muestra de nuevo la ventana del menú principal

    boton_volver = tk.Button(ventana, text="Volver", font=("Calibri", 24), bg="white", command=volver_menu)
    boton_volver.pack(pady=(30, 20))




