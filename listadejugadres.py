from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from tkcalendar import DateEntry  
from PIL import Image, ImageTk
import re

directorio_imagenes = r"C:\Users\Usuario\Downloads\visual code\matematica\Liga de Handball Punilla"

def cargar_imagen(label):
    archivo = filedialog.askopenfilename(initialdir=directorio_imagenes, filetypes=[("Imágenes", ".png;.jpg;*.jpeg")])
    if archivo:
        img = Image.open(archivo)
        img = img.resize((300, 300))  
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img


def verificar_correo(correo):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, correo):
        messagebox.showerror("Error", f"{correo} : no es una dirección de correo válida.")
        return False
    return True

def validar_dni(dni):
    if not dni.isdigit():
        messagebox.showerror("Error", "El DNI debe contener solo dígitos.")
        return False
    elif len(dni) < 7 or len(dni) > 8:
        messagebox.showerror("Error", "El número del DNI debe tener 7 u 8 dígitos.")
        return False
    return True

def validar_telefono(telefono):
    if not telefono.isdigit():
        messagebox.showerror("Error", "El teléfono debe contener solo dígitos.")
        return False
    elif len(telefono) < 6 or len(telefono) > 10:
        messagebox.showerror("Error", "El número de teléfono debe tener entre 6 y 10 dígitos.")
        return False
    return True

def validar_campos_obligatorios(entries):
    if any(entry.get().strip() == "" for entry in entries):
        messagebox.showerror("Error", "Todos los campos obligatorios deben completarse.")
        return False
    return True

def validar_campos():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    dni = entry_dni.get()
    domicilio = entry_domicilio.get()
    telefono = entry_telefono.get()
    fecha_nacimiento = entry_fecha_nacimiento.get_date()
    correo = entry_correo.get()
    localidad = localidad_combo.get()
    club = club_combo.get()
    tipo = tipo_combo.get()

    if not validar_campos_obligatorios([entry_nombre, entry_apellido, entry_dni, entry_correo]):
        return False

    if not re.match("^[A-Za-z ]+$", nombre):
        messagebox.showerror("Error", "El nombre solo debe contener letras y espacios.")
        return False
    if not re.match("^[A-Za-z ]+$", apellido):
        messagebox.showerror("Error", "El apellido solo debe contener letras y espacios.")
        return False
    if not validar_dni(dni):
        return False
    if not validar_telefono(telefono):
        return False
    if not verificar_correo(correo):
        return False

    if tipo == 'Categoría':
        messagebox.showerror("Error", "Debe seleccionar una categoría válida.")
        return False
    if localidad == 'Ninguna':
        messagebox.showerror("Error", "Debe seleccionar una localidad.")
        return False
    if club == 'Cualquiera':
        messagebox.showerror("Error", "Debe seleccionar un club.")
        return False

    if ficha_medica_img_label.image is None or carnet_img_label.image is None:
        messagebox.showerror("Error", "Es obligatorio cargar el Carnet y la Ficha Médica.")
        return False

    if messagebox.askyesno("Confirmación", "¿Está seguro que desea guardar?"):
        messagebox.showinfo("Éxito", "Datos guardados exitosamente ⚽")
        borrar_datos()
    return True

def borrar_datos():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
    entry_domicilio.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_fecha_nacimiento.set_date('2024-10-23')  
    entry_correo.delete(0, tk.END)
    tipo_combo.set('Categoría')
    localidad_combo.set('Ninguna')
    club_combo.set('Cualquiera')
    ficha_medica_img_label.config(image='', text="Sin Imagen")
    ficha_medica_img_label.image = None
    carnet_img_label.config(image='', text="Sin Imagen")
    carnet_img_label.image = None

def confirmar_borrado():
    if messagebox.askyesno("Confirmación", "¿Está seguro que desea borrar todos los datos?"):
        borrar_datos()

def volver_menu():
    root.destroy()

def solo_letras(char):
    return char.isalpha() or char == " "

def solo_numeros(char):
    return char.isdigit()

root = tk.Tk()
root.title("Alta/Modificación de Jugadores")
root.geometry("1366x765")
root.configure(bg="#ff7f00")
root.resizable(False, False)

frame_datos = tk.Frame(root, bg="#ff7f00")
frame_datos.grid(row=0, column=0, padx=20, pady=10, sticky="n")

frame_imagenes = tk.Frame(root, bg="#ff7f00")
frame_imagenes.grid(row=0, column=1, padx=20, pady=10, sticky="n")

frame_botones = tk.Frame(root, bg="#ff7f00")
frame_botones.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="n")

tk.Label(frame_datos, text="Nombre (Obligatorio)", bg="#ff7f00", fg="black").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_nombre = tk.Entry(frame_datos, width=30, validate="key")
entry_nombre['validatecommand'] = (root.register(solo_letras), '%S')
entry_nombre.grid(row=1, column=1, pady=5)

tk.Label(frame_datos, text="Apellido (Obligatorio)", bg="#ff7f00", fg="black").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_apellido = tk.Entry(frame_datos, width=30, validate="key")
entry_apellido['validatecommand'] = (root.register(solo_letras), '%S')
entry_apellido.grid(row=2, column=1, pady=5)

tk.Label(frame_datos, text="D.N.I (Obligatorio)", bg="#ff7f00", fg="black").grid(row=3, column=0, sticky="e", padx=10, pady=5)
entry_dni = tk.Entry(frame_datos, width=30, validate="key")
entry_dni['validatecommand'] = (root.register(solo_numeros), '%S')
entry_dni.grid(row=3, column=1, pady=5)

tk.Label(frame_datos, text="Domicilio", bg="#ff7f00", fg="white").grid(row=4, column=0, sticky="e", padx=10, pady=5)
entry_domicilio = tk.Entry(frame_datos, width=30)
entry_domicilio.grid(row=4, column=1, pady=5)

tk.Label(frame_datos, text="Teléfono", bg="#ff7f00", fg="white").grid(row=5, column=0, sticky="e", padx=10, pady=5)
entry_telefono = tk.Entry(frame_datos, width=30, validate="key")
entry_telefono['validatecommand'] = (root.register(solo_numeros), '%S')
entry_telefono.grid(row=5, column=1, pady=5)

tk.Label(frame_datos, text="Correo Electrónico (Obligatorio)", bg="#ff7f00", fg="white").grid(row=6, column=0, sticky="e", padx=10, pady=5)
entry_correo = tk.Entry(frame_datos, width=30)
entry_correo.grid(row=6, column=1, pady=5)

tk.Label(frame_datos, text="Fecha de Nacimiento", bg="#ff7f00", fg="white").grid(row=7, column=0, sticky="e", padx=10, pady=5)
entry_fecha_nacimiento = DateEntry(frame_datos, width=27, background="orange", foreground="black", date_pattern="yyyy-mm-dd", state="readonly")  
entry_fecha_nacimiento.grid(row=7, column=1, pady=5)

tk.Label(frame_datos, text="Localidad", bg="#ff7f00", fg="black").grid(row=8, column=0, sticky="e", padx=10, pady=5)
localidad_combo = ttk.Combobox(frame_datos, values=["Ninguna", "Cosquín", "La Falda", "Mina Clavero"], state="readonly")
localidad_combo.set("Ninguna")
localidad_combo.grid(row=8, column=1, pady=5)

tk.Label(frame_datos, text="Club", bg="#ff7f00", fg="black").grid(row=9, column=0, sticky="e", padx=10, pady=5)
club_combo = ttk.Combobox(frame_datos, values=["Cualquiera", "Club 1", "Club 2", "Club 3"], state="readonly")
club_combo.set("Cualquiera")
club_combo.grid(row=9, column=1, pady=5)

tk.Label(frame_datos, text="Categoría", bg="#ff7f00", fg="black").grid(row=10, column=0, sticky="e", padx=10, pady=5)
tipo_combo = ttk.Combobox(frame_datos, values=["Categoría", "Femenino", "Masculino"], state="readonly")
tipo_combo.set("Categoría")
tipo_combo.grid(row=10, column=1, pady=5)

ficha_medica_img_label = tk.Label(frame_imagenes, text="Sin Imagen", bg="#ff7f00", width=20, height=6)
ficha_medica_img_label.grid(row=0, column=0, padx=10, pady=10)

carnet_img_label = tk.Label(frame_imagenes, text="Sin Imagen", bg="#ff7f00", width=20, height=6)
carnet_img_label.grid(row=0, column=1, padx=10, pady=10)

btn_cargar_ficha_medica = tk.Button(frame_imagenes, text="Cargar Ficha Médica", command=lambda: cargar_imagen(ficha_medica_img_label), bg="gray", fg="black")
btn_cargar_ficha_medica.grid(row=1, column=0, padx=10, pady=10)

btn_cargar_carnet = tk.Button(frame_imagenes, text="Cargar Carnet", command=lambda: cargar_imagen(carnet_img_label), bg="gray", fg="black")
btn_cargar_carnet.grid(row=1, column=1, padx=10, pady=10)

btn_guardar = tk.Button(frame_botones, text="Guardar", command=validar_campos, bg="#4caf50", fg="white")
btn_guardar.grid(row=0, column=0, padx=20, pady=10)

btn_borrar = tk.Button(frame_botones, text="Borrar", command=confirmar_borrado, bg="#f44336", fg="white")
btn_borrar.grid(row=0, column=1, padx=20, pady=10)

btn_volver = tk.Button(frame_botones, text="Volver", command=volver_menu, bg="#2196f3", fg="white")
btn_volver.grid(row=0, column=2, padx=20, pady=10)

root.mainloop()
