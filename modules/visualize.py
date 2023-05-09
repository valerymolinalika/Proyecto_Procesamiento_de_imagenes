from tkinter.font import Font
from tkinter import ttk,messagebox
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os

class visualize():
    def __init__(self, window, tab):
        
        self.tab1=tab
        self.ventana=window
        
        self.img_boton = tk.PhotoImage(file="images/refresh.png")
        self.img_boton2 = tk.PhotoImage(file="images/_ok.png")
        self.fontStyle1 = Font(family="Tw Cen MT", size=35, weight="bold", slant="roman", underline=0, overstrike=0)
        self.fontStyle2 = Font(family="Lucida Grande", size=25)
        self.fontStyle3 = Font(family="Lucida Grande", size=15)

        # Titulo de la app
        self.title =  tk.Label(self.tab1, text ="VISUALIZE YOUR IMAGE", font=self.fontStyle1, bg="#2c343c",fg="white" )
        self.title.place(x=5, y= 5, width=500,height=70)

        # Crear un lienzo para mostrar la imagen
        self.canvasx = tk.Canvas(self.tab1, bg='#2c343c')
        self.canvasx.place(x=10, y= 120, width=400, height=400)

        # Crear un lienzo para mostrar la imagen
        self.canvasy = tk.Canvas(self.tab1, bg='#2c343c')
        self.canvasy.place(x=420, y= 120, width=400, height=400)

        # Crear un lienzo para mostrar la imagen
        self.canvasz = tk.Canvas(self.tab1, bg='#2c343c')
        self.canvasz.place(x=830, y= 120, width=400, height=400)

        combobox = ctk.CTkComboBox(self.tab1,
                                     values=["option 1", "option 2"],
                                     width=200, state="readonly", )
        combobox.place(x=0.35, y=20)
        #self.option_menu.configure(background="#2c343c",foreground='yellow', state='disabled',  highlightbackground='#661ae6')

    #     self.canvas.delete("all")
    def display_selected(self, *args):
        self.path_imagen="MRI/patient/"+self.selected_element.get()
        self.init_plot()

    def init_plot(self):
        self.img = nib.load(self.path_imagen)
        self.data = self.img.get_fdata()
        # Mostrar la imagen en un lienzo
        self.canvas.delete("all")
        # Crear una figura y un objeto de plot
        self.fig, self.ax = plt.subplots()
        # Mostrar la imagen en el plot
        self.ax.imshow(self.data[:,:,5])
        #    Convertir la figura en un widget de Tkinter y mostrarla en el canvas
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvasx)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().place( x=0, y=0,width=400, height=400) 

    def updateOptionmenu(self):
         # Obtener lista de archivos y subdirectorios en la carpeta
        self.elements = os.listdir("MRI/patient/")
        if not self.elements:
           
             self.option_menu = ctk.CTkComboBox(self.tab1,
                                     values=self.elements,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
             self.option_menu.place(x=280, y= 277, )

        else:
           
            self.option_menu = ctk.CTkComboBox(self.tab1,
                                     values=self.elements,
                                     width=220,height=35, state='readonly',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected)
            self.option_menu.place(x=280, y= 277, )