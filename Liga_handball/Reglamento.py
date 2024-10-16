import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import re
def main():
    root = tk.Tk()
    root.title("Reglamento")
    root.geometry("1365x768")
    root.configure(bg="#ff7700")

    label = tk.Label(root, text="Reglamento", font=("Calibri", 24), bg="#ff7700")
    label.pack(pady=(20, 10))

    def Volver_menu():
        root.destroy()
        import Menu
    
    boton1 = tk.Button (root, text="Volver", font=("Calibri",24),bg="white", command=Volver_menu)
    boton1.pack(pady=(30, 20))


    root.mainloop()

main()