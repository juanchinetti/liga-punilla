import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re


def validar_contraseña(password):
    if len(password) < 6:  
        return False
    if not re.search(r'[A-Z]', password):  
        return False
    if not re.search(r'[a-z]', password): 
        return False
    if not re.search(r'[0-9]', password): 
        return False
    return True


def login():
    username = entry_username.get()
    password = entry_password.get()

    
    if username == "admin" and validar_contraseña(password):
        messagebox.showinfo("Inicio de Sesión", "¡Inicio de sesión exitoso!")
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos. \n"
                                      "La contraseña debe tener al menos una mayúscula, una minúscula y un número.")


root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("1366x768") 


root.config(bg="#FF914D")


# Cargar y redimensionar la imagen
original_image = Image.open("Logo_Handball.png")
resized_image = original_image.resize((325, 325))
logo_image = ImageTk.PhotoImage(resized_image)

label_title = tk.Label(root, text="Inicio de Sesión", font=("Arial", 18, "bold"), bg="#FF914D", fg="black")
label_title.pack(pady=10)  

label_username = tk.Label(root, text="Nombre de Usuario:", bg="#FF914D", fg="#000000", font=("Arial", 14, "bold"))
label_username.pack(pady=5)
entry_username = tk.Entry(root, font=("Arial", 12))
entry_username.pack(pady=5, ipadx=20, ipady=5)


label_password = tk.Label(root, text="Contraseña:", bg="#FF914D", fg="#000000", font=("Arial", 14, "bold"))
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*", font=("Arial", 12))
entry_password.pack(pady=5, ipadx=20, ipady=5)


button_login = tk.Button(root, text="Iniciar Sesión", command=login, bg="#FFFFFF", fg="#000000", activebackground="#DDDDDD", activeforeground="#000000", font=("Arial", 12, "bold"))
button_login.pack(pady=20)


root.mainloop()
