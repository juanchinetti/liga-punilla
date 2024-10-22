import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os
import subprocess

# Ruta del archivo PDF predefinido
PDF_PREDEFINIDO = "C:/Users/tomiv/OneDrive/Desktop/REGLAMENTO.pdf"  # Cambia esto por la ruta de tu PDF

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

def editar_pdf():
    # Abrir el archivo PDF con el editor predeterminado del sistema
    try:
        archivo_pdf_ruta = ventana.archivo_pdf.name
        if os.name == 'posix':  # Linux o Mac
            subprocess.call(('xdg-open', archivo_pdf_ruta))
        else:  # Windows
            os.startfile(archivo_pdf_ruta)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el PDF para editar: {str(e)}")

# Crear la interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Visualizador y Editor de PDF")
ventana.geometry("1365x768")  # Ajuste del tamaño de la ventana

# Crear un frame principal para organizar la ventana
frame_principal = tk.Frame(ventana)
frame_principal.pack(expand=True, fill="both")

# Frame para el área de visualización del PDF
frame_visualizacion = tk.Frame(frame_principal)
frame_visualizacion.pack(side="left", expand=True, fill="both", padx=10, pady=10)

# Área para mostrar el PDF como imagen
etiqueta_imagen = tk.Label(frame_visualizacion)
etiqueta_imagen.pack(expand=True, fill="both")

# Frame para los botones de navegación y editar, al lado del PDF
frame_botones = tk.Frame(frame_principal)
frame_botones.pack(side="right", padx=10, pady=10, fill="y")

# Botón para abrir el PDF en un editor externo
boton_editar = tk.Button(frame_botones, text="Editar PDF", command=editar_pdf)
boton_editar.pack(pady=5)

# Botones para navegar entre páginas
boton_anterior = tk.Button(frame_botones, text="Página Anterior", command=pagina_anterior)
boton_anterior.pack(pady=5)

etiqueta_estado = tk.Label(frame_botones, text="Página 1 de 1")
etiqueta_estado.pack(pady=5)

boton_siguiente = tk.Button(frame_botones, text="Página Siguiente", command=pagina_siguiente)
boton_siguiente.pack(pady=5)
boton_volver = tk.Button(frame_botones, text="volver", command=volver)
boton_volver.pack(pady=5)

# Variables para almacenar el archivo PDF y la página actual
ventana.archivo_pdf = None
ventana.pagina_actual = 0

# Cargar automáticamente el PDF predefinido al iniciar el programa
abrir_pdf(PDF_PREDEFINIDO)

ventana.mainloop()

 