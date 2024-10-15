from tkinter import *
from tkinter import ttk
import mysql.connector
from ConexionBD import *

class LISTADO(Frame):
    def __init__(self, master=None, menu=None):
        super().__init__(master, bg="#ff7700", width=1366, height=768)
        self.master = master
        self.menu_principal = menu
        self.pack_propagate(False)
        self.pack(expand=True)

        # Obtener todos los jugadores
        self.jugadores = []
        self.actualizar_jugadores()

        self.variable = IntVar(value=0)  
        self.interfaz()

    def actualizar_jugadores(self):
        mycursor.execute("SELECT j.id, j.nombre, j.apellido, j.dni, j.correo_electronico, j.fecha_nacimiento, g.descripcion AS genero, l.nombre AS localidad, c.nombre AS club FROM Jugadores j JOIN Generos g ON j.genero_id = g.id JOIN Localidades l ON j.localidad_id = l.id LEFT JOIN Clubes c ON j.club_id = c.id")
        self.jugadores = mycursor.fetchall()

    def actualizar_treeview(self):
        arbol = self.arbol
        for item in arbol.get_children():
            arbol.delete(item)

        for jugador in self.jugadores:
            arbol.insert("", "end", values=(jugador[1], jugador[2], jugador[3], jugador[4], jugador[5], jugador[6], jugador[7], jugador[8]))

    def interfaz(self):
        # Frame principal
        frame = LabelFrame(self, text="Listado de Jugadores", bg="#ff7700", font=('Calibri', 20), borderwidth=5)
        frame.grid(row=0, column=0, padx=5, pady=50)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Etiqueta "Jugadores Registrados"
        lbl_jugadores_registrados = Label(self, text="Jugadores Registrados", bg="#ff7700", font=('Calibri', 25))
        lbl_jugadores_registrados.grid(row=1, column=0, padx=10, pady=10)

        # Treeview
        self.arbol = ttk.Treeview(self, columns=("nombre", "apellido", "dni", "correo", "fecha_nacimiento", "genero", "localidad", "club"), show="headings")
        self.arbol.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Botones debajo de la grilla
        btn_volver = Button(self, text="Volver", borderwidth=2, bg="grey", font=('Calibri', 15), command=self.volver_menu)
        btn_volver.grid(row=3, column=0, padx=10, pady=10)

        btn_modificar = Button(self, text="Modificar", borderwidth=2, bg="grey", font=('Calibri', 15), command=self.modificar_jugador)
        btn_modificar.grid(row=4, column=0, padx=10, pady=10)

        stilo = ttk.Style()
        stilo.configure("Treeview", font=("Robot", 10), rowheight=25)
        stilo.configure("Treeview.Heading", font=("Robot", 13))

        # Definir encabezados
        self.arbol.heading("nombre", text="Nombre")
        self.arbol.heading("apellido", text="Apellido")
        self.arbol.heading("dni", text="DNI")
        self.arbol.heading("correo", text="Correo")
        self.arbol.heading("fecha_nacimiento", text="Fecha de Nacimiento")
        self.arbol.heading("genero", text="Género")
        self.arbol.heading("localidad", text="Localidad")
        self.arbol.heading("club", text="Club")

        # Ancho de las columnas y datos centrados
        self.arbol.column("nombre", anchor='center', width=100)
        self.arbol.column("apellido", anchor='center', width=100)
        self.arbol.column("dni", anchor='center', width=100)
        self.arbol.column("correo", anchor='center', width=150)
        self.arbol.column("fecha_nacimiento", anchor='center', width=150)
        self.arbol.column("genero", anchor='center', width=100)
        self.arbol.column("localidad", anchor='center', width=100)
        self.arbol.column("club", anchor='center', width=100)

        # Carga los datos iniciales
        self.actualizar_treeview()

    def volver_menu(self):
        self.master.destroy()  # Cierra la ventana actual
        import Menu  # Importa tu módulo de menú principal (sin .py)

    def modificar_jugador(self):
        # Aquí deberías implementar la lógica para modificar un jugador
        print("Modificar jugador")  # Placeholder para la función

# Ejemplo de uso
if __name__ == "__main__":
    ventana = Tk()
    ventana.wm_title("Listado de Jugadores")
    ventana.wm_resizable(False, False)
    entrada = LISTADO(ventana)
    entrada.mainloop()
