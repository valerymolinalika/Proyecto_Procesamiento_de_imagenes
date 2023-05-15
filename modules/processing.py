from tkinter.font import Font
from tkinter import ttk,messagebox
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms.standardization import standardization
from algorithms.denoise import denoise
import shutil
import os


class processing():
    def __init__(self, window, tab):
        
        self.tab1=tab
        self.ventana=window

        # Cargar fuentes e imagenes
        self.img_boton = tk.PhotoImage(file="images/refresh.png")
        self.img_boton2 = tk.PhotoImage(file="images/_ok.png")
        self.fontStyle1 = Font(family="Tw Cen MT", size=35, weight="bold", slant="roman", underline=0, overstrike=0)
        self.fontStyle2 = Font(family="Lucida Grande", weight="bold", size=25)
        self.fontStyle3 = Font(family="Lucida Grande", size=15)

        # Titulo de la app
        self.title =  tk.Label(self.tab1, text ="PROCESSING YOUR IMAGE", font=self.fontStyle1, bg="#2c343c",fg="white" )
        self.title.place(x=10, y= 10, width=600,height=100)

         # Crear un lienzo para mostrar la imagen
        self.canvas = tk.Canvas(self.tab1, bg='#2c343c')
        self.canvas.place(x=700, y= 40, width=450, height=450)

        self.label =  tk.Label(self.tab1, text ="Select an Image: ", font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.label.place(x=25, y= 122, width=180,height=25)
        self.option_menu = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
        self.option_menu.place(x=310, y= 120)
        self.btn = tk.Button(self.tab1, image=self.img_boton, bg="#2c343c", borderwidth=0, command=self.updateOptionmenu)
        self.btn.place(x=540, y= 117, width=40,height=40)

        self.labelMethod =  tk.Label(self.tab1, text ="Select segmentation method: ", font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.labelMethod.place(x=15, y= 168, width=300,height=50)

        self.segmentation_method = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
        self.segmentation_method.place(x=310, y= 175)

    def updateOptionmenu(self):
         # Obtener lista de archivos y subdirectorios en la carpeta
        self.elements = os.listdir("MRI/patient/")
        if not self.elements:
           
            self.option_menu = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
            self.option_menu.place(x=200, y= 120)

        else:
            self.option_menu = ctk.CTkComboBox(self.tab1,
                                     values=self.elements,
                                     width=220,height=35, state='readonly',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected)
            self.option_menu.place(x=200, y= 120)
            
            self.segmentation_method = ctk.CTkComboBox(self.tab1,
                                     values=['Tresholding','Region growing', 'K-means'],
                                     width=220,height=35, state='readonly',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected2)
            self.segmentation_method.place(x=200, y= 250)


    def display_selected(self, *args):
        self.path_imagen="MRI/patient/"+self.option_menu.get()
        self.init_plot()

    def init_plot(self):
        self.img = nib.load(self.path_imagen)
        self.data = self.img.get_fdata()
        # Mostrar la imagen en un lienzo
        self.canvas.delete("all")
        
        # Crear una figura y un objeto de plot       
        self.fig, self.ax= plt.subplots()
        # Mostrar la imagen en el plot
        self.ax.imshow(self.data[:,:,15])
        #    Convertir la figura en un widget de Tkinter y mostrarla en el canvas
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().place( x=0, y=0,width=450, height=450)
    
    def display_selected2(self, *args):
        if self.segmentation_method.get()=='Thresholding' and self.path_imagen!="" :
            self.tautext = tk.Label(self.tab1, text ="Tau:", font=self.fontStyle3, bg="#00415d",fg="white" )
            self.tautext.place(x=50, y= 300, width=80,height=100)
            self.entry = tk.Entry(self.tab1,justify="center")
            self.entry.insert(0, "110")
            self.entry.place(x=60, y=380,width=150,height=40)

            self.toletext = tk.Label(self.tab1, text ="Tolerance:", font=self.fontStyle3, bg="#00415d",fg="white" )
            self.toletext.place(x=250, y= 300, width=150,height=100)
            self.entry2 = tk.Entry(self.tab1,justify="center")
            self.entry2.insert(0, "1")
            self.entry2.place(x=250, y=380,width=150,height=40)

            self.btn = tk.Button(self.tab1, image=self.img_boton2, bg="#00415d", borderwidth=0, command= lambda: self.callfunction("1"))
            self.btn.place(x=400, y= 370, width=80,height=50)