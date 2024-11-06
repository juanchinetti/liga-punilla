import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def obtener_autoridades(filtro_puesto=None):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tomilola23.",  # Asegúrate de tener la contraseña correcta
            database="LigaHandball"
        )
        cursor = conn.cursor()
        if filtro_puesto and filtro_puesto != "Todos":
            cursor.execute("""
                SELECT A.nombre, A.apellido, P.nombre AS puesto
                FROM Autoridades A
                JOIN Puestos P ON A.puesto_id = P.id
                WHERE P.nombre = %s
            """, (filtro_puesto,))
        else:
            cursor.execute("""
                SELECT A.nombre, A.apellido, P.nombre AS puesto
                FROM Autoridades A
                JOIN Puestos P ON A.puesto_id = P.id
            """)
        autoridades_bd = cursor.fetchall()
        return autoridades_bd
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de autoridades: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def obtener_puestos():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tomilola23.",  # Asegúrate de tener la contraseña correcta
            database="LigaHandball"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM Puestos")
        puestos = [puesto[0] for puesto in cursor.fetchall()]
        return puestos
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de puestos: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def abrir_ventana_modificar(autoridad):
    ventana_modificar = tk.Toplevel(root)
    ventana_modificar.title("Modificar Autoridad")
    ventana_modificar.geometry("400x300")

    nombre_actual = autoridad[0]
    apellido_actual = autoridad[1]
    puesto_actual = autoridad[2]

    tk.Label(ventana_modificar, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana_modificar)
    entry_nombre.pack(pady=5)
    entry_nombre.insert(0, nombre_actual)

    tk.Label(ventana_modificar, text="Apellido:").pack(pady=5)
    entry_apellido = tk.Entry(ventana_modificar)
    entry_apellido.pack(pady=5)
    entry_apellido.insert(0, apellido_actual)

    tk.Label(ventana_modificar, text="Puesto:").pack(pady=5)
    combo_puesto = ttk.Combobox(ventana_modificar, values=obtener_puestos(), state="readonly")
    combo_puesto.pack(pady=5)
    combo_puesto.set(puesto_actual)

    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nuevo_apellido = entry_apellido.get()
        nuevo_puesto = combo_puesto.get()

        if nuevo_nombre and nuevo_apellido and nuevo_puesto:
            conn = None
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="tomilola23.",  # Asegúrate de tener la contraseña correcta
                    database="LigaHandball"
                )
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Autoridades A
                    JOIN Puestos P ON A.puesto_id = P.id
                    SET A.nombre = %s, A.apellido = %s, A.puesto_id = P.id
                    WHERE A.nombre = %s AND A.apellido = %s
                """, (nuevo_nombre, nuevo_apellido, nombre_actual, apellido_actual))
                conn.commit()
                actualizar_treeview()
                messagebox.showinfo("Éxito", "Los datos de la autoridad han sido modificados con éxito.")
                ventana_modificar.destroy()  # Cierra solo la ventana de modificación
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo modificar la autoridad: {e}")
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    tk.Button(ventana_modificar, text="Guardar cambios", command=guardar_cambios).pack(pady=20)

def borrar_autoridad():
    selected_index = arbol.selection()
    if selected_index:
        autoridad_actual = arbol.item(selected_index[0])['values']
        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de eliminar esta autoridad?")
        if respuesta:
            conn = None
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="tomilola23.",
                    database="LigaHandball"
                )
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM Autoridades 
                    WHERE nombre = %s AND apellido = %s
                """, (autoridad_actual[0], autoridad_actual[1]))
                conn.commit()
                actualizar_treeview()
                messagebox.showinfo("Éxito", "La autoridad ha sido eliminada con éxito.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar la autoridad: {e}")
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
    else:
        messagebox.showwarning("Advertencia", "Selecciona una autoridad para eliminar.")

def agregar_autoridad():
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Autoridad")
    ventana_agregar.geometry("400x300")

    tk.Label(ventana_agregar, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.pack(pady=5)

    tk.Label(ventana_agregar, text="Apellido:").pack(pady=5)
    entry_apellido = tk.Entry(ventana_agregar)
    entry_apellido.pack(pady=5)

    tk.Label(ventana_agregar, text="Puesto:").pack(pady=5)
    combo_puesto = ttk.Combobox(ventana_agregar, values=obtener_puestos(), state="readonly")
    combo_puesto.pack(pady=5)

    def guardar_nueva_autoridad():
        nuevo_nombre = entry_nombre.get()
        nuevo_apellido = entry_apellido.get()
        nuevo_puesto = combo_puesto.get()
        if nuevo_nombre and nuevo_apellido and nuevo_puesto:
            conn = None
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="tomilola23.",
                    database="LigaHandball"
                )
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Autoridades (nombre, apellido, puesto_id) 
                    VALUES (%s, %s, (SELECT id FROM Puestos WHERE nombre = %s))
                """, (nuevo_nombre, nuevo_apellido, nuevo_puesto))
                conn.commit()
                actualizar_treeview()
                messagebox.showinfo("Éxito", "La nueva autoridad ha sido agregada con éxito.")
                ventana_agregar.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo agregar la autoridad: {e}")
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    tk.Button(ventana_agregar, text="Guardar", command=guardar_nueva_autoridad).pack(pady=20)
def modificar_autoridad():
    selected_index = arbol.selection()
    if selected_index:
        autoridad_actual = arbol.item(selected_index[0])['values']
        abrir_ventana_modificar(autoridad_actual)
    else:
        messagebox.showwarning("Advertencia", "Selecciona una autoridad para modificar.")

def actualizar_treeview():
    for item in arbol.get_children():
        arbol.delete(item)
    filtro_puesto = slider_filtro.get()
    autoridades_bd = obtener_autoridades(filtro_puesto if filtro_puesto and filtro_puesto != "Todos" else None)
    for autoridad in autoridades_bd:
        arbol.insert("", "end", values=(autoridad[0], autoridad[1], autoridad[2]))  # Insertar nombre, apellido y puesto

def crear_ventana(padre):
    global root  # Hacer root global para ser accesible en abrir_ventana_modificar
    root = tk.Toplevel(padre)
    root.title("Lista de Autoridades")
    root.state('zoomed')
    root.resizable(False, False)
    root.configure(bg="#ff7700")

    label = tk.Label(root, text="Autoridades Registradas", font=("Calibri", 24), bg="#ff7700")
    label.pack(pady=(20, 10))

    frame_filtro = tk.Frame(root, bg="#ff7700")
    frame_filtro.pack(pady=(10, 0))

    tk.Label(frame_filtro, text="Filtrar por puesto:", font=("Calibri", 18), bg="#ff7700").pack(side=tk.LEFT, padx=10)

    puestos = obtener_puestos()
    puestos.insert(0, "Todos")

    global slider_filtro
    slider_filtro = ttk.Combobox(frame_filtro, values=puestos, state="readonly", font=("Calibri", 18))
    slider_filtro.current(0)
    slider_filtro.pack(side=tk.LEFT)

    button_filtrar = tk.Button(frame_filtro, text="Aplicar Filtro", font=("Calibri", 18), bg="#d3d3d3", command=actualizar_treeview)
    button_filtrar.pack(side=tk.LEFT, padx=10)

    global arbol
    arbol = ttk.Treeview(root, columns=("nombre", "apellido", "puesto"), show="headings")
    arbol.pack(pady=(10, 20), expand=True, fill='both')

    arbol.heading("nombre", text="Nombre")
    arbol.heading("apellido", text="Apellido")
    arbol.heading("puesto", text="Puesto")
    arbol.column("nombre", anchor='center', width=200)
    arbol.column("apellido", anchor='center', width=200)
    arbol.column("puesto", anchor='center', width=150)

    actualizar_treeview()
    
    def volver_menu():
        root.destroy()  
        padre.deiconify()
    
    
    
    button_frame = tk.Frame(root, bg="#ff7700")
    button_frame.pack(pady=(20, 20))

    boton_volver = tk.Button(root, text="Volver", font=("Calibri", 24), bg="white", command=volver_menu)
    boton_volver.pack(pady=(30, 20))

    button_modificar = tk.Button(button_frame, text="Modificar", font=("Calibri", 24), bg="#d3d3d3", command=modificar_autoridad)
    button_modificar.pack(side=tk.LEFT, padx=(0, 20))

    button_borrar = tk.Button(button_frame, text="Borrar", font=("Calibri", 24), bg="#d3d3d3", command=borrar_autoridad)
    button_borrar.pack(side=tk.LEFT, padx=(20, 20))

    button_agregar = tk.Button(button_frame, text="Agregar", font=("Calibri", 24), bg="#d3d3d3", command=agregar_autoridad)
    button_agregar.pack(side=tk.LEFT, padx=(20, 0))