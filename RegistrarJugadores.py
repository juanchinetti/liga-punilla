import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector

# Conectar a la base de datos MySQL
def conectar_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia por tu usuario
            password="",  # Cambia por tu contraseña
            database="LigaHandball"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {err}")
        return None

# Obtener datos de la tabla 'Clubes'
def obtener_clubes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM Clubes")
    clubes = cursor.fetchall()
    conn.close()
    return clubes

# Obtener datos de la tabla 'Localidades'
def obtener_localidades():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM Localidades")
    localidades = cursor.fetchall()
    conn.close()
    return localidades

# Obtener datos de la tabla 'Generos'
def obtener_generos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, descripcion FROM Generos")
    generos = cursor.fetchall()
    conn.close()
    return generos

# Función para insertar un nuevo jugador en la base de datos
def guardar_jugador():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    dni = entry_dni.get()
    correo = entry_email.get()
    fecha_nacimiento = calendar_fecha_nacimiento.get()
    genero_id = combo_genero.get()
    localidad_id = combo_localidad.get()
    club_id = combo_club.get()
    domicilio = entry_domicilio.get()

    if not nombre or not apellido or not dni or not fecha_nacimiento or not genero_id or not localidad_id or not club_id:
        messagebox.showwarning("Advertencia", "Por favor, rellena todos los campos obligatorios")
        return

    conn = conectar_db()
    if conn:
        cursor = conn.cursor()

        # Insertar el nuevo jugador
        try:
            cursor.execute(
                "INSERT INTO Jugadores (nombre, apellido, dni, correo_electronico, fecha_nacimiento, genero_id, localidad_id, club_id, domicilio, ficha_medica_activa) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nombre, apellido, dni, correo, fecha_nacimiento, genero_id, localidad_id, club_id, domicilio, 0)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Jugador guardado correctamente")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo guardar el jugador: {err}")
        finally:
            conn.close()

# Crear la interfaz
root = tk.Tk()
root.title("Registro de Jugadores")
root.geometry("400x500")

# Campos para el formulario
tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Apellido:").grid(row=1, column=0, padx=10, pady=10)
entry_apellido = tk.Entry(root)
entry_apellido.grid(row=1, column=1)

tk.Label(root, text="DNI:").grid(row=2, column=0, padx=10, pady=10)
entry_dni = tk.Entry(root)
entry_dni.grid(row=2, column=1)

tk.Label(root, text="Correo electrónico:").grid(row=3, column=0, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=3, column=1)

tk.Label(root, text="Fecha de Nacimiento:").grid(row=4, column=0, padx=10, pady=10)
calendar_fecha_nacimiento = DateEntry(root, date_pattern="yyyy-mm-dd", maxdate="today")
calendar_fecha_nacimiento.grid(row=4, column=1)

tk.Label(root, text="Género:").grid(row=5, column=0, padx=10, pady=10)
combo_genero = ttk.Combobox(root, values=[f"{g[0]} - {g[1]}" for g in obtener_generos()])
combo_genero.grid(row=5, column=1)

tk.Label(root, text="Localidad:").grid(row=6, column=0, padx=10, pady=10)
combo_localidad = ttk.Combobox(root, values=[f"{l[0]} - {l[1]}" for l in obtener_localidades()])
combo_localidad.grid(row=6, column=1)

tk.Label(root, text="Club:").grid(row=7, column=0, padx=10, pady=10)
combo_club = ttk.Combobox(root, values=[f"{c[0]} - {c[1]}" for c in obtener_clubes()])
combo_club.grid(row=7, column=1)

tk.Label(root, text="Domicilio:").grid(row=8, column=0, padx=10, pady=10)
entry_domicilio = tk.Entry(root)
entry_domicilio.grid(row=8, column=1)

# Botón para guardar
boton_guardar = tk.Button(root, text="Guardar Jugador", command=guardar_jugador)
boton_guardar.grid(row=9, column=0, columnspan=2, pady=20)

# Iniciar la interfaz
root.mainloop()
