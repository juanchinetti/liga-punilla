import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import re


directorio_imagenes = r"C:\Users\Usuario\Downloads\visual code\matematica\Liga de Handball Punilla"

def cargar_imagen(label):
    archivo = filedialog.askopenfilename(initialdir=directorio_imagenes, filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
    if archivo:
        img = Image.open(archivo)
        
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img

def validar_campos():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    dni = entry_dni.get()
    domicilio = entry_domicilio.get()
    telefono = entry_telefono.get()

    if not re.match("^[A-Za-z]+$", nombre):
        messagebox.showerror("Error", "Por favor, escriba su nombre como está en el DNI")
        return False
    if not re.match("^[A-Za-z]+$", apellido):
        messagebox.showerror("Error", "Por favor, escriba su apellido como está en el DNI")
        return False
    if not re.match("^[0-9]+$", dni):
        messagebox.showerror("Error", "Por favor, solo números en el DNI")
        return False
    if not re.match("^[A-Za-z0-9 ]+$", domicilio):
        messagebox.showerror("Error", "Por favor, escriba su domicilio como está en el DNI")
        return False
    if not re.match("^[0-9]+$", telefono):
        messagebox.showerror("Error", "Por favor, escriba su teléfono como está en el DNI")
        return False

    return True

def confirmar_guardado():
    if validar_campos():
        respuesta = messagebox.askquestion("Confirmación", "¿Está seguro que desea guardar?", icon='warning')
        if respuesta == 'yes':
            messagebox.showinfo("Éxito", "Guardado exitosamente")
        else:
            messagebox.showinfo("Cancelado", "El guardado fue cancelado")

class ABMJugadoresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alta/Modificación de Jugadores")
        self.root.geometry("600x600")
        self.root.configure(bg="#ff7f00")
        self.root.resizable(False, False)

        frame = tk.Frame(self.root, bg="#ff7f00")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Nombre", bg="#ff7f00", fg="white").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        global entry_nombre
        entry_nombre = tk.Entry(frame, width=30)
        entry_nombre.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Apellido", bg="#ff7f00", fg="white").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        global entry_apellido
        entry_apellido = tk.Entry(frame, width=30)
        entry_apellido.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="D.N.I", bg="#ff7f00", fg="white").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        global entry_dni
        entry_dni = tk.Entry(frame, width=30)
        entry_dni.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Domicilio", bg="#ff7f00", fg="white").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        global entry_domicilio
        entry_domicilio = tk.Entry(frame, width=30)
        entry_domicilio.grid(row=4, column=1, pady=5)

        tk.Label(frame, text="Teléfono", bg="#ff7f00", fg="white").grid(row=5, column=0, sticky="e", padx=10, pady=5)
        global entry_telefono
        entry_telefono = tk.Entry(frame, width=30)
        entry_telefono.grid(row=5, column=1, pady=5)

        tk.Label(frame, text="Sexo", bg="#ff7f00", fg="white").grid(row=6, column=0, sticky="e", padx=10, pady=5)
        global sexo_combo
        sexo_combo = ttk.Combobox(frame, values=["Masculino", "Femenino"], width=28, state="readonly")
        sexo_combo.grid(row=6, column=1, pady=5)

        tk.Label(frame, text="Localidad", bg="#ff7f00", fg="white").grid(row=7, column=0, sticky="e", padx=10, pady=5)
        global localidad_combo
        localidad_combo = ttk.Combobox(frame, values=["Localidad 1", "Localidad 2", "Localidad 3"], width=28, state="readonly")
        localidad_combo.grid(row=7, column=1, pady=5)

        tk.Label(frame, text="Club", bg="#ff7f00", fg="white").grid(row=8, column=0, sticky="e", padx=10, pady=5)
        global club_combo
        club_combo = ttk.Combobox(frame, values=["Club A", "Club B", "Club C"], width=28, state="readonly")
        club_combo.grid(row=8, column=1, pady=5)

        # Frame para Ficha Médica y Carnet para que no se mezclen con otros labels
        imagen_frame = tk.Frame(frame, bg="#ff7f00")
        imagen_frame.grid(row=1, column=2, rowspan=8, padx=20, pady=5)

        ficha_medica_label = tk.Label(imagen_frame, text="Ficha Médica", bg="#ff7f00", fg="white")
        ficha_medica_label.grid(row=0, column=0, padx=10, pady=5)

        ficha_medica_img_label = tk.Label(imagen_frame, bg="#ff7f00", text="Sin Imagen")
        ficha_medica_img_label.grid(row=1, column=0, padx=10, pady=5)

        tk.Button(imagen_frame, text="Subir", command=lambda: cargar_imagen(ficha_medica_img_label), bg="grey").grid(row=2, column=0, padx=10, pady=5)

        carnet_label = tk.Label(imagen_frame, text="Carnet", bg="#ff7f00", fg="white")
        carnet_label.grid(row=3, column=0, padx=10, pady=5)

        carnet_img_label = tk.Label(imagen_frame, bg="#ff7f00", text="Sin Imagen")
        carnet_img_label.grid(row=4, column=0, padx=10, pady=5)

        tk.Button(imagen_frame, text="Subir", command=lambda: cargar_imagen(carnet_img_label), bg="grey").grid(row=5, column=0, padx=10, pady=5)

        cancelar_btn = tk.Button(frame, text="Cancelar", bg="red", fg="white", width=10, command=self.root.quit)
        cancelar_btn.grid(row=9, column=1, pady=20, sticky="e")

        guardar_btn = tk.Button(frame, text="Guardar", bg="green", fg="white", width=10, command=confirmar_guardado)
        guardar_btn.grid(row=9, column=2, pady=20, sticky="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = ABMJugadoresApp(root)
    root.mainloop()
