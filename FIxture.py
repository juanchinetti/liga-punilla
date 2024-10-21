import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import mysql.connector

# Generar el fixture automáticamente
def generar_fixture():
    clubes_a = obtener_clubes("A")
    clubes_b = obtener_clubes("B")

    if len(clubes_a) < 2 or len(clubes_b) < 2:
        messagebox.showwarning("Advertencia", "Debe haber al menos 2 clubes en cada grupo para generar el fixture.")
        return

    fixture.clear()

    # Asegurar que el número de clubes sea par agregando un "descanso" si es necesario
    if len(clubes_a) % 2 != 0:
        clubes_a.append("Descanso")
    if len(clubes_b) % 2 != 0:
        clubes_b.append("Descanso")

    # Generar 18 jornadas con 4 partidos para cada grupo
    num_jornadas = 18

    for jornada in range(1, num_jornadas + 1):
        partidos_a = generar_partidos_por_grupo(clubes_a, jornada, "A")
        partidos_b = generar_partidos_por_grupo(clubes_b, jornada, "B")

        # Agregar partidos de los dos grupos y un separador
        fixture.extend(partidos_a + partidos_b)
        fixture.append(("", "", "", "", ""))  # Separador entre jornadas

    actualizar_fixture()

# Generar partidos por grupo
def generar_partidos_por_grupo(clubes, jornada, grupo):
    random.shuffle(clubes)  # Mezclar los clubes para variar los emparejamientos
    partidos = []
    usados = set()

    for i in range(0, len(clubes), 2):
        if i + 1 < len(clubes):
            club1 = clubes[i]
            club2 = clubes[i + 1]
            if "Descanso" not in (club1, club2) and club1 not in usados and club2 not in usados:
                # Asegurarse de que los clubes no jueguen más de una vez en la jornada
                partidos.append((jornada, grupo, club1, club2, "-"))  # Se guarda solo el número de jornada
                usados.update([club1, club2])

    # Asegurarse de que siempre haya 4 partidos
    while len(partidos) < 4:
        partidos.append((jornada, grupo, "Descanso", "Descanso", "-"))

    return partidos[:4]  # Retornar los primeros 4 partidos

# Función para obtener clubes por grupo (A o B)
def obtener_clubes(grupo):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM Clubes WHERE grupo = %s", (grupo,))
        clubes = [fila[0] for fila in cursor.fetchall()]
        conexion.close()
        return clubes
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudieron obtener los clubes: {err}")
        return []

# Función para actualizar la grilla con los datos del fixture
def actualizar_fixture():
    filtro_seleccionado = slider_filtro.get()
    for item in arbol.get_children():
        arbol.delete(item)
    for partido in fixture:
        if filtro_seleccionado == "Todos" or partido[1] == filtro_seleccionado:
            arbol.insert("", "end", values=partido)

# Función para guardar el fixture en la base de datos
def guardar_fixture():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Encuentros")  # Limpiar tabla antes de guardar
        for partido in fixture:
            if partido[0]:
                cursor.execute(
                    "INSERT INTO Encuentros (grupo, jornada, club1, club2, resultado) VALUES (%s, %s, %s, %s, %s)",
                    (partido[1], partido[0], partido[2], partido[3], partido[4])  # Cambiar el orden aquí
                )
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "El fixture ha sido guardado.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al guardar el fixture: {err}")

# Función para cargar el fixture desde la base de datos
def cargar_fixture():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT jornada, grupo, club1, club2, resultado FROM Encuentros")
        resultados = cursor.fetchall()
        conexion.close()
        
        # Limpiar el fixture actual
        global fixture
        fixture = []

        for jornada, grupo, club1, club2, resultado in resultados:
            fixture.append((jornada, grupo, club1, club2, resultado))
        
        actualizar_fixture()  # Actualizar la interfaz con los datos cargados
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudieron cargar los encuentros: {err}")

# Función para editar el resultado
def editar_resultado(event):
    item_id = arbol.selection()[0]
    valores = arbol.item(item_id, "values")
    nuevo_resultado = simpledialog.askstring("Editar Resultado", "Ingrese el nuevo resultado:", initialvalue=valores[4])
    if nuevo_resultado:
        arbol.item(item_id, values=(valores[0], valores[1], valores[2], valores[3], nuevo_resultado))
        index = arbol.index(item_id)
        fixture[index] = (valores[0], valores[1], valores[2], valores[3], nuevo_resultado)

# Función para volver al menú
def volver_menu():
    root.destroy()
    import Menu

# Crear la ventana principal
root = tk.Tk()
root.title("Fixture de la Liga de Handball")
root.geometry("1365x768")
root.resizable(False, False)  # Desactivar la posibilidad de redimensionar
root.configure(bg="#ff7700")
root.state("zoomed")  # Maximizar la ventana

# Título
label = tk.Label(root, text="Fixture de la Liga de Handball", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))

# Filtro con slider
frame_filtro = tk.Frame(root, bg="#ff7700")
frame_filtro.pack(pady=(10, 0))

slider_filtro = ttk.Combobox(frame_filtro, values=["Todos", "A", "B"], state="readonly", font=("Calibri", 18))
slider_filtro.current(0)
slider_filtro.pack(side=tk.LEFT)
slider_filtro.bind("<<ComboboxSelected>>", lambda e: actualizar_fixture())

# Grilla del Treeview
arbol = ttk.Treeview(root, columns=("jornada", "grupo", "club1", "club2", "resultado"), show="headings")
arbol.pack(pady=(10, 20), fill="both", expand=True)

arbol.heading("jornada", text="Jornada")
arbol.heading("grupo", text="Grupo")
arbol.heading("club1", text="Club 1")
arbol.heading("club2", text="Club 2")
arbol.heading("resultado", text="Resultado")

arbol.column("jornada", anchor='center', width=150)
arbol.column("grupo", anchor='center', width=80)
arbol.column("club1", anchor='center', width=150)
arbol.column("club2", anchor='center', width=150)
arbol.column("resultado", anchor='center', width=100)

style = ttk.Style()
style.configure("Treeview", font=("Calibri", 12), rowheight=25)
style.configure("Treeview.Heading", font=("Calibri", 14, "bold"))

arbol.bind("<Double-1>", editar_resultado)

# Botones
button_crear_fixture = tk.Button(root, text="Crear Fixture", font=("Calibri", 24), command=generar_fixture)
button_crear_fixture.pack(pady=(10, 10))

button_guardar = tk.Button(root, text="Guardar Fixture", font=("Calibri", 24), command=guardar_fixture)
button_guardar.pack(pady=(10, 10))

button_volver = tk.Button(root, text="Volver", font=("Calibri", 24), command=volver_menu)
button_volver.pack(pady=(10, 20))

fixture = []

# Llamar a la función para cargar el fixture al iniciar
cargar_fixture()

root.mainloop()