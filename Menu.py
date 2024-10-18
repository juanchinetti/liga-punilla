import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox


root = tk.Tk()
root.title("Menú Principal")
root.geometry("1230x600")
root.configure(bg="#ff7700")
root.resizable(False, False)

logo_image = None

def crear_logo(root):
    global logo_image
    try:
        original_image = Image.open("Logo_Handball.png")
        resized_image = original_image.resize((325, 325))
        logo_image = ImageTk.PhotoImage(resized_image)
        
        logo_label = tk.Label(root, image=logo_image, bg="#ff7700")
        logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de la imagen 'Liga-Punilla.png'.")
        
        logo_label = tk.Label(root, text="Logo no disponible", font=("Calibri", 24), bg="#ff7700", fg="white")
        logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

# Llamar a la función crear_logo en lugar de crear el logo directamente
crear_logo(root)
def abrir_ver_clubes():
    root.destroy()
    import ViewClubes  
    ViewClubes.main()
def abrir_historia():
    root.destroy()
    import Historia  
    Historia.main()
def abrir_Reglamento():
    root.destroy()
    import Reglamento 
    Reglamento.main()
def abrir_Fixture():
    root.destroy()
    import FIxture 
    FIxture.main()
def abrir_jugadores():
    root.destroy()
    import ViewJugadores 
    ViewJugadores .main()

button1 = tk.Button(root, text="Historia", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_historia)
button2 = tk.Button(root, text="Ver Clubes", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_ver_clubes)
button3 = tk.Button(root, text="Fixture", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_Fixture)
button4 = tk.Button(root, text="Ver Jugadores", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1,command=abrir_jugadores)
button5 = tk.Button(root, text="Salir", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=root.destroy)
button6 = tk.Button(root, text="Reglamento", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_Reglamento)

button1.grid(row=1, column=0, padx=(0, 1), pady=(2, 2))  
button2.grid(row=2, column=0, padx=(0, 1), pady=(2, 2))  
button3.grid(row=1, column=1, padx=(1, 0), pady=(2, 2))  
button4.grid(row=2, column=1, padx=(1, 0), pady=(2, 2)) 
button5.grid(row=4, column=0, columnspan=2, pady=(10, 10))  
button6.grid(row=3, column=0, columnspan=2, pady=(10, 10))


root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


root.mainloop()