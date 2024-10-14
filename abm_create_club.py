import sqlite3
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ClubesABM:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Clubes de Handball")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        self.root.config(bg="#3b3b3b")
        self.root.option_add("*Font", "Arial 16 bold")

        
        self.conn = sqlite3.connect('ligahandball.db')
        self.cursor = self.conn.cursor()

       
        self.frame = tk.Frame(self.root, bg="#3b3b3b")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        
        self.label_nombre = tk.Label(self.frame, text="Nombre del Club:", bg="#3b3b3b",fg="#FF914D")
        self.label_nombre.grid(column=0, row=0, padx=15, pady=15)
        self.entry_nombre = tk.Entry(self.frame, width=25)
        self.entry_nombre.grid(column=1, row=0, padx=15, pady=15)

        
        self.label_foto = tk.Label(self.frame, text="Foto:", bg="#3b3b3b",fg="#FF914D")
        self.label_foto.grid(column=0, row=1, padx=15, pady=15)
        self.entry_foto = tk.Entry(self.frame, width=25)
        self.entry_foto.config(state="disabled")
        self.entry_foto.grid(column=1, row=1, padx=15, pady=15)
        self.button_foto = tk.Button(self.frame, text="Seleccionar", command=self.seleccionar_foto)
        self.button_foto.grid(column=2, row=1, padx=15, pady=15)
    
       
        self.label_imagen = tk.Label(self.frame)
        self.label_imagen.grid(column=0, row=2, columnspan=3, padx=15, pady=15)

       
        self.button_guardar = tk.Button(self.frame, text="Guardar", command=self.guardar_club,bg="#FF914D")
        self.button_guardar.grid(column=1, row=3, padx=15, pady=15)
        self.button_salir = tk.Button(self.frame, text="Salir", command=self.salir,bg="#FF914D")
        self.button_salir.grid(column=2, row=3, padx=15, pady=15)

    def seleccionar_foto(self):
        try:
            archivo = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Imágenes", ".jpg .jpeg .png")])
            self.entry_foto.config(state="normal")
            self.entry_foto.delete(0, tk.END)
            self.entry_foto.insert(0, archivo)
            self.entry_foto.config(state="disabled")
            self.mostrar_imagen(archivo)
        except Exception as e:
            print(f"Error seleccionando foto: {e}")

    def mostrar_imagen(self, archivo):
        try:
            imagen = Image.open(archivo)
            imagen.thumbnail((300, 300))  
            foto = ImageTk.PhotoImage(imagen)
            self.label_imagen.config(image=foto)
            self.label_imagen.image = foto
        except Exception as e:
            print(f"Error mostrando imagen: {e}")

    def guardar_club(self):
        try:
            nombre = self.entry_nombre.get()
            foto = self.entry_foto.get()
            if nombre and foto:
                imagen = Image.open(foto)
                imagen.thumbnail((100, 100))  
                foto_bytes = imagen.tobytes()
                self.cursor.execute("INSERT INTO clubes (nombre, foto) VALUES (?, ?)", (nombre, foto_bytes))
                self.conn.commit()
                self.entry_nombre.delete(0, tk.END)
                self.entry_foto.config(state="normal")
                self.entry_foto.delete(0, tk.END)
                self.entry_foto.config(state="disabled")
                self.label_imagen.config(image=None)
                print("Club registrado con éxito")
            else:
                print("Ingrese todos los campos")
        except Exception as e:
            print(f"Error guardando club: {e}")

    def salir(self):
        try:
            self.conn.close()
            self.root.destroy()
        except Exception as e:
            print(f"Error saliendo: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ClubesABM()
    app.run()