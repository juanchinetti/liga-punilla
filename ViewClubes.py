import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import mysql.connector

# Función para obtener los clubes desde la base de datos
def obtener_clubes(filtro_genero=None):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conn.cursor()
        # Modificar la consulta para obtener el nombre, la localidad y el género, y filtrar si se especifica un género
        if filtro_genero:
            cursor.execute("""
                SELECT c.nombre, l.nombre AS localidad, g.descripcion AS genero
                FROM Clubes c
                JOIN Localidades l ON c.localidad_id = l.id
                JOIN Generos g ON c.genero_id = g.id
                WHERE g.descripcion = %s
            """, (filtro_genero,))
        else:
            cursor.execute("""
                SELECT c.nombre, l.nombre AS localidad, g.descripcion AS genero
                FROM Clubes c
                JOIN Localidades l ON c.localidad_id = l.id
                JOIN Generos g ON c.genero_id = g.id
            """)
        clubes_bd = cursor.fetchall()
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
    import RegistrarClubes  # Asegúrate de que registroclubes.py está en el mismo directorio

# Función para actualizar el Treeview con los clubes
def actualizar_treeview():
    for item in arbol.get_children():
        arbol.delete(item)
    filtro_genero = combobox_genero.get()
    if filtro_genero == "Todos":
        filtro_genero = None
    clubes_bd = obtener_clubes(filtro_genero)  # Obtener clubes desde la base de datos con filtro de género
    for club in clubes_bd:
        arbol.insert("", "end", values=(club[0], club[1], club[2]))

# Crear la ventana principal
root = tk.Tk()
root.title("Lista de Clubes")
root.geometry("1366x768")  # Tamaño de la ventana
root.configure(bg="#ff7700")

# Crear un Label
label = tk.Label(root, text="Clubes Registrados", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))

# Crear un Treeview para mostrar los clubes
arbol = ttk.Treeview(root, columns=("nombre", "localidad", "genero"), show="headings")
arbol.pack(pady=(10, 20), expand=True, fill='both')

# Definir encabezados
arbol.heading("nombre", text="Nombre del Club")
arbol.heading("localidad", text="Localidad")
arbol.heading("genero", text="Género")
arbol.column("nombre", anchor='center', width=400)
arbol.column("localidad", anchor='center', width=300)
arbol.column("genero", anchor='center', width=200)

# Crear un Combobox para filtrar por género
frame_filtro = tk.Frame(root, bg="#ff7700")
frame_filtro.pack(pady=(10, 0))

tk.Label(frame_filtro, text="Filtrar por género:", font=("Calibri", 18), bg="#ff7700").pack(side=tk.LEFT, padx=10)

combobox_genero = ttk.Combobox(frame_filtro, values=["Todos", "Masculino", "Femenino"], state="readonly", font=("Calibri", 18))
combobox_genero.current(0)
combobox_genero.pack(side=tk.LEFT)

# Botón para aplicar el filtro
button_filtrar = tk.Button(frame_filtro, text="Aplicar Filtro", font=("Calibri", 18), bg="#d3d3d3", command=actualizar_treeview)
button_filtrar.pack(side=tk.LEFT, padx=10)

# Llenar el Treeview con los clubes existentes
actualizar_treeview()

# Crear un Frame para los botones
button_frame = tk.Frame(root, bg="#ff7700")
button_frame.pack(pady=(20, 20))

# Crear botones
button_volver = tk.Button(button_frame, text="Volver", font=("Calibri", 24), bg="#d3d3d3", command=volver_menu)
button_volver.pack(side=tk.LEFT, padx=(0, 20))

button_nuevo = tk.Button(button_frame, text="Nuevo", font=("Calibri", 24), bg="#d3d3d3", command=nuevo_club)
button_nuevo.pack(side=tk.LEFT, padx=(0, 20))

button_modificar = tk.Button(button_frame, text="Modificar", font=("Calibri", 24), bg="#d3d3d3", command=modificar_club)
button_modificar.pack(side=tk.LEFT)

# Ejecutar la aplicación
root.mainloop()
