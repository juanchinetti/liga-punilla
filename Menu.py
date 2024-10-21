import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from registrarclub import ClubesABM 

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
    ViewJugadores.main()

def abrir_listajugares():
    root.destroy()
    import listadejugadres
    listadejugadres.main()

def nuevo_club():
    root.destroy()  # Cierra la ventana del menú
    app = ClubesABM(root)  # Crea una instancia de ClubesABM
    app.run()  # Inicia la nueva ventana

def abrir_registrodeautoridades():
    root.destroy()
    import registrodeautoridades
    ClubesABM.main()

def abrir_verautoridades():
    root.destroy()
    import verautoridades
    verautoridades.main()

root = tk.Tk()
root.title("Menú Principal")
root.geometry("1230x600")
root.configure(bg="#ff7700")
root.resizable(False, False)

# Cargar imagen de logo
try:
    original_image = Image.open(r"C:\Users\Usuario\Downloads\visual code\matematica\Liga de Handball Punilla\liga-punilla.png")
    resized_image = original_image.resize((250, 250))
    logo_image = ImageTk.PhotoImage(resized_image)

    # Mostrar el logo
    logo_label = tk.Label(root, image=logo_image, bg="#ff7700")
    logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

except FileNotFoundError:
    messagebox.showerror("Error", "No se encontró el archivo de la imagen 'Liga-Punilla.png'.")
    
    logo_label = tk.Label(root, text="Logo no disponible", font=("Calibri", 24), bg="#ff7700", fg="white")
    logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

# Crear botones existentes
button1 = tk.Button(root, text="Registrar Club", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=nuevo_club)
button2 = tk.Button(root, text="Ver Clubes", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_ver_clubes)
button3 = tk.Button(root, text="Registrar Jugador", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_listajugares)
button4 = tk.Button(root, text="Ver Jugadores", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_jugadores)
button10 = tk.Button(root, text="Ver Autoridades", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_verautoridades)

# Posicionar botones existentes
button1.grid(row=1, column=0, padx=(0, 1), pady=(2, 2))  
button2.grid(row=2, column=0, padx=(0, 1), pady=(2, 2))  
button3.grid(row=1, column=1, padx=(1, 0), pady=(2, 2))  
button4.grid(row=2, column=1, padx=(1, 0), pady=(2, 2)) 
button10.grid(row=4, column=0, columnspan=2, pady=(20, 20))  # Centrar "Ver Autoridades"

# Crear nuevos botones
button6 = tk.Button(root, text="Historia", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_historia)
button7 = tk.Button(root, text="Reglamento", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_Reglamento)
button8 = tk.Button(root, text="Fixture", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_Fixture)
button9 = tk.Button(root, text="R. Autoridades", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_registrodeautoridades)
button5 = tk.Button(root, text="Salir", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=root.quit)

# Posicionar nuevos botones
button6.grid(row=3, column=0, padx=(0, 1), pady=(2, 2))  
button7.grid(row=3, column=1, padx=(1, 0), pady=(2, 2))  
button8.grid(row=5, column=0, padx=(0, 1), pady=(2, 2))  
button9.grid(row=5, column=1, padx=(1, 0), pady=(2, 2)) 
button5.grid(row=6, column=0, columnspan=2, pady=(20, 20))  # "Salir" al final

# Configurar las filas y columnas
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()



#def abrir_ver_clubes():
    #root.destroy()
    #import ViewClubes  
    #ViewClubes.main()
#def abrir_historia():
    #root.destroy()
    #import Historia  
    #Historia.main()
#def abrir_Reglamento():
   # root.destroy()
    #import Reglamento 
    #Reglamento.main()
#def abrir_Fixture():
    #root.destroy()
    #import FIxture 
    #FIxture.main()
#def abrir_jugadores():
    #root.destroy()
    #import ViewJugadores 
    #ViewJugadores.main()
#crear_logo(root)


#button1 = tk.Button(root, text="Historia", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_historia)
#button2 = tk.Button(root, text="Ver Clubes", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_ver_clubes)
#button3 = tk.Button(root, text="Fixture", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_Fixture)
#button4 = tk.Button(root, text="Ver Jugadores", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1,command=abrir_jugadores)
#button5 = tk.Button(root, text="Salir", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=root.destroy)
#button6 = tk.Button(root, text="Reglamento", font=("Calibri", 24), bg="#d3d3d3", width=15, height=1, command=abrir_Reglamento)

#button1.grid(row=1, column=0, padx=(0, 1), pady=(2, 2))  
#button2.grid(row=2, column=0, padx=(0, 1), pady=(2, 2))  
#button3.grid(row=1, column=1, padx=(1, 0), pady=(2, 2))  
#button4.grid(row=2, column=1, padx=(1, 0), pady=(2, 2)) 
#button5.grid(row=4, column=0, columnspan=2, pady=(10, 10))  
#button6.grid(row=3, column=0, columnspan=2, pady=(10, 10))


#root.grid_rowconfigure(0, weight=1)
#root.grid_rowconfigure(1, weight=1)
#root.grid_rowconfigure(2, weight=1)
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=1)
