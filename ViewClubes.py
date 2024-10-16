import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import mysql.connector

# Función para obtener los clubes de la base de datos según el género seleccionado
def obtener_clubes(genero):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conexion.cursor()
        # Filtrar los clubes por género
        consulta = """
            SELECT nombre FROM Clubes 
            WHERE genero_id = (SELECT id FROM Generos WHERE descripcion = %s)
        """
        cursor.execute(consulta, (genero,))
        clubes = [fila[0] for fila in cursor.fetchall()]
        conexion.close()
        return clubes
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudieron obtener los clubes: {err}")
        return []

# Generar el fixture automáticamente
def generar_fixture():
    # Obtener el género seleccionado
    genero = combobox_genero.get()
    if genero == "Seleccione":
        messagebox.showwarning("Advertencia", "Por favor, seleccione un género para generar el fixture.")
        return

    # Obtener los clubes del género seleccionado
    clubes = obtener_clubes(genero)
    if len(clubes) < 2:
        messagebox.showwarning("Advertencia", "Debe haber al menos 2 clubes para generar el fixture.")
        return

    fixture.clear()

    # Asegurar que el número de clubes sea par agregando un "descanso" si es necesario
    if len(clubes) % 2 != 0:
        clubes.append("Descanso")

    # Determinar el grupo según el género
    grupo = "A" if genero == "Masculino" else "B"

    # Generar 18 jornadas
    num_jornadas = 18
    num_partidos_por_jornada = 4

    for jornada in range(1, num_jornadas + 1):
        partidos = []
        random.shuffle(clubes)  # Mezclar los clubes para los partidos

        # Generar los partidos para la jornada
        for i in range(0, len(clubes), 2):
            if i + 1 < len(clubes):
                club1 = clubes[i]
                club2 = clubes[i + 1]
                if "Descanso" not in (club1, club2):  # No generar partidos con "Descanso"
                    fecha = f"2024-{jornada:02d}-01"  # Ejemplo de fecha por cada jornada
                    resultado = "-"
                    partidos.append((grupo, f"Jornada {jornada} ({fecha})", club1, club2, resultado))

        # Verificar que haya 4 partidos en la jornada
        while len(partidos) < num_partidos_por_jornada:
            # Si no hay suficientes partidos, agregar partidos aleatorios (evitando duplicados)
            club1, club2 = random.sample(clubes[:-1], 2)  # No elegir "Descanso"
            if (grupo, f"Jornada {jornada} ({fecha})", club1, club2, "-") not in partidos:
                partidos.append((grupo, f"Jornada {jornada} ({fecha})", club1, club2, "-"))

        # Agregar un espacio en blanco para separar las jornadas
        fixture.extend(partidos)
        fixture.append(("", "", "", "", ""))

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
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Encuentros")  # Limpiar la tabla antes de guardar el nuevo fixture
        for partido in fixture:
            if partido[0]:  # Solo guardar partidos válidos (no las filas en blanco)
                consulta = """
                    INSERT INTO Encuentros (grupo, jornada, club1, club2, resultado)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(consulta, partido)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "El fixture ha sido guardado en la base de datos.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al guardar el fixture en la base de datos: {err}")

# Función para editar el resultado seleccionado en el Treeview
def editar_resultado(event):
    item_seleccionado = arbol.selection()
    if not item_seleccionado:
        return
    item_id = item_seleccionado[0]
    valores = arbol.item(item_id, "values")

    nuevo_resultado = simpledialog.askstring("Editar Resultado", "Ingrese el nuevo resultado:", initialvalue=valores[4])
    if nuevo_resultado:
        arbol.item(item_id, values=(valores[0], valores[1], valores[2], valores[3], nuevo_resultado))
        # Actualizar también en la lista fixture
        index = arbol.index(item_id)
        fixture[index] = (valores[0], valores[1], valores[2], valores[3], nuevo_resultado)

# Crear la ventana principal
root = tk.Tk()
root.title("Fixture de la Liga de Handball")
root.geometry("1365x768")
root.configure(bg="#ff7700")

# Crear un Label para el título
label = tk.Label(root, text="Fixture de la Liga de Handball", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))

# Crear un Treeview para mostrar el fixture
arbol = ttk.Treeview(root, columns=("grupo", "jornada", "club1", "club2", "resultado"), show="headings")
arbol.pack(pady=(10, 20), fill="both", expand=True)

# Definir encabezados
arbol.heading("grupo", text="Grupo")
arbol.heading("jornada", text="Jornada (Fecha)")
arbol.heading("club1", text="Club 1")
arbol.heading("club2", text="Club 2")
arbol.heading("resultado", text="Resultado")

# Configurar el ancho de las columnas
arbol.column("grupo", anchor='center', width=80)
arbol.column("jornada", anchor='center', width=150)
arbol.column("club1", anchor='center', width=150)
arbol.column("club2", anchor='center', width=150)
arbol.column("resultado", anchor='center', width=100)

# Estilos para el Treeview
style = ttk.Style()
style.configure("Treeview", font=("Calibri", 12), rowheight=25)
style.configure("Treeview.Heading", font=("Calibri", 14, "bold"))

# Combobox para seleccionar el género
frame_filtro = tk.Frame(root, bg="#ff7700")
frame_filtro.pack(pady=(10, 0))

tk.Label(frame_filtro, text="Género:", font=("Calibri", 18), bg="#ff7700").pack(side=tk.LEFT, padx=10)

combobox_genero = ttk.Combobox(frame_filtro, values=["Seleccione", "Masculino", "Femenino"], state="readonly", font=("Calibri", 18))
combobox_genero.current(0)
combobox_genero.pack(side=tk.LEFT)

# Botón para crear fixture
button_crear_fixture = tk.Button(root, text="Crear Fixture", font=("Calibri", 18), bg="#d3d3d3", command=generar_fixture)
button_crear_fixture.pack(pady=(10, 20))

# Botón para guardar cambios
button_guardar = tk.Button(root, text="Guardar Fixture", font=("Calibri", 18), bg="#d3d3d3", command=guardar_fixture)
button_guardar.pack()

# Conectar evento de doble clic para editar el resultado
arbol.bind("<Double-1>", editar_resultado)

# Lista global para el fixture
fixture = []

# Ejecutar la aplicación
root.mainloop()
