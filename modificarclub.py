import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import mysql.connector

class ClubesABM:
    def __init__(self, menu_root, club_actual=None):
        self.menu_root = menu_root
        self.club_actual = club_actual

        # Configuración de la ventana
        self.root = tk.Tk()
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
        self.label_genero = tk.Label(self.frame, text="Categoria:", bg="#d3d3d3", fg="black")
        self.label_genero.grid(row=2, column=0, padx=10, pady=10)
        self.combo_genero = ttk.Combobox(self.frame, values=self.obtener_generos(), width=23)
        self.combo_genero.grid(row=2, column=1, padx=10, pady=10)

        # Añadir el menú desplegable para el grupo
        self.label_grupo = tk.Label(self.frame, text="Grupo:", bg="#d3d3d3", fg="black")
        self.label_grupo.grid(row=3, column=0, padx=10, pady=10)
        self.combo_grupo = ttk.Combobox(self.frame, values=["Grupo A", "Grupo B"], width=23)
        self.combo_grupo.grid(row=3, column=1, padx=10, pady=10)

        # Si se pasó un club a modificar, completar los campos con los valores actuales
        if self.club_actual:
            self.entry_nombre.insert(0, self.club_actual[0])
            self.combo_localidad.set(self.club_actual[1])
            self.combo_genero.set(self.club_actual[2])
            self.combo_grupo.set(self.club_actual[3])

        # Botón para modificar club
        self.button_modificar = tk.Button(self.root, text="Guardar cambios", command=self.modificar_club, bg="#d3d3d3")
        self.button_modificar.pack(pady=(10, 10))

        # Iniciar el bucle de la ventana
        self.root.mainloop()

    def modificar_club(self):
        # Llamar al método para mostrar el diálogo de modificación
        self.modificar_club(
            self.entry_nombre.get().strip(),
            self.combo_localidad.get().strip(),
            self.combo_genero.get().strip()
        )

    def guardar_modificacion(self, nuevo_nombre, nueva_localidad, nuevo_genero):
        # Aquí implementa la lógica para guardar los cambios en la base de datos
        if nuevo_nombre and nueva_localidad and nuevo_genero:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    port="3306",
                    database="LigaHandball"
                )
                cursor = conn.cursor()

                # Verificar si la nueva localidad existe en la base de datos
                cursor.execute("SELECT id FROM Localidades WHERE nombre = %s", (nueva_localidad,))
                localidad_id = cursor.fetchone()

                # Verificar si el nuevo género es válido
                cursor.execute("SELECT id FROM Generos WHERE descripcion = %s", (nuevo_genero,))
                genero_id = cursor.fetchone()

                if localidad_id and genero_id:
                    cursor.execute("""UPDATE Clubes SET nombre = %s, localidad_id = %s, genero_id = %s WHERE nombre = %s""",
                                   (nuevo_nombre, localidad_id[0], genero_id[0], self.club_actual[0]))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Los datos del club han sido modificados con éxito.")
                    self.root.destroy()  # Cerrar la ventana después de guardar
                else:
                    messagebox.showerror("Error", "Datos inválidos. Verifique la localidad y el género.")

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo modificar el club: {e}")
            finally:
                conn.close()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")

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

# Ejemplo de cómo iniciar la ventana
if __name__ == "__main__":
    menu_root = None  # Cambia esto por la referencia real a tu menú principal
   
    app = ClubesABM(menu_root)