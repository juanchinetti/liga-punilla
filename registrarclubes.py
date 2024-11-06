import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector

class ClubesABM:
    def __init__(self, menu_root):
        # Configuración de la ventana principal
        entry_width = 25
        self.root = tk.Tk()
        self.root.title("Registro de Clubes de Handball")
        self.root.geometry("1366x765")
        self.root.resizable(False, False)
        self.root.config(bg="#FF914D")
        self.root.option_add("*Font", "Arial 16 bold")

        self.label_titulo = tk.Label(self.root, text="Nuevo club", bg="#FF914D", fg="black", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=(20, 0))  # Espaciado superior

        # Conexión a la base de datos
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port="3306",
                database="ligaHandball"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            self.root.destroy()
            return

        # Frame para centrar contenido
        self.frame = tk.Frame(self.root, bg="#d3d3d3")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Etiquetas y entradas de texto
        self.crear_campos(entry_width)

        # Botones para guardar y volver
        self.button_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_club, bg="#d3d3d3")
        self.button_guardar.place(relx=0.4, rely=0.8, anchor="center")

        self.button_volver = tk.Button(self.root, text="Volver", command=self.volver_menu, bg="#d3d3d3")
        self.button_volver.place(relx=0.6, rely=0.8, anchor="center")

        self.imagen_tk = None  # Mantener la referencia de la imagen aquí

        self.root.mainloop()

    def crear_campos(self, entry_width):
        """Crea los campos de entrada en la interfaz"""
        self.label_nombre = tk.Label(self.frame, text="Nombre:", bg="#d3d3d3", fg="black")
        self.label_nombre.grid(column=0, row=0, padx=15, pady=15)
        self.entry_nombre = tk.Entry(self.frame, width=entry_width)
        self.entry_nombre.grid(column=1, row=0, padx=15, pady=15)

        self.label_genero = tk.Label(self.frame, text="Categoría:", bg="#d3d3d3", fg="black")
        self.label_genero.grid(row=2, column=0, padx=10, pady=5)
        self.genero_combo = ttk.Combobox(self.frame, values=self.obtener_generos(), width=entry_width - 2, state='readonly')
        self.genero_combo.grid(row=2, column=1, padx=15, pady=15)
        self.genero_combo.set("Seleccione una opción")

        self.label_localidad = tk.Label(self.frame, text="Localidad:", bg="#d3d3d3", fg="black")
        self.label_localidad.grid(row=3, column=0, padx=10, pady=5)
        self.localidad_combo = ttk.Combobox(self.frame, values=self.obtener_localidades(), width=entry_width - 2, state='readonly')
        self.localidad_combo.grid(row=3, column=1, padx=15, pady=15)
        self.localidad_combo.set("Seleccione una opción")

        # Selección de foto
        self.label_foto = tk.Label(self.frame, text="Foto:", bg="#d3d3d3", fg="black")
        self.label_foto.grid(column=0, row=5, padx=15, pady=15)
        self.entry_foto = tk.Entry(self.frame, width=entry_width, state="disabled")
        self.entry_foto.grid(column=1, row=5, padx=15, pady=15)
        self.button_foto = tk.Button(self.frame, text="Seleccionar", command=self.seleccionar_foto)
        self.button_foto.grid(column=2, row=5, padx=15, pady=15)

        # Etiqueta para mostrar imagen
        self.label_imagen = tk.Label(self.frame)
        self.label_imagen.grid(column=3, row=5, columnspan=3, padx=15, pady=15)

    def guardar_club(self):
        nombre = self.entry_nombre.get()
        genero = self.genero_combo.get()
        localidad = self.localidad_combo.get()

        if not nombre or genero == "Seleccione una opción" or localidad == "Seleccione una opción":
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        try:
            with open(self.entry_foto.get(), 'rb') as file:
                foto_binaria = file.read()
        except FileNotFoundError:
            messagebox.showwarning("Advertencia", "La imagen seleccionada no se encontró.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Clubes (nombre, genero_id, localidad_id, logo) VALUES (%s, (SELECT id FROM Generos WHERE descripcion = %s), (SELECT id FROM Localidades WHERE nombre = %s), %s)",
                (nombre, genero, localidad, foto_binaria)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Club guardado exitosamente.")
            self.root.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar el club: {e}")

    def obtener_generos(self):
        try:
            self.cursor.execute("SELECT descripcion FROM Generos")
            return [row[0] for row in self.cursor.fetchall()]
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener los géneros: {e}")
            return []

    def obtener_localidades(self):
        try:
            self.cursor.execute("SELECT nombre FROM Localidades")
            return [row[0] for row in self.cursor.fetchall()]
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener las localidades: {e}")
            return []

    def seleccionar_foto(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.gif")],
        )
        if file_path:
            self.entry_foto.config(state="normal")
            self.entry_foto.delete(0, tk.END)
            self.entry_foto.insert(0, file_path)
            self.entry_foto.config(state="disabled")

            img = Image.open(file_path).resize((100, 100), Image.LANCZOS)
            self.imagen_tk = ImageTk.PhotoImage(img)
            self.label_imagen.config(image=self.imagen_tk)
            self.label_imagen.image = self.imagen_tk

    def volver_menu(self):
        self.root.destroy()

# Ejecución de la aplicación
if __name__ == "__main__":
    app = ClubesABM(None)

