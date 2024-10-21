import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector


class AutoridadesABM:
    def __init__(self, menu_root):
        entry_width = 25
        self.menu_root = menu_root  # Guardamos la referencia a la ventana del menú
        self.root = tk.Tk()
        self.root.title("Registro de Autoridades de Handball")
        self.root.geometry("1366x765")
        self.root.resizable(False, False)
        self.root.config(bg="#FF914D")
        self.root.option_add("*Font", "Arial 16 bold")

        # Etiqueta para el título
        self.label_titulo = tk.Label(self.root, text="Autoridades", bg="#FF914D", fg="black", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=(20, 0))  # Espaciado superior

        # Conexión a la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port="3306",
            database="LigaHandball"
        )
        self.cursor = self.conn.cursor()

        # Frame para centrar contenido
        self.frame = tk.Frame(self.root, bg="#d3d3d3")  # Fondo gris claro en el frame
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Etiquetas y entradas de texto
        self.label_nombre = tk.Label(self.frame, text="Nombre:", bg="#d3d3d3", fg="black")
        self.label_nombre.grid(column=0, row=0, padx=15, pady=15)
        self.entry_nombre = tk.Entry(self.frame, width=entry_width)
        self.entry_nombre.grid(column=1, row=0, padx=15, pady=15)

        self.label_apellido = tk.Label(self.frame, text="Apellido:", bg="#d3d3d3", fg="black")
        self.label_apellido.grid(column=0, row=1, padx=15, pady=15)
        self.entry_apellido = tk.Entry(self.frame, width=entry_width)
        self.entry_apellido.grid(column=1, row=1, padx=15, pady=15)

        self.label_puesto = tk.Label(self.frame, text="Puesto:", bg="#d3d3d3", fg="black")
        self.label_puesto.grid(column=0, row=2, padx=15, pady=15)
        self.puesto_combo = ttk.Combobox(self.frame, values=self.obtener_puestos(), width=entry_width - 2, state='readonly')
        self.puesto_combo.grid(column=1, row=2, padx=15, pady=15)

        # Botón para seleccionar foto
        self.label_foto = tk.Label(self.frame, text="Foto:", bg="#d3d3d3", fg="black")
        self.label_foto.grid(column=0, row=3, padx=15, pady=15)
        self.entry_foto = tk.Entry(self.frame, width=entry_width)  
        self.entry_foto.config(state="disabled")
        self.entry_foto.grid(column=1, row=3, padx=15, pady=15)
        self.button_foto = tk.Button(self.frame, text="Seleccionar", command=self.seleccionar_foto)
        self.button_foto.grid(column=2, row=3, padx=15, pady=15)

        # Etiqueta para mostrar imagen
        self.label_imagen = tk.Label(self.frame)
        self.label_imagen.grid(column=3, row=3, columnspan=3, padx=15, pady=15)

        # Botones para guardar y volver
        self.button_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_autoridad, bg="#d3d3d3")
        self.button_guardar.place(relx=0.4, rely=0.8, anchor="center")

        self.button_volver = tk.Button(self.root, text="Volver", command=self.volver_menu, bg="#d3d3d3")
        self.button_volver.place(relx=0.6, rely=0.8, anchor="center")

    def seleccionar_foto(self):
        archivo = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if archivo:
            self.entry_foto.config(state="normal")
            self.entry_foto.delete(0, tk.END)
            self.entry_foto.insert(0, archivo)
            self.entry_foto.config(state="disabled")

            # Abrir la imagen usando Pillow
            imagen = Image.open(archivo)

            # Cambiar el tamaño de la imagen
            imagen.thumbnail((200, 200))

            # Convertir a PhotoImage
            self.imagen_tk = ImageTk.PhotoImage(imagen)

            # Asignar la imagen al label
            self.label_imagen.config(image=self.imagen_tk)
            self.label_imagen.image = self.imagen_tk  # Mantener una referencia a la imagen

    def obtener_puestos(self):
        try:
            self.cursor.execute("SELECT nombre FROM Puestos")  # Cambia "nombre" por el nombre de la columna que deseas
            puestos = [row[0] for row in self.cursor.fetchall()]
            return puestos
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudieron recuperar los puestos: {e}")
            return []

    def guardar_autoridad(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        puesto = self.puesto_combo.get()
        foto = self.entry_foto.get()

        puesto_id = self.obtener_id_puesto(puesto)

        # Verificar que los campos no estén vacíos
        if not nombre or not apellido or not puesto:
            tk.messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")
            return
        
        try:
            with self.conn:
                self.cursor.execute("INSERT INTO Autoridades (nombre, apellido, puesto_id, foto) VALUES (%s, %s, %s, %s)", 
                                    (nombre, apellido, puesto_id, foto))
                tk.messagebox.showinfo("Éxito", "Autoridad registrada exitosamente.")
                self.entry_nombre.delete(0, tk.END)  # Limpiar campo de nombre
                self.entry_apellido.delete(0, tk.END)  # Limpiar campo de apellido
                self.entry_foto.config(state="normal")
                self.entry_foto.delete(0, tk.END)  # Limpiar campo de foto
                self.entry_foto.config(state="disabled")
                self.label_imagen.config(image='')  # Limpiar imagen
        except mysql.connector.Error as e:
            print(f"Error al guardar la autoridad: {e}")

    def obtener_id_puesto(self, puesto_nombre):
        self.cursor.execute("SELECT id FROM Puestos WHERE nombre = %s", (puesto_nombre,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def volver_menu(self):
        self.root.destroy()
        import Menu  # Importar el módulo del menú

    def run(self):
        self.root.mainloop()

# Función main para iniciar la aplicación
def main():
    app = AutoridadesABM(None)  # Puedes pasar None si no necesitas usar el menú
    app.run()

# Código para lanzar la aplicación
if __name__ == "__main__":
    main()
