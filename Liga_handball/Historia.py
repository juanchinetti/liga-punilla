import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import re

root = tk.Tk()
root.title("Historia")
root.geometry("1365x768")
root.configure(bg="#ff7700")

def Volver_menu():
    root.destroy()
    import Menu
    
label = tk.Label(root, text="Historia", font=("Calibri", 24), bg="#ff7700")
label.pack(pady=(20, 10))

boton1 = tk.Button (root, text="Volver", font=("Calibri",24),bg="white", command=Volver_menu)
boton1.pack(pady=(30, 20))
root.mainloop()