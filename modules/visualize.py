from tkinter.font import Font
from tkinter import ttk,messagebox
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from algorithms.volumes import Calculate_volumes
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

        self.label =  tk.Label(self.tab1, text ="Select an Image: ", font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.label.place(x=30, y= 82, width=180,height=25)
        self.option_menu = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
        self.option_menu.place(x=200, y= 80)
        self.btn = tk.Button(self.tab1, image=self.img_boton, bg="#2c343c", borderwidth=0, command=self.updateOptionmenu)
        self.btn.place(x=440, y= 78, width=40,height=40)

        self.calculate=ctk.CTkButton(self.tab1, height=40, font=("Lucida Grande", 15),text="Calculate",text_color='#a7a1a5',fg_color='#661ae6', command= lambda: self.calculate_volumes())
        self.calculate.place(x=100, y=550)

        
        # Etiquetas
        label1 = tk.Label(self.tab1, text="Cerebrospinal fluid:", font=self.fontStyle3, bg="#2c343c", fg="#a7a1a5")
        label1.place(x=800, y=580, width=180, height=25)
        label2 = tk.Label(self.tab1, text="Grey matter:", font=self.fontStyle3, bg="#2c343c", fg="#a7a1a5")
        label2.place(x=800, y=535, width=110, height=25)
        label3 = tk.Label(self.tab1, text="Normal-appearing white matter:", font=self.fontStyle3, bg="#2c343c", fg="#a7a1a5")
        label3.place(x=300, y=580, width=280, height=25)
        label4 = tk.Label(self.tab1, text="White matter hyperintensities:", font=self.fontStyle3, bg="#2c343c", fg="#a7a1a5")
        label4.place(x=300, y=535, width=260, height=25)


        # Campos de entrada
        self.entry1 = ctk.CTkEntry(self.tab1, placeholder_text="m3", width=80, height=32 ,font =("Lucida Grande",15),border_color="#661ae6", state="disabled")
        self.entry1.place(x=600, y=535)
        self.entry2 = ctk.CTkEntry(self.tab1, placeholder_text="m3", width=80, height=32 ,font =("Lucida Grande",15),border_color="#661ae6", state="disabled")
        self.entry2.place(x=600, y=580)
        self.entry3 = ctk.CTkEntry(self.tab1, placeholder_text="m3", width=80, height=32 ,font =("Lucida Grande",15),border_color="#661ae6", state="disabled")
        self.entry3.place(x=940, y=535)
        self.entry4 = ctk.CTkEntry(self.tab1, placeholder_text="m3", width=80, height=32 ,font =("Lucida Grande",15),border_color="#661ae6", state="disabled")
        self.entry4.place(x=940, y=580)
    
    def display_selected(self, *args):
        self.path_imagen="MRI/patient/"+self.option_menu.get()
        self.init_plot()

    def init_plot(self):
        self.img = nib.load(self.path_imagen)
        self.data = self.img.get_fdata()

        self.canvasx.delete("all")
        self.canvasy.delete("all")
        self.canvasz.delete("all")

        # Crear una figura y un objeto de plot para el eje x
        self.figx, self.axx = plt.subplots()
        # Mostrar la imagen en el plot
        self.axx.imshow(self.data[5,:,:], cmap='gray')
        self.axx.set_aspect('auto', adjustable='box')
        self.x=5

        # Crear una figura y un objeto de plot el eje y
        self.figy, self.axy = plt.subplots()
        # Mostrar la imagen en el plot
        self.axy.imshow(self.data[:,5,:], cmap='gray')
        self.axy.set_aspect('auto', adjustable='box')
        self.y=5

        # Crear una figura y un objeto de plot el eje z
        self.figz, self.axz = plt.subplots()
        # Mostrar la imagen en el plot
        self.axz.imshow(self.data[:,:,5], cmap="gray")
        self.axz.set_aspect('auto', adjustable='box')
        self.z=5

        #    Convertir la figura en un widget de Tkinter y mostrarla en el canvas
        self.canvas_widgetx = FigureCanvasTkAgg(self.figx, self.canvasx)
        self.canvas_widgetx.draw()
        self.canvas_widgetx.get_tk_widget().place( x=0, y=0,width=400, height=400) 
        cidx = self.figx.canvas.mpl_connect('motion_notify_event', self.onclickx)

        #    Convertir la figura en un widget de Tkinter y mostrarla en el canvas
        self.canvas_widgety = FigureCanvasTkAgg(self.figy, self.canvasy)
        self.canvas_widgety.draw()
        self.canvas_widgety.get_tk_widget().place( x=0, y=0,width=400, height=400) 
        cidy = self.figy.canvas.mpl_connect('motion_notify_event', self.onclicky)

        #    Convertir la figura en un widget de Tkinter y mostrarla en el canvas
        self.canvas_widgetz = FigureCanvasTkAgg(self.figz, self.canvasz)
        self.canvas_widgetz.draw()
        self.canvas_widgetz.get_tk_widget().place( x=0, y=0,width=400, height=400) 
        cidz = self.figz.canvas.mpl_connect('motion_notify_event', self.onclickz)


    def calculate_volumes(self):
        self.data=Calculate_volumes.remove_brain()
        volumes=Calculate_volumes.volumes()

    def updateOptionmenu(self):
         # Obtener lista de archivos y subdirectorios en la carpeta
        self.elements = os.listdir("MRI/patient/")
        if not self.elements:
           
            self.option_menu = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
            self.option_menu.place(x=200, y= 80)

        else:
            self.option_menu = ctk.CTkComboBox(self.tab1,
                                     values=self.elements,
                                     width=220,height=35, state='readonly',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected)
            self.option_menu.place(x=200, y= 80)
    
    def onclickx(self, event):
        if event.xdata and event.ydata:
            self.z = int(event.xdata)
            self.y = int(event.ydata)
            for line in self.axx.lines:
                line.remove()
            for line in self.axy.lines:
                line.remove()
            for line in self.axz.lines:
                line.remove()
            self.axx.axvline(self.z, color='r', linestyle='--')
            self.axx.axhline(self.y, color='r', linestyle='--')
            self.figx.canvas.draw()
        self.visualize(self.x,self.y,self.z,'x')
    def onclicky(self, event):
        if event.xdata and event.ydata:
            self.z = int(event.xdata)
            self.x = int(event.ydata)
            for line in self.axy.lines:
                line.remove()
            for line in self.axx.lines:
                line.remove()
            for line in self.axz.lines:
                line.remove()
            self.axy.axvline(self.z, color='r', linestyle='--')
            self.axy.axhline(self.x, color='r', linestyle='--')
            self.figy.canvas.draw()
        self.visualize(self.x,self.y,self.z,'y')
    def onclickz(self, event):
        if event.xdata and event.ydata:
            self.x = int(event.xdata)
            self.y = int(event.ydata)
            for line in self.axz.lines:
                line.remove()
            for line in self.axx.lines:
                line.remove()
            for line in self.axy.lines:
                line.remove()
            self.axz.axvline(self.x, color='r', linestyle='--')
            self.axz.axhline(self.y, color='r', linestyle='--')
            self.figz.canvas.draw()
        self.visualize(self.x,self.y,self.z,'z')
    
    def visualize (self,x,y,z,axis):
        
        if self.path_imagen!="":

            # Mostrar la imagen en el plot
            if axis=='x':
                self.canvasy.delete("all")
                self.canvasz.delete("all")

                self.axy.imshow(self.data[:,self.y,:], cmap="gray")
                #self.axz.imshow(np.rot90(np.rot90(np.rot90(self.data[:, :, self.z]))), cmap="gray")
                self.axz.imshow(self.data[:, :, self.z], cmap="gray")
                self.axy.set_aspect('auto', adjustable='box')
                self.axz.set_aspect('auto', adjustable='box')
                self.canvas_widgety.draw()
                self.canvas_widgetz.draw()

            elif axis=='y':
                self.canvasx.delete("all")
                self.canvasz.delete("all")

                self.axx.imshow(self.data[self.x,:,:], cmap="gray")
                self.axz.imshow(self.data[:,:,self.z], cmap="gray")
                self.axx.set_aspect('auto', adjustable='box')
                self.axz.set_aspect('auto', adjustable='box')
                self.canvas_widgetx.draw()
                self.canvas_widgetz.draw()

            elif axis=='z':
                self.canvasy.delete("all")
                self.canvasx.delete("all")

                self.axy.imshow(self.data[:,self.y,:], cmap="gray")
                self.axx.imshow(self.data[self.x,:,:], cmap="gray")
                self.axy.set_aspect('auto', adjustable='box')
                self.axx.set_aspect('auto', adjustable='box')
                self.canvas_widgety.draw()
                self.canvas_widgetx.draw()

            # Convertir la figura en un widget de Tkinter y mostrarla en el canvas
            self.canvas_widgetx.draw()
        