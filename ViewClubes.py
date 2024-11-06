import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from RegistrarClubes import ClubesABM as RegistroClubes
from modificarclub import ClubesABM as ModificarClubes

class GestionClubesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Clubes")
        self.root.geometry("1366x768")
        self.root.configure(bg="#ff7700")
        
        # Interfaz gráfica
        self.crear_interfaz()

        # Cargar clubes al inicio
        self.actualizar_treeview()

    def obtener_clubes(self, filtro_genero=None, filtro_nombre=None):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port="3306",
                database="ligaHandball"
            )
            cursor = conn.cursor()

            query = """
            SELECT c.id, c.nombre, l.nombre AS localidad, g.descripcion AS genero
            FROM Clubes c
            JOIN Localidades l ON c.localidad_id = l.id
            JOIN Generos g ON c.genero_id = g.id
            WHERE c.activo = TRUE
            """
            params = []

            if filtro_genero and filtro_genero != "Todos":
                query += " AND g.descripcion = %s"
                params.append(filtro_genero)
            if filtro_nombre:
                query += " AND c.nombre LIKE %s"
                params.append(f"%{filtro_nombre}%")

            cursor.execute(query, params)
            clubes_bd = cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de clubes: {e}")
            return []
        finally:
            conn.close()

        return clubes_bd

    def desactivar_club(self, id_del_club):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port="3306",
                database="ligaHandball"
            )
            cursor = conn.cursor()
            sql = "UPDATE Clubes SET activo = FALSE WHERE id = %s"
            cursor.execute(sql, (id_del_club,))
            conn.commit()
            messagebox.showinfo("Éxito", "El club ha sido desactivado con éxito.")
            self.actualizar_treeview()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo desactivar el club: {e}")
        finally:
            conn.close()

    def eliminar_club(self):
        selected_club_index = self.arbol.selection()
        if selected_club_index:
            club_actual = self.arbol.item(selected_club_index[0])['values']
            id_club = club_actual[0]
            nombre_club_actual = club_actual[1]

            confirmacion = messagebox.askyesno("Confirmar Desactivación", f"¿Está seguro que desea desactivar el club '{nombre_club_actual}'?")
            if confirmacion:
                self.desactivar_club(id_club)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un club para desactivar.")

    def modificar_club(self):
        selected_club_index = self.arbol.selection()
        if selected_club_index:
            club_actual = self.arbol.item(selected_club_index[0])['values']
            id_club = club_actual[0]

            if isinstance(id_club, (int, str)):
                app = ModificarClubes(menu_root=None, club_actual=club_actual)
                app.abrir()
                
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

    def volver_menu(self):
        self.root.destroy()
        import Menu
        Menu.root = tk.Tk()
        Menu.root.mainloop()

    def nuevo_club(self):
        app = RegistroClubes(self.root)
        app.run()

    def actualizar_treeview(self):
        for item in self.arbol.get_children():
            self.arbol.delete(item)
        filtro_genero = self.combobox_genero.get()
        filtro_nombre = self.entry_buscar.get()
        clubes_bd = self.obtener_clubes(filtro_genero, filtro_nombre)
        print(clubes_bd) 

        for club in clubes_bd:
            try:
                self.arbol.insert("", "end", values=(club[0], club[1], club[2], club[3]))
            except IndexError as e:
                print(f"Error al insertar club: {club}. Detalles: {e}")

    def crear_interfaz(self):
        label = tk.Label(self.root, text="Clubes Registrados", font=("Calibri", 24), bg="#ff7700")
        label.pack(pady=(20, 10))

        self.arbol = ttk.Treeview(
            self.root, columns=("id", "nombre", "localidad", "tipo"), show="headings", style="Treeview"
        )
        self.arbol.heading("#2", text="Nombre", anchor="center")
        self.arbol.heading("#3", text="Localidad", anchor="center")
        self.arbol.heading("#4", text="Categoría", anchor="center")
        self.arbol.column("#0", width=0, stretch=tk.NO)
        self.arbol.column("#2", width=230, anchor="center")
        self.arbol.column("#3", width=230, anchor="center")
        self.arbol.column("#4", width=230, anchor="center")
        self.arbol.column("#1", width=0, stretch=tk.NO)
        self.arbol.pack(pady=(10, 20), expand=True, fill='both')

        frame_filtro = tk.Frame(self.root, bg="#ff7700")
        frame_filtro.pack(pady=(10, 0))

        tk.Label(frame_filtro, text="Filtrar por Categoria:", font=("Calibri", 18), bg="#ff7700").pack(side=tk.LEFT, padx=10)
        self.combobox_genero = ttk.Combobox(frame_filtro, values=["Todos", "Masculino", "Femenino"], state="readonly", font=("Calibri", 18))
        self.combobox_genero.current(0)
        self.combobox_genero.pack(side=tk.LEFT)

        button_filtrar = tk.Button(frame_filtro, text="Aplicar Filtro", font=("Calibri", 18), bg="#d3d3d3", command=self.actualizar_treeview)
        button_filtrar.pack(side=tk.LEFT, padx=10)

        tk.Label(frame_filtro, text="Buscar Club:", font=("Calibri", 18), bg="#ff7700").pack(side=tk.LEFT, padx=10)
        self.entry_buscar = tk.Entry(frame_filtro, font=("Calibri", 18))
        self.entry_buscar.pack(side=tk.LEFT, padx=10)

        button_buscar = tk.Button(frame_filtro, text="Buscar", font=("Calibri", 18), bg="#d3d3d3", command=self.actualizar_treeview)
        button_buscar.pack(side=tk.LEFT, padx=10)

        frame_botones = tk.Frame(self.root, bg="#ff7700")
        frame_botones.pack(pady=(20, 0))

        button_nuevo = tk.Button(frame_botones, text="Nuevo Club", font=("Calibri", 18), bg="#d3d3d3", command=self.nuevo_club)
        button_nuevo.pack(side=tk.LEFT, padx=10)

        button_modificar = tk.Button(frame_botones, text="Modificar Club", font=("Calibri", 18), bg="#d3d3d3", command=self.modificar_club)
        button_modificar.pack(side=tk.LEFT, padx=10)

        button_eliminar = tk.Button(frame_botones, text="Desactivar Club", font=("Calibri", 18), bg="#d3d3d3", command=self.eliminar_club)
        button_eliminar.pack(side=tk.LEFT, padx=10)

        button_volver = tk.Button(frame_botones, text="Volver al Menú", font=("Calibri", 18), bg="#d3d3d3", command=self.volver_menu)
        button_volver.pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionClubesApp(root)
    root.mainloop()

