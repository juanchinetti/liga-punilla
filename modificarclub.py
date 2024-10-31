import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
class ViewClubes:
    def __init__(self, root):
        self.root = root
        self.arbol = ttk.Treeview(root)  # Aquí creamos el árbol
        self.arbol.pack()
        self.cargar_datos()  # Cargar datos inicialmente

    def cargar_datos(self):
        # Limpia el Treeview
        for i in self.arbol.get_children():
            self.arbol.delete(i)
        
        # Cargar los datos de la base de datos
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port="3306",
                database="LigaHandball"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clubes")  # Cambia esto según tu consulta
            clubs = cursor.fetchall()
            for club in clubs:
                self.arbol.insert("", "end", values=club)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo cargar los clubes: {e}")
        finally:
            conn.close()

    def modificar_club(self):
        selected_club_index = self.arbol.selection()
        if selected_club_index:
            club_actual = self.arbol.item(selected_club_index[0])['values']
            app = ClubesABM(menu_root=self.root, club_actual=club_actual, arbol=self.arbol, actualizar=self.cargar_datos)  # Pasar método de actualización
            app.abrir()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un club para modificar.")


class ClubesABM:
    def __init__(self, menu_root, club_actual=None, arbol=None, actualizar=None):
        self.menu_root = menu_root
        self.club_actual = club_actual
        self.arbol = arbol  # Almacena la referencia al árbol
        self.actualizar = actualizar  # Almacena la referencia al método de actualización

        # Configuración de la ventana
        self.root = tk.Toplevel(menu_root)  # Crea una ventana secundaria
        self.root.title("Modificar Club")
        self.root.geometry("1366x765")
        self.root.resizable(False, False)
        self.root.config(bg="#FF914D")
        self.root.option_add("*Font", "Arial 16 bold")

        # Título
        self.label_titulo = tk.Label(self.root, text="Modificar Club", bg="#FF914D", fg="black", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=(20, 10))

        # Frame para centrar contenido
        self.frame = tk.Frame(self.root, bg="#d3d3d3")
        self.frame.pack(padx=20, pady=20)

        # Etiquetas y entradas de texto
        self.label_nombre = tk.Label(self.frame, text="Nombre:", bg="#d3d3d3", fg="black")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)
        self.entry_nombre = tk.Entry(self.frame, width=25)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        # Combobox para Localidad
        self.label_localidad = tk.Label(self.frame, text="Localidad:", bg="#d3d3d3", fg="black")
        self.label_localidad.grid(row=1, column=0, padx=10, pady=10)
        self.combo_localidad = ttk.Combobox(self.frame, values=self.obtener_localidades(), width=23)
        self.combo_localidad.grid(row=1, column=1, padx=10, pady=10)

        # Combobox para Género
        self.label_genero = tk.Label(self.frame, text="Categoría:", bg="#d3d3d3", fg="black")
        self.label_genero.grid(row=2, column=0, padx=10, pady=10)
        self.combo_genero = ttk.Combobox(self.frame, values=self.obtener_generos(), width=23)
        self.combo_genero.grid(row=2, column=1, padx=10, pady=10)

        # Rellenar campos si `club_actual` está definido
        if self.club_actual:
            self.entry_nombre.insert(0, self.club_actual[1])  # Asumiendo que el nombre está en el índice 1
            self.combo_localidad.set(self.club_actual[2])  # Asumiendo que la localidad está en el índice 2
            self.combo_genero.set(self.club_actual[3])  # Asumiendo que el género está en el índice 3

        # Botón para guardar cambios
        self.button_modificar = tk.Button(self.frame, text="Guardar cambios", command=self.modificar_club, bg="#d3d3d3")
        self.button_modificar.grid(row=4, column=1, pady=(10, 10))

    def abrir(self):
        self.root.mainloop()

    def modificar_club(self):
        if self.club_actual:  # Asegura que hay un club seleccionado
            self.guardar_modificacion(
                self.club_actual[0],                    # ID del club actual
                self.entry_nombre.get().strip(),        # Nombre
                self.combo_localidad.get().strip(),     # Localidad
                self.combo_genero.get().strip()         # Género
            )
        else:
            messagebox.showwarning("Advertencia", "No hay club seleccionado para modificar.")

    def guardar_modificacion(self, id_club, nombre, localidad, genero):
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
            UPDATE Clubes 
            SET nombre = %s, 
                localidad_id = (SELECT id FROM Localidades WHERE nombre = %s), 
                genero_id = (SELECT id FROM Generos WHERE descripcion = %s) 
            WHERE id = %s
            """
            cursor.execute(query, (nombre, localidad, genero, id_club))
            conn.commit()
            messagebox.showinfo("Éxito", "Club modificado con éxito.")

            # Llama al método para actualizar el Treeview
            if self.actualizar:
                self.actualizar()  # Asegúrate de que esto esté llamando a `cargar_datos` correctamente

            self.root.destroy()  # Cierra la ventana después de modificar
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo modificar el club: {e}")
        finally:
            conn.close()

    def obtener_localidades(self):
        # Función para obtener las localidades de la base de datos
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port="3306",
                database="LigaHandball"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM Localidades")
            localidades = [row[0] for row in cursor.fetchall()]
            return localidades
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener las localidades: {e}")
            return []
        finally:
            conn.close()

    def obtener_generos(self):
        # Función para obtener los géneros de la base de datos
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port="3306",
                database="LigaHandball"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT descripcion FROM Generos")
            generos = [row[0] for row in cursor.fetchall()]
            return generos
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener los géneros: {e}")
            return []
        finally:
            conn.close()
