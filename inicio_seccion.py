import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class Login:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("400x700+100+50")
        self.ventana.title("Liga Handball")
        fondo = "#ff7700"
        
        # ------------------------------------
        # -------------- FRAMES --------------
        # ------------------------------------
        
        self.frame_superior = Frame(self.ventana, bg=fondo)
        self.frame_superior.pack(fill="both", expand=True)
        
        self.frame_inferior = Frame(self.ventana, bg=fondo)
        self.frame_inferior.pack(fill="both", expand=True)
        
        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)
        
        # ------------------------------------
        # -------------- TITULO --------------
        # ------------------------------------
        
        self.titulo = Label(self.frame_superior, text="Liga Recreativa de Handball", font=("Arial", 14, "bold"), bg=fondo)
        self.titulo.pack(side="top", pady=20)
        
        # ------------------------------------
        # -------------- IMAGEN --------------
        # ------------------------------------
        
        self.img = Image.open("logo.png").resize((165, 165))
        self.render = ImageTk.PhotoImage(self.img)  # Guardamos la referencia en self.render
        self.fondo = Label(self.frame_superior, image=self.render, bg=fondo)
        self.fondo.pack(expand=True, fill="both", side="top")
        
        # ------------------------------------
        # -------------- DATOS ---------------
        # ------------------------------------
        
        self.label_usuario = Label(self.frame_inferior, text="Usuario:", font=("Arial", 18, "bold"), bg=fondo, fg="Black")
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e")
        
        self.entry_usuario = Entry(self.frame_inferior, bd=0, width=14, font=("Arial", 18))
        self.entry_usuario.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")
        
        self.label_contraseña = Label(self.frame_inferior, text="Contraseña:", font=("Arial", 18, "bold"), bg=fondo, fg="Black")
        self.label_contraseña.grid(row=1, column=0, pady=10, sticky="e")
        
        self.entry_contraseña = Entry(self.frame_inferior, bd=0, width=14, font=("Arial", 18, "bold"), show="*")
        self.entry_contraseña.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")
        
        self.boton_ingresar = Button(self.frame_inferior, text="Ingresar", width=16, font=("Arial", 14, "bold"), cursor="hand2", command=self.entrar)
        self.boton_ingresar.grid(row=2, column=0, columnspan=2, pady=35)
        
        mainloop()

    def entrar(self):
        nombre = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
    
        if nombre == "Tomas" and contraseña == "1234":
            self.ventana.destroy()  
            import Menu
            Menu.main()  # Llamamos a la función para abrir el menú

    """def abrir_menu(self):
        try:
            import Menu  # Importamos Menu aquí para evitar conflictos iniciales
            Menu.Menu()  # Llamamos a la clase Menu del archivo Menu.py
        except Exception as e:
            print(f"Error al abrir el menú: {e}")"""

# Ejecutar la ventana de inicio de sesión
Login()
