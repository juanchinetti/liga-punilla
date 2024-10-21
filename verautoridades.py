import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector


def obtener_autoridades(filtro_puesto=None):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Asegúrate de tener la contraseña correcta
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
            password="",  # Asegúrate de tener la contraseña correcta
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

def modificar_autoridad():
    selected_index = arbol.selection()
    if selected_index:
        autoridad_actual = arbol.item(selected_index[0])['values'][0]  # Tomar el nombre de la autoridad
        nuevo_nombre = simpledialog.askstring("Modificar Autoridad", "Ingrese el nuevo nombre:", initialvalue=autoridad_actual)
        if nuevo_nombre:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",  # Asegúrate de tener la contraseña correcta
                    database="LigaHandball"
                )
                cursor = conn.cursor()
                cursor.execute("UPDATE Autoridades SET nombre = %s WHERE nombre = %s", (nuevo_nombre, autoridad_actual))
                conn.commit()
                actualizar_treeview()
                messagebox.showinfo("Éxito", "Los datos de la autoridad han sido modificados con éxito.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo modificar la autoridad: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

def volver_menu():
    root.destroy()
    import Menu

def nueva_autoridad():
    root.destroy()
    import registrodeautoridades

def actualizar_treeview():
    for item in arbol.get_children():
        arbol.delete(item)
    filtro_puesto = slider_filtro.get()
    autoridades_bd = obtener_autoridades(filtro_puesto if filtro_puesto and filtro_puesto != "Todos" else None)
    for autoridad in autoridades_bd:
        arbol.insert("", "end", values=(autoridad[0], autoridad[1], autoridad[2]))  # Insertar nombre, apellido y puesto

root = tk.Tk()
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

slider_filtro = ttk.Combobox(frame_filtro, values=puestos, state="readonly", font=("Calibri", 18))
slider_filtro.current(0)
slider_filtro.pack(side=tk.LEFT)

button_filtrar = tk.Button(frame_filtro, text="Aplicar Filtro", font=("Calibri", 18), bg="#d3d3d3", command=actualizar_treeview)
button_filtrar.pack(side=tk.LEFT, padx=10)

arbol = ttk.Treeview(root, columns=("nombre", "apellido", "puesto"), show="headings")
arbol.pack(pady=(10, 20), expand=True, fill='both')

arbol.heading("nombre", text="Nombre")
arbol.heading("apellido", text="Apellido")
arbol.heading("puesto", text="Puesto")
arbol.column("nombre", anchor='center', width=200)
arbol.column("apellido", anchor='center', width=200)
arbol.column("puesto", anchor='center', width=150)

actualizar_treeview()

button_frame = tk.Frame(root, bg="#ff7700")
button_frame.pack(pady=(20, 20))

button_volver = tk.Button(button_frame, text="Volver", font=("Calibri", 24), bg="#d3d3d3", command=volver_menu)
button_volver.pack(side=tk.LEFT, padx=(0, 20))

button_nuevo = tk.Button(button_frame, text="Agregar", font=("Calibri", 24), bg="#d3d3d3", command=nueva_autoridad)
button_nuevo.pack(side=tk.LEFT, padx=(0, 20))

button_modificar = tk.Button(button_frame, text="Modificar", font=("Calibri", 24), bg="#d3d3d3", command=modificar_autoridad)
button_modificar.pack(side=tk.LEFT)

root.mainloop()