import tkinter as tk
from PIL import Image, ImageTk
import reglamento
import Historia
import Autoridades


def abrir_historia():
    Historia.crear_ventana(ventana_principal)

def abrir_Autoridades():
    Autoridades.crear_ventana(ventana_principal)

def abrir_reglamento():
    reglamento.crear_ventana(ventana_principal)

def main():
    global ventana_principal  # Hacer que esta variable sea global para usarla en `abrir_ventana`
    ventana_principal = tk.Tk()
    ventana_principal.geometry("1400x700+100+50")
    ventana_principal.title("Liga Handball")
    fondo = "#ff7700"
    
    # Frames (superior e inferior)
    frame_superior = tk.Frame(ventana_principal, bg=fondo)
    frame_superior.pack(fill="both", expand=True)
    
    frame_inferior = tk.Frame(ventana_principal, bg=fondo)
    frame_inferior.pack(fill="both", expand=True)
    
    frame_medio = tk.Frame(ventana_principal, bg=fondo, width=500, height=500)
    frame_medio.place(relx=0.5, rely=0.74, anchor="center")

    # Titulo
    titulo = tk.Label(frame_superior, text="Menu", font=("Arial", 24, "bold"), bg=fondo)
    titulo.place(relx=0.47, rely=0.2)
    
    img = Image.open("logo.png").resize((200, 200))
    render = ImageTk.PhotoImage(img)
    fondo = tk.Label(frame_superior, image=render, bg=fondo)
    fondo.place(relx=0.5, rely=0.7, anchor="center")

        # Botones
    historia = tk.Button(frame_medio, text="Historia", font=("Mononoki", 20, "bold"), command=abrir_historia)
    historia.grid(row=5, column=2, padx=20)
        
    autoridades = tk.Button(frame_medio, text="Autoridades", font=("Mononoki", 20, "bold"),command=abrir_Autoridades)
    autoridades.grid(row=5, column=1, padx=20)
        
    reglamento = tk.Button(frame_medio, text="Reglamento", font=("Mononoki", 20, "bold"), command=abrir_reglamento)
    reglamento.grid(row=5, column=3, padx=20)
        
    #cerrar_seccion = tk.Button(frame_medio, text="Cerrar Sesión", width=24, font=("Mononoki", 20, "bold"), command=cerrar_seccion_def)
    #cerrar_seccion.grid(row=6, column=1, columnspan=3, pady=20)
    
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()


