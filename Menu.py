import tkinter as tk
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.title("Menú")
root.geometry("1366x768")
root.configure(bg="#ff7700")
root.resizable(False, False)

# Cargar y redimensionar la imagen
original_image = Image.open("Logo_Handball.png")
resized_image = original_image.resize((325, 325))
logo_image = ImageTk.PhotoImage(resized_image)

# Etiqueta para mostrar la imagen
logo_label = tk.Label(root, image=logo_image, bg="#ff7700")
logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

# Crear botones
button1 = tk.Button(root, text="Registrar Club", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1)
button2 = tk.Button(root, text="Ver Clubes", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1)
button3 = tk.Button(root, text="Registrar Jugador", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1)
button4 = tk.Button(root, text="Ver Jugadores", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1)
button5 = tk.Button(root, text="Salir", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=root.quit)

# Posicionar los botones en la cuadrícula
button1.grid(row=1, column=0, padx=(0, 0), pady=(0, 0))  # Botón a la izquierda, arriba
button2.grid(row=2, column=1, padx=(0, 0), pady=(0, 0))  # Botón a la izquierda, abajo
button3.grid(row=1, column=1, padx=(0, 0), pady=(0, 0))  # Botón a la derecha, arriba
button4.grid(row=2, column=0, padx=(0, 0), pady=(0, 0))  # Botón a la derecha, abajo
button5.grid(row=3, column=0, columnspan=2, pady=(10, 10))  # Botón de salir

# Ajustar el tamaño de la cuadrícula
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Ejecutar la aplicación
root.mainloop()
