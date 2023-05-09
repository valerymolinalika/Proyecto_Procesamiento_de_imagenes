from tkinter.font import Font
from tkinter import ttk,messagebox
from tkinter import *
import tkinter as tk

from modules.uploadImages import uploadImages
from modules.visualize import visualize
import os

class interfaz():
    def __init__(self):

        # Borra archivos previos
        archivos = os.listdir("MRI/patient/")
        for archivo in archivos:
            ruta_archivo = os.path.join("MRI/patient/", archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
         # Creacion de la ventana
        self.ventana =  tk.Tk()
        self.ventana.geometry(f"{1250}x{650}+{0}+{0}")
        self.ventana.configure(bg='#2c343c')
        self.path_imagen=""
        self.size=10

        # Crear un widget Notebook con dos pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True)

        # Pestaña 1: Interfaz de usuario
        self.tab1 = tk.Frame(self.notebook,bg='#2c343c')
        self.notebook.add(self.tab1, text='Upload Images')

        self.tab2 = tk.Frame(self.notebook, bg='#2c343c')
        self.notebook.add(self.tab2, text='Preprocessing')

        self.tab3 = tk.Frame(self.notebook, bg='#2c343c')
        self.notebook.add(self.tab3, text='Processing')

        self.tab4 = tk.Frame(self.notebook, bg='#2c343c')
        self.notebook.add(self.tab4, text='Visualize')

        uploadImages(self.ventana, self.tab1)
        visualize(self.ventana, self.tab4)
        self.ventana.mainloop()

mi_interfaz = interfaz()
