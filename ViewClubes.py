
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
            database="ligaHandball"
        )
        cursor = conn.cursor()

        # Cambiamos el query a SELECT para obtener los datos de los clubes
        query = """
        SELECT c.id, c.nombre, l.nombre AS localidad, g.descripcion AS genero
        FROM Clubes c
        JOIN Localidades l ON c.localidad_id = l.id
        JOIN Generos g ON c.genero_id = g.id
        """
        params = []

        # Agregamos filtros dinámicamente según los valores de `filtro_genero` y `filtro_nombre`
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
        # Obtener los valores del club seleccionado
        club_actual = arbol.item(selected_club_index[0])['values']
        
        # Asegúrate de que el ID del club está en la primera posición
        id_club = club_actual[0]  # El ID del club ahora es el primer elemento
        
        # Asegúrate de que id_club es un valor simple, no un objeto
        if isinstance(id_club, (int, str)):
            app = ModificarClubes(menu_root=None, club_actual=club_actual)
            app.abrir()
            
            # Cuando el usuario confirme los cambios, llama a guardar_modificacion con el ID
            app.guardar_modificacion(
                id_club,
                app.entry_nombre.get().strip(),
                app.combo_localidad.get().strip(),
                app.combo_genero.get().strip()
            )
        else:
            messagebox.showerror("Error", "El ID del club no es válido.")
    else:
        messagebox.showwarning("Advertencia", "Seleccione un club para modificar.")


def eliminar_club():
    selected_club_index = arbol.selection()
    if selected_club_index:
        club_actual = arbol.item(selected_club_index[0])['values']
        nombre_club_actual = club_actual[1]

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
    import Menu
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
    print(clubes_bd) 

    for club in clubes_bd:
        try:
            arbol.insert("", "end", values=(club[0], club[1], club[2], club[3]))
        except IndexError as e:
            print(f"Error al insertar club: {club}. Detalles: {e}")

root = tk.Tk()
root.title("Lista de Clubes")
root.geometry("1366x768")
root.configure(bg="#ff7700")

label = tk.Label(root, text="Clubes Registrados", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))



arbol = ttk.Treeview(
    root, columns=("id", "nombre", "localidad", "tipo"), show="headings", style="Treeview"
)

# Define los encabezados
arbol.heading("#2", text="Nombre", anchor="center")  # Encabezado para "nombre"
arbol.heading("#3", text="Localidad", anchor="center")  # Encabezado para "localidad"
arbol.heading("#4", text="Categoría", anchor="center")  # Encabezado para "categoría"

# Configura las columnas
arbol.column("#0", width=0, stretch=tk.NO)  # Columna virtual

arbol.column("#2", width=230, anchor="center")  # nombre
arbol.column("#3", width=230, anchor="center")  # localidad
arbol.column("#4", width=230, anchor="center")  # tipo
arbol.column("#1", width=0, stretch=tk.NO)  # Ocultar columna "id" (ancho 0)

# Empaqueta el Treeview
arbol.pack(pady=(10, 20), expand=True, fill='both')





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
