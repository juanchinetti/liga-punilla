import tkinter as tk
from tkinter import messagebox, StringVar
import mysql.connector

# Conectar a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",  # Cambia esto si usas otro host
    user="root",  # Tu usuario de MySQL
    password="",  # Tu contraseña de MySQL
    database="LigaHandball"  # La base de datos que has creado
)

# Función para obtener autoridades desde la base de datos
def cargar_autoridades():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT A.id, A.nombre, A.apellido, P.nombre AS puesto FROM Autoridades A INNER JOIN Puestos P ON A.puesto_id = P.id")
    autoridades_db = cursor.fetchall()
    cursor.close()
    return autoridades_db

# Función para agregar una nueva autoridad a la base de datos
def alta_autoridad():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    puesto = entry_puesto.get()

    if nombre and apellido and puesto:
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO Autoridades (nombre, apellido, puesto_id) VALUES (%s, %s, (SELECT id FROM Puestos WHERE nombre=%s))",
                           (nombre, apellido, puesto))
            conexion.commit()
            messagebox.showinfo("Alta", f"Autoridad '{nombre} {apellido}' agregada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al agregar autoridad: {err}")
        finally:
            cursor.close()
    else:
        messagebox.showwarning("Advertencia", "Debe completar todos los campos.")

# Función para modificar una autoridad en la base de datos
def modificar_autoridad():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    puesto = entry_puesto.get()

    cursor = conexion.cursor()
    if nombre and apellido and puesto:
        try:
            cursor.execute("UPDATE Autoridades SET nombre=%s, apellido=%s, puesto_id=(SELECT id FROM Puestos WHERE nombre=%s) WHERE id=%s",
                           (nombre, apellido, puesto, id_autoridad))
            conexion.commit()
            messagebox.showinfo("Modificación", "Autoridad modificada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al modificar autoridad: {err}")
        finally:
            cursor.close()
    else:
        messagebox.showwarning("Advertencia", "Debe completar todos los campos para modificar.")

# Función para eliminar una autoridad de la base de datos
def baja_autoridad():
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Autoridades WHERE id = %s", (id_autoridad,))
        conexion.commit()
        messagebox.showinfo("Baja", f"Autoridad eliminada correctamente.")
        cursor.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al eliminar autoridad: {err}")

# Función para buscar autoridades por puesto
def buscar_por_puesto(*args):
    puesto_seleccionado = variable_puesto.get()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT A.id, A.nombre, A.apellido, P.nombre AS puesto FROM Autoridades A INNER JOIN Puestos P ON A.puesto_id = P.id WHERE P.nombre = %s", (puesto_seleccionado,))
    autoridades_encontradas = cursor.fetchall()
    cursor.close()

# Función para volver al menú
def Volver_menu():
    ventana.destroy()
    import Menu

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Autoridades")
ventana.geometry("1365x768")
ventana.config(bg="#ff7700")

# Frame para los controles
frame_controles = tk.Frame(ventana, bg="#ff7700")
frame_controles.pack(pady=20)

# Etiquetas y entradas
tk.Label(frame_controles, text="Nombre:", bg="#ff7700").grid(row=0, column=0, padx=10, pady=5)
entry_nombre = tk.Entry(frame_controles, width=30)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_controles, text="Apellido:", bg="#ff7700").grid(row=1, column=0, padx=10, pady=5)
entry_apellido = tk.Entry(frame_controles, width=30)
entry_apellido.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_controles, text="Puesto:", bg="#ff7700").grid(row=2, column=0, padx=10, pady=5)
entry_puesto = tk.Entry(frame_controles, width=30)
entry_puesto.grid(row=2, column=1, padx=10, pady=5)

# Opción de búsqueda por puesto
tk.Label(frame_controles, text="Buscar por puesto:", bg="#ff7700").grid(row=3, column=0, padx=10, pady=5)

# Variable para el OptionMenu
puestos = ['Presidenta', 'Tesorero', 'Secretaria', 'Vocal Titular', 'Revisor de Cuenta']
variable_puesto = StringVar(frame_controles)
variable_puesto.set(puestos[0])  # Valor por defecto

# Menú desplegable para seleccionar el puesto
menu_puestos = tk.OptionMenu(frame_controles, variable_puesto, *puestos, command=buscar_por_puesto)
menu_puestos.grid(row=3, column=1, padx=10, pady=5)

# Botón para mostrar todas las autoridades
btn_mostrar_todas = tk.Button(frame_controles, text="Mostrar Todas")
btn_mostrar_todas.grid(row=3, column=2, padx=10, pady=5)

# Botones de acciones
btn_alta = tk.Button(frame_controles, text="Alta", command=alta_autoridad)
btn_alta.grid(row=4, column=0, padx=10, pady=5)

btn_modificar = tk.Button(frame_controles, text="Modificar", command=modificar_autoridad)
btn_modificar.grid(row=4, column=1, padx=10, pady=5)

btn_baja = tk.Button(frame_controles, text="Baja", command=baja_autoridad)
btn_baja.grid(row=4, column=2, padx=10, pady=5)

# Botón para volver al menú
btn_volver_menu = tk.Button(ventana, text="Volver al Menú", command=Volver_menu)
btn_volver_menu.pack(pady=10)

# Ejecutar la ventana
ventana.mainloop()

# Cerrar la conexión a la base de datos al finalizar
conexion.close()
