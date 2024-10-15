import tkinter as tk
from tkinter import ttk, messagebox
import random
import mysql.connector

# Conectar a la base de datos y obtener los nombres de los clubes
def obtener_clubes():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM Clubes")  # Asumiendo que la tabla se llama 'Clubes' y tiene una columna 'nombre'
        clubes = [fila[0] for fila in cursor.fetchall()]
        conexion.close()
        return clubes
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudieron obtener los clubes: {err}")
        return []

# Generar el fixture automáticamente
def generar_fixture():
    # Obtener los clubes de la base de datos
    clubes = obtener_clubes()
    if len(clubes) < 2:
        messagebox.showwarning("Advertencia", "Debe haber al menos 2 clubes para generar el fixture.")
        return

    fixture.clear()

    # Generar 18 jornadas, cada club juega 2 veces por jornada
    for jornada in range(1, 19):
        partidos = []
        random.shuffle(clubes)  # Mezclar los clubes para los partidos
        for i in range(0, len(clubes), 2):
            if i + 1 < len(clubes):
                club1 = clubes[i]
                club2 = clubes[i + 1]
                fecha = f"2024-{jornada:02d}-01"  # Ejemplo de fecha por cada jornada
                resultado = ""
                partidos.append((f"Jornada {jornada} ({fecha})", club1, club2, resultado))

        # Agregar un espacio en blanco para separar las jornadas
        fixture.extend(partidos)
        fixture.append(("", "", "", ""))

    actualizar_fixture()

# Función para actualizar la grilla con los datos del fixture
def actualizar_fixture():
    for item in arbol.get_children():
        arbol.delete(item)
    for partido in fixture:
        arbol.insert("", "end", values=partido)

# Función para guardar los partidos generados en la base de datos
def guardar_fixture():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="tu_usuario",
            password="tu_contraseña",
            database="LigaHandball"
        )
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Encuentros")  # Limpiar la tabla antes de guardar el nuevo fixture
        for partido in fixture:
            if partido[0]:  # Solo guardar partidos válidos (no las filas en blanco)
                consulta = """
                    INSERT INTO Encuentros (jornada, club1, club2, resultado)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(consulta, partido)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "El fixture ha sido guardado en la base de datos.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al guardar el fixture en la base de datos: {err}")

# Crear la ventana principal
root = tk.Tk()
root.title("Fixture de la Liga de Handball")
root.geometry("1365x768")
root.configure(bg="#ff7700")

# Crear un Label para el título
label = tk.Label(root, text="Fixture de la Liga de Handball", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))

# Crear un Treeview para mostrar el fixture
arbol = ttk.Treeview(root, columns=("jornada", "club1", "club2", "resultado"), show="headings")
arbol.pack(pady=(10, 20), fill="both", expand=True)

# Definir encabezados
arbol.heading("jornada", text="Jornada (Fecha)")
arbol.heading("club1", text="Club 1")
arbol.heading("club2", text="Club 2")
arbol.heading("resultado", text="Resultado")

# Configurar el ancho de las columnas
arbol.column("jornada", anchor='center', width=150)
arbol.column("club1", anchor='center', width=150)
arbol.column("club2", anchor='center', width=150)
arbol.column("resultado", anchor='center', width=100)

# Estilos para el Treeview
style = ttk.Style()
style.configure("Treeview", font=("Calibri", 12), rowheight=25)
style.configure("Treeview.Heading", font=("Calibri", 14, "bold"))

# Botón para crear fixture
button_crear_fixture = tk.Button(root, text="Crear Fixture", font=("Calibri", 18), bg="#d3d3d3", command=generar_fixture)
button_crear_fixture.pack(pady=(10, 20))

# Botón para guardar cambios
button_guardar = tk.Button(root, text="Guardar Fixture", font=("Calibri", 18), bg="#d3d3d3", command=guardar_fixture)
button_guardar.pack()

# Lista global para el fixture
fixture = []

# Ejecutar la aplicación
root.mainloop()
