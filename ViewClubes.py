import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import mysql.connector

# Función para obtener los clubes desde la base de datos
def obtener_clubes():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM Clubes")
        clubes_bd = [row[0] for row in cursor.fetchall()]
        conn.close()
        return clubes_bd
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de clubes: {e}")
        return []

# Función para modificar un club seleccionado
def modificar_club():
    selected_club_index = arbol.selection()
    if selected_club_index:
        club_actual = arbol.item(selected_club_index[0])['values'][0]
        nuevo_nombre = simpledialog.askstring("Modificar Club", "Ingrese el nuevo nombre del club:", initialvalue=club_actual)
        if nuevo_nombre:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="LigaHandball"
                )
                cursor = conn.cursor()
                cursor.execute("UPDATE Clubes SET nombre = %s WHERE nombre = %s", (nuevo_nombre, club_actual))
                conn.commit()
                conn.close()
                actualizar_treeview()
                messagebox.showinfo("Éxito", "El nombre del club ha sido modificado con éxito.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo modificar el club: {e}")

# Función para volver al menú principal
def volver_menu():
    root.destroy()
    import Menu  # Asegúrate de que Menu.py está en el mismo directorio

# Función para abrir el registro de nuevos clubes
def nuevo_club():
    root.destroy()
    import registroclubes  # Asegúrate de que registroclubes.py está en el mismo directorio

# Función para actualizar el Treeview con los clubes
def actualizar_treeview():
    for item in arbol.get_children():
        arbol.delete(item)
    clubes_bd = obtener_clubes()  # Obtener clubes desde la base de datos
    for club in clubes_bd:
        arbol.insert("", "end", values=(club,))

# Crear la ventana principal
root = tk.Tk()
root.title("Lista de Clubes")
root.geometry("1366x768")  # Tamaño de la ventana
root.configure(bg="#ff7700")

# Crear un Label
label = tk.Label(root, text="Clubes Registrados", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))

# Crear un Treeview para mostrar los clubes
arbol = ttk.Treeview(root, columns=("nombre",), show="headings")
arbol.pack(pady=(10, 20))

# Definir encabezados
arbol.heading("nombre", text="Nombre del Club")
arbol.column("nombre", anchor='center', width=300)

# Llenar el Treeview con los clubes existentes
actualizar_treeview()

# Crear un Frame para los botones
button_frame = tk.Frame(root, bg="#ff7700")
button_frame.pack(pady=(10, 20))

# Crear botones
button_volver = tk.Button(button_frame, text="Volver", font=("Calibri", 24), bg="#d3d3d3", command=volver_menu)
button_volver.pack(side=tk.LEFT, padx=(0, 20))

button_nuevo = tk.Button(button_frame, text="Nuevo", font=("Calibri", 24), bg="#d3d3d3", command=nuevo_club)
button_nuevo.pack(side=tk.LEFT, padx=(0, 20))

button_modificar = tk.Button(button_frame, text="Modificar", font=("Calibri", 24), bg="#d3d3d3", command=modificar_club)
button_modificar.pack(side=tk.LEFT)

# Ejecutar la aplicación
root.mainloop()
