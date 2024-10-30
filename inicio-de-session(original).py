import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os

def verificar_usuario(username, password):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LigaHandball"
        )
        cursor = conexion.cursor()
        query = "SELECT * FROM Usuarios WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado is not None
    except mysql.connector.Error as err:
        messagebox.showerror("Error de base de datos", f"Error al conectar con la base de datos: {err}")
        return False

def login():
    username = entry_username.get()
    password = entry_password.get()

    if verificar_usuario(username, password):
        messagebox.showinfo("Inicio de Sesión", "¡Inicio de sesión exitoso!")
        root.destroy()
        os.system("python menu.py")
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("1366x768")
root.state('zoomed')
root.resizable(False, False)
root.config(bg="#ff7700")

# Título
label_title = tk.Label(root, text="Inicio de Sesión", font=("Calibri", 25, "bold"), bg="#ff7700", fg="#FFFFFF")
label_title.pack(pady=20)

# Crear un marco para los campos de entrada y etiquetas con bordes redondeados
frame = tk.Frame(root, bg="#252e32", bd=2, relief="groove", width=600, height=400)
frame.pack(padx=20, pady=20)
frame.pack_propagate(False)

# Campo de entrada para el nombre de usuario
label_username = tk.Label(frame, text="Usuario:", font=("Calibri", 25, "bold"), bg="#252e32", fg="#FFFFFF")
label_username.pack(pady=10)
entry_username = tk.Entry(frame, font=("Calibri", 25), bd=0, highlightthickness=0, relief="flat")
entry_username.pack(pady=10, ipadx=20, ipady=5)

# Campo de entrada para la contraseña
label_password = tk.Label(frame, text="Contraseña:", font=("Calibri", 25, "bold"), bg="#252e32", fg="#FFFFFF")
label_password.pack(pady=10)
entry_password = tk.Entry(frame, show="*", font=("Calibri", 25), bd=0, highlightthickness=0, relief="flat")
entry_password.pack(pady=10, ipadx=20, ipady=5)

# Botón para iniciar sesión
button_login = tk.Button(frame, text="Iniciar Sesión", command=login, bg="#FFFFFF", fg="#000000",
                         activebackground="#DDDDDD", activeforeground="#000000", font=("Calibri", 25, "bold"))
button_login.pack(pady=30)

# Ejecutar la aplicación
root.mainloop()
