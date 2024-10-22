import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os
import subprocess

# Ruta del archivo PDF predefinido
PDF_PREDEFINIDO = "C:/Users/tomiv/OneDrive/Desktop/REGLAMENTO.pdf"  # Cambia esto por la ruta de tu PDF

# Archivo para guardar la ruta del PDF
ARCHIVO_RUTA_PDF = "ruta_pdf.txt"

def cargar_ruta_pdf():
    """Cargar la ruta del último PDF guardado desde un archivo."""
    if os.path.exists(ARCHIVO_RUTA_PDF):
        with open(ARCHIVO_RUTA_PDF, "r") as file:
            return file.read().strip()
    return PDF_PREDEFINIDO  # Si no existe el archivo, retornar el PDF predeterminado

def guardar_ruta_pdf(ruta):
    """Guardar la ruta del PDF actual en un archivo."""
    with open(ARCHIVO_RUTA_PDF, "w") as file:
        file.write(ruta)

def abrir_pdf(archivo_pdf):
    try:
        ventana.archivo_pdf = fitz.open(archivo_pdf)
        ventana.pagina_actual = 0
        mostrar_pagina(ventana.pagina_actual)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el PDF: {str(e)}")

def mostrar_pagina(num_pagina):
    try:
        if 0 <= num_pagina < len(ventana.archivo_pdf):
            pagina = ventana.archivo_pdf.load_page(num_pagina)  # Cargar la página seleccionada
            pix = pagina.get_pixmap()  # Renderizar la página como imagen
            imagen = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            imagen_tk = ImageTk.PhotoImage(imagen)

            etiqueta_imagen.config(image=imagen_tk)
            etiqueta_imagen.image = imagen_tk  # Guardar referencia para que no se borre
            actualizar_estado_pagina()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la página: {str(e)}")

def actualizar_estado_pagina():
    # Actualizar el estado de las páginas (mostrar página actual)
    etiqueta_estado.config(text=f"Página {ventana.pagina_actual + 1} de {len(ventana.archivo_pdf)}")

def pagina_anterior():
    if ventana.pagina_actual > 0:
        ventana.pagina_actual -= 1
        mostrar_pagina(ventana.pagina_actual)

def pagina_siguiente():
    if ventana.pagina_actual < len(ventana.archivo_pdf) - 1:
        ventana.pagina_actual += 1
        mostrar_pagina(ventana.pagina_actual)

def volver():
    ventana.destroy()
    import Menu

def seleccionar_pdf():
    # Abrir un cuadro de diálogo para seleccionar un nuevo PDF
    nuevo_pdf = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if nuevo_pdf:
        abrir_pdf(nuevo_pdf)  # Abrir el nuevo PDF seleccionado
        guardar_ruta_pdf(nuevo_pdf)  # Guardar la ruta del nuevo PDF

def guardar_pdf():
    # Abrir un cuadro de diálogo para guardar el PDF actual
    if ventana.archivo_pdf:
        guardar_como = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if guardar_como:
            ventana.archivo_pdf.save(guardar_como)
            messagebox.showinfo("Guardado", "PDF guardado con éxito.")
            guardar_ruta_pdf(guardar_como)  # Guardar la ruta del PDF guardado

# Crear la interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Visualizador de PDF")
ventana.geometry("1365x768")  # Ajuste del tamaño de la ventana
ventana.configure(bg="#ff7700")

# Crear un frame principal para organizar la ventana
frame_principal = tk.Frame(ventana)
frame_principal.pack(expand=True, fill="both")
frame_principal.configure(bg="#ff7700")

# Frame para el área de visualización del PDF
frame_visualizacion = tk.Frame(frame_principal)
frame_visualizacion.pack(side="left", expand=True, fill="both", padx=10, pady=10)
frame_visualizacion.configure(bg="#ff7700")
# Área para mostrar el PDF como imagen
etiqueta_imagen = tk.Label(frame_visualizacion)
etiqueta_imagen.pack(expand=True, fill="both")

# Frame para los botones de navegación, al lado del PDF
frame_botones = tk.Frame(frame_principal)
frame_botones.pack(side="right", padx=10, pady=10, fill="y")
frame_botones.configure(bg="#ff7700")

# Botón para seleccionar un nuevo PDF
boton_seleccionar = tk.Button(frame_botones, text="Seleccionar PDF", command=seleccionar_pdf)
boton_seleccionar.pack(pady=5)

# Botón para guardar el PDF actual
boton_guardar = tk.Button(frame_botones, text="Guardar PDF", command=guardar_pdf)
boton_guardar.pack(pady=5)

# Botones para navegar entre páginas
boton_anterior = tk.Button(frame_botones, text="Página Anterior", command=pagina_anterior)
boton_anterior.pack(pady=5)

etiqueta_estado = tk.Label(frame_botones, text="Página 1 de 1",bg="#ff7700")
etiqueta_estado.pack(pady=5)

boton_siguiente = tk.Button(frame_botones, text="Página Siguiente", command=pagina_siguiente)
boton_siguiente.pack(pady=5)

boton_volver = tk.Button(frame_botones, text="Volver", command=volver)
boton_volver.pack(pady=5)

# Variables para almacenar el archivo PDF y la página actual
ventana.archivo_pdf = None
ventana.pagina_actual = 0

# Cargar automáticamente el PDF guardado al iniciar el programa
ruta_pdf_guardado = cargar_ruta_pdf()
abrir_pdf(ruta_pdf_guardado)

ventana.mainloop()
