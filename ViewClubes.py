import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from RegistrarClubes import ClubesABM as RegistroClubes
from modificarclub import ClubesABM as ModificarClubes

def obtener_clubes(filtro_genero=None, filtro_nombre=None):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port="3306",
            database="LigaHandball"
        )
        cursor = conn.cursor()

        query = """
            SELECT c.nombre, l.nombre AS localidad, g.descripcion AS genero
            FROM Clubes c
            JOIN Localidades l ON c.localidad_id = l.id
            JOIN Generos g ON c.genero_id = g.id
        """
        params = []

        if filtro_genero and filtro_genero != "Todos":
            query += " WHERE g.descripcion = %s"
            params.append(filtro_genero)
        if filtro_nombre:
            query += " WHERE" if 'WHERE' not in query else " AND"
            query += " c.nombre LIKE %s"
            params.append(f"%{filtro_nombre}%")

        cursor.execute(query, params)
        clubes_bd = cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de clubes: {e}")
        return []
    finally:
        conn.close()

    return clubes_bd

def modificar_club():
    selected_club_index = arbol.selection()
    if selected_club_index:
        club_actual = arbol.item(selected_club_index[0])['values']
        # Crear una nueva instancia de ClubesABM para modificar el club seleccionado
        app = ModificarClubes(menu_root=root, club_actual=club_actual)
    else:
        messagebox.showwarning("Advertencia", "Seleccione un club para modificar.")

def eliminar_club():
    selected_club_index = arbol.selection()
    if selected_club_index:
        club_actual = arbol.item(selected_club_index[0])['values']
        nombre_club_actual = club_actual[0]

        confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro que desea eliminar el club '{nombre_club_actual}'?")
        if confirmacion:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    port="3306",
                    database="LigaHandball"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Clubes WHERE nombre = %s", (nombre_club_actual,))
                conn.commit()
                actualizar_treeview()
                messagebox.showinfo("Éxito", "El club ha sido eliminado con éxito.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar el club: {e}")
            finally:
                conn.close()
    else:
        messagebox.showwarning("Advertencia", "Seleccione un club para eliminar.")

def volver_menu():
    root.destroy()
    import Menu  # Asegúrate de que este módulo esté en el mismo directorio
    Menu.root = tk.Tk()
    Menu.root.mainloop()

def nuevo_club():
    app = RegistroClubes(root)
    app.run()

def actualizar_treeview():
    for item in arbol.get_children():
        arbol.delete(item)
    filtro_genero = combobox_genero.get()
    filtro_nombre = entry_buscar.get()
    clubes_bd = obtener_clubes(filtro_genero, filtro_nombre)
    for club in clubes_bd:
        arbol.insert("", "end", values=(club[0], club[1], club[2]))

root = tk.Tk()
root.title("Lista de Clubes")
root.geometry("1366x768")
root.configure(bg="#ff7700")

label = tk.Label(root, text="Clubes Registrados", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))

arbol = ttk.Treeview(root, columns=("nombre", "localidad", "tipo"), show="headings")
arbol.pack(pady=(10, 20), expand=True, fill='both')

arbol.heading("nombre", text="Nombre del Club")
arbol.heading("localidad", text="Localidad")
arbol.heading("tipo", text="Categoría")
arbol.column("nombre", anchor='center', width=400)
arbol.column("localidad", anchor='center', width=300)
arbol.column("tipo", anchor='center', width=200)

frame_filtro = tk.Frame(root, bg="#ff7700")
frame_filtro.pack(pady=(10, 0))

tk.Label(frame_filtro, text="Filtrar por género:", font=("Calibri", 18), bg="#ff7700").pack(side=tk.LEFT, padx=10)
combobox_genero = ttk.Combobox(frame_filtro, values=["Todos", "Masculino", "Femenino"], state="readonly", font=("Calibri", 18))
combobox_genero.current(0)
combobox_genero.pack(side=tk.LEFT)

button_filtrar = tk.Button(frame_filtro, text="Aplicar Filtro", font=("Calibri", 18), bg="#d3d3d3", command=actualizar_treeview)
button_filtrar.pack(side=tk.LEFT, padx=10)

tk.Label(frame_filtro, text="Buscar Club:", font=("Calibri", 18), bg="#ff7700").pack(side=tk.LEFT, padx=10)
entry_buscar = tk.Entry(frame_filtro, font=("Calibri", 18))
entry_buscar.pack(side=tk.LEFT, padx=10)

button_buscar = tk.Button(frame_filtro, text="Buscar", font=("Calibri", 18), bg="#d3d3d3", command=actualizar_treeview)
button_buscar.pack(side=tk.LEFT, padx=10)

frame_botones = tk.Frame(root, bg="#ff7700")
frame_botones.pack(pady=(20, 0))

button_nuevo = tk.Button(frame_botones, text="Nuevo Club", font=("Calibri", 18), bg="#d3d3d3", command=nuevo_club)
button_nuevo.pack(side=tk.LEFT, padx=10)

button_modificar = tk.Button(frame_botones, text="Modificar Club", font=("Calibri", 18), bg="#d3d3d3", command=modificar_club)
button_modificar.pack(side=tk.LEFT, padx=10)

button_eliminar = tk.Button(frame_botones, text="Eliminar Club", font=("Calibri", 18), bg="#d3d3d3", command=eliminar_club)
button_eliminar.pack(side=tk.LEFT, padx=10)

button_volver = tk.Button(frame_botones, text="Volver al Menú", font=("Calibri", 18), bg="#d3d3d3", command=volver_menu)
button_volver.pack(side=tk.LEFT, padx=10)

actualizar_treeview()
root.mainloop()
