

import tkinter as tk
from tkinter import messagebox

def main(menu_principal=None):
    root = tk.Tk()
    root.title("Historia")
    root.configure(bg="#ff7700")

    # Maximizar la ventana sin pantalla completa
    root.state('zoomed')
    
    # Deshabilitar redimensionar la ventana
    root.resizable(False, False)
    
    texto_largo = """La Liga nace en 2018 con el objetivo de desarrollar el handball en la región.
    A partir de noviembre de 2023, se convierte en la Asociación Liga Recreativa Handball Punilla por resolución 489 C/23.
    Actualmente, cuenta con más de 200 jugadores en la categoría mayores y más de 50 niños en las categorías formativas, 
    abarcando edades de 7 a 50 años, quienes disfrutan de este espacio de recreación y deporte cada 15 días. 
    Las competencias anuales incluyen 9 jornadas en la categoría mayores, con sedes alternas en las distintas localidades participantes. 
    En las categorías formativas se realiza un encuentro mensual, también en diferentes localidades. 
    La asociación cuenta con más de 12 equipos en la categoría mayores y más de 5 equipos en las categorías formativas, 
    que disfrutan de este espacio cada fin de semana. Detrás de esta organización hay una comisión 
    y colaboradores dedicados a gestionar las necesidades de los jugadores y las instituciones que representan."""

    label_titulo = tk.Label(root, text="HISTORIA", font=("Calibri", 24, "bold"), bg="#ff7700")
    label_titulo.pack(pady=(20, 10))

    # Ajustar el tamaño del widget Text para que no sea demasiado grande
    text_widget = tk.Text(root, wrap="word", font=("Calibri", 20), bg="#d3d3d3", padx=10, pady=10, relief="flat", width=100, height=15)
    text_widget.insert(tk.END, texto_largo)
    text_widget.config(state=tk.DISABLED)  # Hacer que el texto no sea editable
    text_widget.pack(padx=10, pady=10)

    def Volver_menu():
        root.destroy()  # Cierra la ventana actual de "Historia"
        if menu_principal:
            menu_principal.deiconify()  # Muestra la ventana del menú principal si está disponible

    # Mantener visible el botón Volver
    boton_volver = tk.Button(root, text="Volver", font=("Calibri", 24), bg="white", command=Volver_menu)
    boton_volver.pack(pady=(30, 20))

    root.mainloop()

if __name__ == "__main__":
    main()

