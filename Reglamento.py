import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os

# Ruta del archivo PDF predefinido
PDF_PREDEFINIDO = "C:/Users/Usuario/Downloads/liga-punilla-Jere/REGLAMENTO.pdf"  # Cambia esto por la ruta de tu PDF

# Archivo para guardar la ruta del PDF
ARCHIVO_RUTA_PDF = "ruta_pdf.txt"

def cargar_ruta_pdf():
    """Cargar la ruta del último PDF guardado desde un archivo."""
    if os.path.exists(ARCHIVO_RUTA_PDF):
        with open(ARCHIVO_RUTA_PDF, "r") as file:
            return file.read().strip()
    return PDF_PREDEFINIDO  # Retorna el PDF predeterminado si no existe el archivo

def guardar_ruta_pdf(ruta):
    """Guardar la ruta del PDF actual en un archivo."""
    with open(ARCHIVO_RUTA_PDF, "w") as file:
        file.write(ruta)

def abrir_pdf(archivo_pdf, ventana):
    """Abrir un archivo PDF y mostrar la primera página."""
    try:
        ventana.archivo_pdf = fitz.open(archivo_pdf)
        ventana.pagina_actual = 0
        mostrar_pagina(ventana, ventana.pagina_actual)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el PDF: {str(e)}")

def mostrar_pagina(ventana, num_pagina):
    """Mostrar la página especificada del PDF."""
    try:
        if 0 <= num_pagina < len(ventana.archivo_pdf):
            pagina = ventana.archivo_pdf.load_page(num_pagina)
            pix = pagina.get_pixmap()
            imagen = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            imagen_tk = ImageTk.PhotoImage(imagen)

            etiqueta_imagen.image = imagen_tk  # Mantener la referencia
            etiqueta_imagen.config(image=imagen_tk)  # Actualizar la imagen mostrada
            actualizar_estado_pagina(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la página: {str(e)}")

def actualizar_estado_pagina(ventana):
    """Actualizar el estado de la página actual en la etiqueta."""
    etiqueta_estado.config(text=f"Página {ventana.pagina_actual + 1} de {len(ventana.archivo_pdf)}")

def pagina_anterior(ventana):
    """Navegar a la página anterior del PDF."""
    if ventana.pagina_actual > 0:
        ventana.pagina_actual -= 1
        mostrar_pagina(ventana, ventana.pagina_actual)

def pagina_siguiente(ventana):
    """Navegar a la página siguiente del PDF."""
    if ventana.pagina_actual < len(ventana.archivo_pdf) - 1:
        ventana.pagina_actual += 1
        mostrar_pagina(ventana, ventana.pagina_actual)

def volver(ventana):
    """Cerrar la ventana actual y volver al menú."""
    ventana.destroy()
    import Menu  # Asegúrate de que el módulo Menu exista

def seleccionar_pdf(ventana):
    """Abrir un cuadro de diálogo para seleccionar un nuevo PDF."""
    nuevo_pdf = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if nuevo_pdf:
        abrir_pdf(nuevo_pdf, ventana)
        guardar_ruta_pdf(nuevo_pdf)

def guardar_pdf(ventana):
    """Abrir un cuadro de diálogo para guardar el PDF actual."""
    if ventana.archivo_pdf:
        guardar_como = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if guardar_como:
            ventana.archivo_pdf.save(guardar_como)
            messagebox.showinfo("Guardado", "PDF guardado con éxito.")
            guardar_ruta_pdf(guardar_como)

def crear_ventana_reglamento():
    """Crear una nueva ventana para mostrar el reglamento."""
    ventana_reglamento = tk.Toplevel()
    ventana_reglamento.title("Reglamento de la Liga")
    ventana_reglamento.geometry("1365x768")
    ventana_reglamento.configure(bg="#ff7700")
    
    # Crear área para mostrar el PDF
    global etiqueta_imagen, etiqueta_estado
    etiqueta_imagen = tk.Label(ventana_reglamento)
    etiqueta_imagen.pack(expand=True, fill="both")

    # Frame para los botones de navegación
    frame_botones = tk.Frame(ventana_reglamento, bg="#ff7700")
    frame_botones.pack(side="right", padx=10, pady=10, fill="y")

    # Botones de la interfaz
    tk.Button(frame_botones, text="Seleccionar PDF", command=lambda: seleccionar_pdf(ventana_reglamento)).pack(pady=5)
    tk.Button(frame_botones, text="Guardar PDF", command=lambda: guardar_pdf(ventana_reglamento)).pack(pady=5)
    tk.Button(frame_botones, text="Página Anterior", command=lambda: pagina_anterior(ventana_reglamento)).pack(pady=5)
    etiqueta_estado = tk.Label(frame_botones, text="Página 1 de 1", bg="#ff7700")
    etiqueta_estado.pack(pady=5)
    tk.Button(frame_botones, text="Página Siguiente", command=lambda: pagina_siguiente(ventana_reglamento)).pack(pady=5)
    tk.Button(frame_botones, text="Volver", command=lambda: volver(ventana_reglamento)).pack(pady=5)

    # Inicializar variables para el archivo PDF y la página actual
    ventana_reglamento.archivo_pdf = None
    ventana_reglamento.pagina_actual = 0

    # Cargar automáticamente el PDF guardado al iniciar el programa
    ruta_pdf_guardado = cargar_ruta_pdf()
    abrir_pdf(ruta_pdf_guardado, ventana_reglamento)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Visualizador de PDF")
ventana.geometry("400x200")  # Tamaño más pequeño para la ventana principal
ventana.configure(bg="#ff7700")

# Botón para abrir el reglamento
tk.Button(ventana, text="Abrir Reglamento", command=crear_ventana_reglamento).pack(pady=20)

ventana.mainloop()
