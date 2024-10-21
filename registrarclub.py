from logging import root
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector


class ClubesABM:
    def __init__(self, menu_root):
        entry_width = 25
        self.menu_root = menu_root  # Guardamos la referencia a la ventana del menú
        self.root = tk.Tk()
        self.root.title("Registro de Clubes de Handball")
        self.root.geometry("1366x765")
        self.root.resizable(False, False)
        self.root.config(bg="#FF914D")
        self.root.option_add("*Font", "Arial 16 bold")

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
        self.label_nombre = tk.Label(self.frame, text="Nombre del Club:", bg="#d3d3d3", fg="black")
        self.label_nombre.grid(column=0, row=0, padx=15, pady=15)
        self.entry_nombre = tk.Entry(self.frame, width=entry_width)  # Usar ancho consistente
        self.entry_nombre.grid(column=1, row=0, padx=15, pady=15)

        # Cambiando self.sexo a self.genero
        self.label_genero = tk.Label(self.frame, text="Categoria:", bg="#d3d3d3", fg="black")
        self.label_genero.grid(row=2, column=0, padx=10, pady=5)
        self.genero_combo = ttk.Combobox(self.frame, values=self.obtener_generos(), width=entry_width - 2, state='readonly')  # Ajustar ancho del Combobox
        self.genero_combo.grid(row=2, column=1, padx=15, pady=15)

        self.label_localidad = tk.Label(self.frame, text="Localidad:", bg="#d3d3d3", fg="black")
        self.label_localidad.grid(row=3, column=0, padx=10, pady=5)
        self.localidad_combo = ttk.Combobox(self.frame, values=self.obtener_localidades(), width=entry_width - 2, state='readonly')  # Llenar combobox desde la base de datos
        self.localidad_combo.grid(row=3, column=1, padx=15, pady=15)

        # Botón para seleccionar foto
        self.label_foto = tk.Label(self.frame, text="Foto:", bg="#d3d3d3", fg="black")
        self.label_foto.grid(column=0, row=4, padx=15, pady=15)
        self.entry_foto = tk.Entry(self.frame, width=entry_width)  # Usar ancho consistente
        self.entry_foto.config(state="disabled")
        self.entry_foto.grid(column=1, row=4, padx=15, pady=15)
        self.button_foto = tk.Button(self.frame, text="Seleccionar", command=self.seleccionar_foto)
        self.button_foto.grid(column=2, row=4, padx=15, pady=15)

        # Etiqueta para mostrar imagen
        self.label_imagen = tk.Label(self.frame)
        self.label_imagen.grid(column=3, row=4, columnspan=3, padx=15, pady=15)

        # Botones para guardar y volver (fuera del frame y con fondo gris claro)
        self.button_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_club, bg="#d3d3d3")
        self.button_guardar.place(relx=0.4, rely=0.8, anchor="center")  # Posicionarlo fuera del frame

        self.button_volver = tk.Button(self.root, text="Volver", command=self.volver_menu, bg="#d3d3d3")
        self.button_volver.place(relx=0.6, rely=0.8, anchor="center")  # Posicionarlo fuera del frame

    def seleccionar_foto(self):
        archivo = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if archivo:  # Comprobar si se seleccionó un archivo
            self.entry_foto.config(state="normal")
            self.entry_foto.delete(0, tk.END)
            self.entry_foto.insert(0, archivo)
            self.entry_foto.config(state="disabled")

            # Abrir la imagen usando Pillow
            imagen = Image.open(archivo)

            # Cambiar el tamaño de la imagen
            imagen.thumbnail((200, 200))  # Cambiar el tamaño de la imagen para mostrarla

            # Convertir a PhotoImage
            self.imagen_tk = ImageTk.PhotoImage(imagen)

            # Asignar la imagen al label
            self.label_imagen.config(image=self.imagen_tk)
            self.label_imagen.image = self.imagen_tk  # Mantener una referencia a la imagen

    def obtener_localidades(self):
        # Recuperar localidades de la base de datos
        try:
            self.cursor.execute("SELECT nombre FROM localidades")  # Cambia "nombre" por el nombre de la columna que deseas
            localidades = [row[0] for row in self.cursor.fetchall()]
            return localidades
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudieron recuperar las localidades: {e}")
            return []

    def obtener_generos(self):
        try:
            self.cursor.execute("SELECT descripcion FROM generos")  # Cambia "nombre" por el nombre de la columna que deseas
            generos = [row[0] for row in self.cursor.fetchall()]
            return generos
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudieron recuperar los géneros: {e}")
            return []

    def guardar_club(self):
        nombre = self.entry_nombre.get()
        foto = self.entry_foto.get()
        genero = self.genero_combo.get()
        localidad = self.localidad_combo.get()

        genero_id = self.obtener_id_genero(genero)
        localidad_id = self.obtener_id_localidad(localidad)

        
        # Verificar que los campos no estén vacíos
        if not nombre:
            tk.messagebox.showwarning("Advertencia", "El nombre del club no puede estar vacío.")
            return
        
        try:
            with self.conn:
                self.cursor.execute("INSERT INTO clubes (nombre,genero_id, localidad_id, logo) VALUES (%s, %s, %s, %s)", (nombre,genero_id,localidad_id, foto))
                tk.messagebox.showinfo("Éxito", "Club registrado exitosamente.")
                self.entry_nombre.delete(0, tk.END)  # Limpiar campo de nombre
                self.entry_foto.config(state="normal")
                self.entry_foto.delete(0, tk.END)  # Limpiar campo de foto
                self.entry_foto.config(state="disabled")
                self.label_imagen.config(image='')  # Limpiar imagen
        except mysql.connector.Error as e:
            print(f"Error al guardar el club: {e}")


    def obtener_id_genero(self, genero_nombre):
        self.cursor.execute("SELECT id FROM generos WHERE descripcion = %s", (genero_nombre,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def obtener_id_localidad(self, localidad_nombre):
        self.cursor.execute("SELECT id FROM localidades WHERE nombre = %s", (localidad_nombre,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def volver_menu():
     root.destroy()
    import Menu 
    def run(self):
        
        self.root.mainloop()

# Código para lanzar la aplicación
if __name__ == "__main__":
    app = ClubesABM(None)  # Puedes pasar None si no necesitas usar el menú
    app.run()