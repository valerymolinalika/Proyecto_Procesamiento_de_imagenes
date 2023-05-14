from tkinter.font import Font
from tkinter import ttk,messagebox
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import shutil
import os


class uploadImages():
    def __init__(self, window, tab):
        
        self.tab1=tab
        self.ventana=window

        # Cargar fuentes e imagenes
        self.img_boton = tk.PhotoImage(file="images/upload.png")
        self.img_boton2 = tk.PhotoImage(file="images/_ok.png")
        self.fontStyle1 = Font(family="Tw Cen MT", size=35, weight="bold", slant="roman", underline=0, overstrike=0)
        self.fontStyle2 = Font(family="Lucida Grande", weight="bold", size=25)
        self.fontStyle3 = Font(family="Lucida Grande", size=15)

        # Titulo de la app
        self.title =  tk.Label(self.tab1, text ="UPLOAD YOUR IMAGE", font=self.fontStyle1, bg="#2c343c",fg="white" )
        self.title.place(x=10, y= 10, width=600,height=100)

        # Crear un lienzo para mostrar la imagen
        self.canvas = tk.Canvas(self.tab1, bg='#2c343c')
        self.canvas.place(x=700, y= 40, width=450, height=450)

        # Crear un botón para abrir la ventana de selección de archivo
        self.btn = tk.Button(self.tab1, image=self.img_boton, bg="#2c343c", borderwidth=0, command=self.open_file)
        self.btn.place(x=266, y= 100, width=80,height=40)
        self.labelb1 =  tk.Label(self.tab1, text ="Browse folder here", font=self.fontStyle3, bg="#2c343c",fg="#661ae6" )
        self.labelb1.place(x=210, y= 145, width=200,height=25)
        self.labelb2 =  tk.Label(self.tab1, text ="Suports nii and nii.gz", font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.labelb2.place(x=185, y= 165, width=250,height=25)
        self.labelb3 =  tk.Label(self.tab1, text ="Preprocessing", font=self.fontStyle2, bg="#2c343c",fg="#661ae6" )
        self.labelb3.place(x=30, y= 210, width=250,height=42)

        #Imagen a mostrar
        self.label =  tk.Label(self.tab1, text ="Select an Image: ", font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.label.place(x=30, y= 265, width=180,height=25)
        self.elements = ["No files"]
        self.option_menu = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
        self.option_menu.place(x=295, y= 270)

        #Eje a mostrar 
        self.labelAxis =  tk.Label(self.tab1, text ="Select the axis to move: ",  font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.labelAxis.place(x=40, y= 313, width=220,height=50)
        self.axis = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected2)
        self.axis.place(x=295, y= 323)

        #Estandarización a aplicar
        self.labelstandarization =  tk.Label(self.tab1, text ="Select a standarization: ",  font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.labelstandarization.place(x=40, y= 368, width=220,height=50)
        self.standarization = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected2)
        self.standarization.place(x=295, y= 376)

        #Remocion de ruido a aplicar
        self.labeldenoising =  tk.Label(self.tab1, text ="Select a denosing method:",  font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.labeldenoising.place(x=40, y= 423, width=230,height=50)
        self.denoising = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected2)
        self.denoising.place(x=295, y= 430)
        
        self.histogram=ctk.CTkButton(self.tab1, height=40, font=("Lucida Grande", 15), text="Histogram",text_color='#a7a1a5',fg_color='#661ae6')
        self.histogram.place(x=100, y=500)
        self.image=ctk.CTkButton(self.tab1, height=40, font=("Lucida Grande", 15),text="Image",text_color='#a7a1a5',fg_color='#661ae6')
        self.image.place(x=300, y=500)

    #Funciones auxiliares 
    def open_file(self):
        # Obtener las rutas de los archivos seleccionados
        self.file_paths = filedialog.askopenfilenames()
        count=0
        # Procesar cada archivo
        for file_path in self.file_paths:
            # Verificar que el archivo tenga la extensión ".nii" o ".nii.gz"
            if os.path.splitext(file_path)[1] not in [".nii", ".gz"]:
                messagebox.showwarning(message="An image has not been uploaded", title="WARNINGN")
                continue
            else: 
                count+=1
            # Guardar la imagen en la carpeta deseada utilizando shutil
            new_file_path = "MRI/patient/" + os.path.basename(file_path)
            shutil.copy(file_path, new_file_path)
        if count>0:
            messagebox.showinfo(message="Files uploades successfully", title="")
        
        self.updateOptionmenu()
        
    def updateOptionmenu(self):
         # Obtener lista de archivos y subdirectorios en la carpeta
        self.elements = os.listdir("MRI/patient/")

        global elementssss
        elementssss = os.listdir("MRI/patient/")
        if not self.elements:
           
             self.option_menu = ctk.CTkComboBox(self.tab1,
                                     values=self.elements,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
             self.option_menu.place(x=295, y= 270)

        else:
            self.option_menu = ctk.CTkComboBox(self.tab1,
                                     values=self.elements,
                                     width=220,height=35, state='readonly',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected)
            self.option_menu.place(x=295, y= 270 )
            

    def update_combox(self):
        self.axis = ctk.CTkComboBox(self.tab1,
                                        values=['Axis x','Axis y','Axis z'],
                                        width=220,height=35, state='readonly',
                                        fg_color="#2c343c",border_color="#661ae6", command=self.display_selected2)
        self.axis.place(x=295, y= 323)

        self.standarization = ctk.CTkComboBox(self.tab1,
                                    values=['Rescaling','Z-score','White Stripe', 'Histogram matching'],
                                    width=220,height=35, state='readonly',
                                    fg_color="#2c343c",border_color="#661ae6", command=self.display_selected2)
        self.standarization.place(x=295, y= 376)

        self.denoising = ctk.CTkComboBox(self.tab1,
                                    values=['Mean filter','Median filter','Filter with borders'],
                                    width=220,height=35, state='readonly',
                                    fg_color="#2c343c",border_color="#661ae6", command=self.display_selected2)
        self.denoising.place(x=295, y= 430)

    def display_selected(self, *args):
        self.path_imagen="MRI/patient/"+self.option_menu.get()
        self.update_combox()
        self.init_plot()


    def display_selected2(self, *args):
        if self.axis.get()=='Axis x' and self.path_imagen!="" :
            self.size = (self.data.shape[0])-1
        elif self.axis.get()=='Axis y' and self.path_imagen!="" :
            self.size = (self.data.shape[1])-1
        elif self.axis.get()=='Axis z' and self.path_imagen!="":
            self.size = (self.data.shape[2])-1
        else:
            self.size=10
        self.barra_valores = ctk.CTkSlider(self.tab1, from_=0, to=self.size, width=450,button_color="#661ae6",
                                         button_hover_color="white",fg_color="white",progress_color="white",command=self.visualize) 
    
        self.barra_valores.place(x=700, y= 500)
        

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
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().place( x=0, y=0,width=450, height=450)
        

    def visualize (self,*args):
        
        if self.path_imagen!="":
            self.canvas.delete("all")

            # Mostrar la imagen en el plot
            value=int(self.barra_valores.get())
            print(value)
            if self.axis.get()=='Axis x':
                self.ax.imshow(self.data[value,:,:])
            elif self.axis.get()=='Axis y':
                self.ax.imshow(self.data[:,value,:])
            elif self.axis.get()=='Axis z':
                self.ax.imshow(self.data[:,:,value])
            else:
                self.ax.imshow(self.data[:,:,5])

            # Convertir la figura en un widget de Tkinter y mostrarla en el canvas
            self.canvas_widget.draw()
        else:
            messagebox.showwarning(message="An image has not been uploaded", title="WARNINGN")
       