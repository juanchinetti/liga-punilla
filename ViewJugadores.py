import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk


jugadores = {
    "Club A": ["Jugador 1A", "Jugador 2A", "Jugador 3A"],
    "Club B": ["Jugador 1B", "Jugador 2B"],
    "Club C": ["Jugador 1C", "Jugador 2C", "Jugador 3C", "Jugador 4C"],
}


def modificar_jugador():
    selected_jugador_index = listbox.curselection()
    selected_club = club_var.get()
    
    if selected_jugador_index:
        jugador_actual = jugadores[selected_club][selected_jugador_index[0]]
        nuevo_nombre = simpledialog.askstring("Modificar Jugador", "Ingrese el nuevo nombre del jugador:", initialvalue=jugador_actual)
        if nuevo_nombre:
            jugadores[selected_club][selected_jugador_index[0]] = nuevo_nombre
            actualizar_lista()


def volver_menu():
    root.destroy()
    #import Menu


def actualizar_lista():
    listbox.delete(0, tk.END)
    club_seleccionado = club_var.get()
    
    if club_seleccionado == "Todos":
        for club in jugadores:
            for jugador in sorted(jugadores[club]):  
                listbox.insert(tk.END, jugador)
    else:
        for jugador in sorted(jugadores[club_seleccionado]):  
            listbox.insert(tk.END, jugador)


root = tk.Tk()
root.title("Lista de Jugadores")
root.geometry("650x600") 
root.configure(bg="#ff7700")
root.resizable(False, False)

label = tk.Label(root, text="Jugadores Registrados", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))


club_var = tk.StringVar(value="Todos")


club_menu = tk.OptionMenu(root, club_var, "Todos", *jugadores.keys(), command=lambda x: actualizar_lista())
club_menu.config(font=("Calibri", 18), bg="#d3d3d3")
club_menu.pack(pady=(10, 20))

listbox = tk.Listbox(root, font=("Calibri", 18), width=30, height=10)
listbox.pack(pady=(10, 20))


actualizar_lista()


button_frame = tk.Frame(root, bg="#ff7700")
button_frame.pack(pady=(10, 20))


button_modificar = tk.Button(button_frame, text="Modificar Jugador", font=("Calibri", 18), bg="#d3d3d3", command=modificar_jugador)
button_modificar.pack(side=tk.LEFT, padx=(0, 5))
button_volver = tk.Button(button_frame, text="Volver al Menú", font=("Calibri", 18), bg="#d3d3d3", command=volver_menu)
button_volver.pack(side=tk.LEFT, padx=(5, 0))


root.mainloop()
