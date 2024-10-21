import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import re

def main():
    root = tk.Tk()
    root.title("Historia")
    root.geometry("1365x768")
    root.configure(bg="#ff7700")
    
    texto_largo = """La Liga nace en 2018 con el objetivo de desarrollar el handball en la región.
    A partir de noviembre de 2023, se convierte en la Asociación Liga Recreativa Handball Punilla por resolución 489 C/23.
    Actualmente, cuenta con más de 200 jugadores en la categoría mayores y más de 50 niños en las categorías formativas, 
    abarcando edades de 7 a 50 años, quienes disfrutan de este espacio de recreación y deporte cada 15 días. 
    Las competencias anuales incluyen 9 jornadas en la categoría mayores, con sedes alternas en las distintas localidades participantes. 
    En las categorías formativas se realiza un encuentro mensual, también en diferentes localidades. 
    La asociación cuenta con más de 12 equipos en la categoría mayores y más de 5 equipos en las categorías formativas, 
    que disfrutan de este espacio cada fin de semana. Detrás de esta organización hay una comisión 
    y colaboradores dedicados a gestionar las necesidades de los jugadores y las instituciones que representan."""

    # Crear el Label con el texto largo y usar wraplength para ajustar el ancho del texto
    
    
    label = tk.Label(root, text="HISTORIA", font=("Calibri", 24,"bold"), bg="#ff7700")
    label.pack(pady=(20, 10))
    label = tk.Label(root, text=texto_largo, wraplength=1000,font=("Calibri", 20), justify="center",bg="#d3d3d3")
    label.pack(padx=10, pady=10)
    
    def Volver_menu():
        root.destroy()
        import Menu
    
    boton1 = tk.Button (root, text="Volver", font=("Calibri",24),bg="white", command=Volver_menu)
    boton1.pack(pady=(30, 20))
    root.mainloop()

if __name__ == "__main__":
    main()