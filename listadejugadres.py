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
        img.thumbnail((120, 120), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img

def validar_campos():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    dni = entry_dni.get()
    domicilio = entry_domicilio.get()
    telefono = entry_telefono.get()
    fecha_nacimiento = entry_fecha_nacimiento.get_date()  
    correo = entry_correo.get()

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
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
        messagebox.showerror("Error", "Por favor, ingrese un correo electrónico válido")
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
    entry_fecha_nacimiento.set_date('')  
    entry_correo.delete(0, tk.END)  
    tipo_combo.set('') 
    localidad_combo.set('')  
    club_combo.set('')  
    ficha_medica_img_label.config(image='', text="Sin Imagen")  
    carnet_img_label.config(image='', text="Sin Imagen") 
    ficha_medica_img_label.image = None  
    carnet_img_label.image = None  
        
def volver_menu():
    root.destroy()  

root = tk.Tk()
root.title("Alta/Modificación de Jugadores")
root.geometry("1366x765")
root.configure(bg="#ff7f00")
root.resizable(False, False)

frame = tk.Frame(root, bg="#ff7f00")
frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

tk.Label(frame, text="Nombre (Obligatorio)", bg="#ff7f00", fg="black").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_nombre = tk.Entry(frame, width=30)
entry_nombre.grid(row=1, column=1, pady=5)

def solo_letras(event):
    if not event.char.isalpha() and event.keysym != 'BackSpace':
        return "break"

entry_nombre.bind("<KeyPress>", solo_letras)

tk.Label(frame, text="Apellido (Obligatorio)", bg="#ff7f00", fg="black").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_apellido = tk.Entry(frame, width=30)
entry_apellido.grid(row=2, column=1, pady=5)
entry_apellido.bind("<KeyPress>", solo_letras)

tk.Label(frame, text="D.N.I (Obligatorio)", bg="#ff7f00", fg="black").grid(row=3, column=0, sticky="e", padx=10, pady=5)
entry_dni = tk.Entry(frame, width=30)
entry_dni.grid(row=3, column=1, pady=5)

def solo_numeros(event):
    if not event.char.isdigit() and event.keysym != 'BackSpace':
        return "break"

entry_dni.bind("<KeyPress>", solo_numeros)

tk.Label(frame, text="Domicilio", bg="#ff7f00", fg="white").grid(row=4, column=0, sticky="e", padx=10, pady=5)
entry_domicilio = tk.Entry(frame, width=30)
entry_domicilio.grid(row=4, column=1, pady=5)

tk.Label(frame, text="Teléfono", bg="#ff7f00", fg="white").grid(row=5, column=0, sticky="e", padx=10, pady=5)
entry_telefono = tk.Entry(frame, width=30)
entry_telefono.grid(row=5, column=1, pady=5)
entry_telefono.bind("<KeyPress>", solo_numeros)

tk.Label(frame, text="Fecha de Nacimiento", bg="#ff7f00", fg="white").grid(row=6, column=0, sticky="e", padx=10, pady=5)
entry_fecha_nacimiento = DateEntry(frame, width=27, background="orange", foreground="black", date_pattern="yyyy-mm-dd", state="readonly")
entry_fecha_nacimiento.grid(row=6, column=1, pady=5)

tk.Label(frame, text="Correo Electrónico", bg="#ff7f00", fg="white").grid(row=7, column=0, sticky="e", padx=10, pady=5)
entry_correo = tk.Entry(frame, width=30)
entry_correo.grid(row=7, column=1, pady=5)

tk.Label(frame, text="Tipo", bg="#ff7f00", fg="white").grid(row=8, column=0, sticky="e", padx=10, pady=5)
tipo_combo = ttk.Combobox(frame, values=["Masculino", "Femenino"], width=28, state='readonly')
tipo_combo.grid(row=8, column=1, pady=5)

tk.Label(frame, text="Localidad", bg="#ff7f00", fg="white").grid(row=9, column=0, sticky="e", padx=10, pady=5)
localidad_combo = ttk.Combobox(frame, values=["Localidad 1", "Localidad 2", "Localidad 3"], width=28, state='readonly')
localidad_combo.grid(row=9, column=1, pady=5)

tk.Label(frame, text="Club", bg="#ff7f00", fg="white").grid(row=10, column=0, sticky="e", padx=10, pady=5)
club_combo = ttk.Combobox(frame, values=["Club A", "Club B", "Club C"], width=28, state='readonly')
club_combo.grid(row=10, column=1, pady=5)

ficha_medica_label = tk.Label(frame, text="Ficha Médica", bg="#ff7f00", fg="white")
ficha_medica_label.grid(row=1, column=3, padx=10, pady=5)

ficha_medica_img_label = tk.Label(frame, bg="#ff7f00", text="Sin Imagen")
ficha_medica_img_label.grid(row=2, column=3, padx=10, pady=5)

tk.Button(frame, text="Subir", command=lambda: cargar_imagen(ficha_medica_img_label), bg="grey").grid(row=3, column=3, padx=10, pady=5)

carnet_label = tk.Label(frame, text="Carnet", bg="#ff7f00", fg="white")
carnet_label.grid(row=4, column=3, padx=10, pady=5)

carnet_img_label = tk.Label(frame, bg="#ff7f00", text="Sin Imagen")
carnet_img_label.grid(row=5, column=3, padx=10, pady=5)

tk.Button(frame, text="Subir", command=lambda: cargar_imagen(carnet_img_label), bg="grey").grid(row=6, column=3, padx=10, pady=5)

cancelar_btn = tk.Button(frame, text="Cancelar", bg="red", fg="white", width=10, command=borrar_datos)
cancelar_btn.grid(row=11, column=0, pady=20)

guardar_btn = tk.Button(frame, text="Guardar", bg="green", fg="white", width=10, command=validar_campos)
guardar_btn.grid(row=11, column=1, pady=20)

volver_menu_btn = tk.Button(frame, text="Volver", bg="lightblue", fg="black", width=10)
volver_menu_btn.grid(row=11, column=2, pady=20)

root.mainloop()