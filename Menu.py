import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesario para cargar imágenes

def abrir_view_clubes():
    root.destroy()
    import ViewClubes

def abrir_view_jugadores():
    root.destroy()
    import ViewJugadores

def abrir_fixture():
    root.destroy()
    import FIxture

def abrir_historia():
    root.destroy()
    import HIstoria

#def abrir_view_autoridades():
    #root.destroy()
    #import ViewAutoridades

def abrir_reglamento():
    root.destroy()
    import Reglamentos

def salir():
    root.quit()

# Crear la ventana principal
root = tk.Tk()
root.title("Menú Principal")
root.geometry(f"{root.winfo_screenwidth()-100}x{root.winfo_screenheight()-100}+50+50")  # Ventana maximizada pero no pantalla completa
root.resizable(False, False)  # Evitar cambiar tamaño manualmente
root.configure(bg="#ff7700")

# Cargar la imagen
try:
    imagen = Image.open("Logo_Handball.png")
    imagen = imagen.resize((300, 300), Image.LANCZOS)  # Cambiado a Image.LANCZOS
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen = tk.Label(root, image=imagen_tk, bg="#ff7700")
    label_imagen.pack(pady=(20, 10))
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

# Frame para los botones
frame_botones = tk.Frame(root, bg="#ff7700")
frame_botones.pack(pady=(10, 20))

# Botones del menú
button_ver_clubes = tk.Button(frame_botones, text="Ver Clubes", font=("Calibri", 18), bg="#d3d3d3", command=abrir_view_clubes, width=20)
button_ver_clubes.grid(row=0, column=0, padx=20, pady=10)

button_ver_jugadores = tk.Button(frame_botones, text="Ver Jugadores", font=("Calibri", 18), bg="#d3d3d3", command=abrir_view_jugadores, width=20)
button_ver_jugadores.grid(row=0, column=1, padx=20, pady=10)

button_fixture = tk.Button(frame_botones, text="Fixture", font=("Calibri", 18), bg="#d3d3d3", command=abrir_fixture, width=20)
button_fixture.grid(row=1, column=0, padx=20, pady=10)

button_historia = tk.Button(frame_botones, text="Historia", font=("Calibri", 18), bg="#d3d3d3", command=abrir_historia, width=20)
button_historia.grid(row=1, column=1, padx=20, pady=10)

#button_ver_autoridades = tk.Button(frame_botones, text="Ver Autoridades", font=("Calibri", 18), bg="#d3d3d3", command=abrir_view_autoridades, width=20)
#button_ver_autoridades.grid(row=2, column=0, padx=20, pady=10)

button_reglamento = tk.Button(frame_botones, text="Reglamento", font=("Calibri", 18), bg="#d3d3d3", command=abrir_reglamento, width=20)
button_reglamento.grid(row=2, column=1, padx=20, pady=10)

# Botón de salir
button_salir = tk.Button(frame_botones, text="Salir", font=("Calibri", 18), bg="#d3d3d3", command=salir, width=44)
button_salir.grid(row=3, column=0, columnspan=2, pady=20)

# Iniciar el bucle principal de la interfaz
root.mainloop()
