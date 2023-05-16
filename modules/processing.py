from tkinter.font import Font
from tkinter import ttk,messagebox
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms.segmentation import segmentation
from algorithms.denoise import denoise
from algorithms.borders import borders
import shutil
import os


class processing():
    def __init__(self, window, tab):
        
        self.tab1=tab
        self.ventana=window

        self.entry= None
        self.entry2=None
        self.entry3=None
        self.entry4=None
        self.clicked_point=None

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
        self.label.place(x=25, y= 122, width=170,height=25)
        self.option_menu = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
        self.option_menu.place(x=320, y= 120)
        self.btn = tk.Button(self.tab1, image=self.img_boton, bg="#2c343c", borderwidth=0, command=self.updateOptionmenu)
        self.btn.place(x=560, y= 117, width=40,height=40)

         #Eje a mostrar 
        self.labelAxis =  tk.Label(self.tab1, text ="Select the axis to move:",  font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.labelAxis.place(x=10, y= 178, width=250,height=25)
        self.axis = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected3)
        self.axis.place(x=320, y= 175)

        self.labelMethod =  tk.Label(self.tab1, text ="Select segmentation method: ", font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
        self.labelMethod.place(x=25, y= 235, width=270,height=25)
        self.segmentation_method = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
        self.segmentation_method.place(x=320, y= 230) 

        self.image=ctk.CTkButton(self.tab1, height=40, font=("Lucida Grande", 15),text="Borders detection ",text_color='#a7a1a5',fg_color='#661ae6',command= self.bordersbutton)
        self.image.place(x=210, y=400)

        


    def updateOptionmenu(self):
         # Obtener lista de archivos y subdirectorios en la carpeta
        self.elements = os.listdir("MRI/patient/")
        if not self.elements:
           
            self.option_menu = ctk.CTkComboBox(self.tab1,
                                     width=220,height=35, state='disabled',
                                     fg_color="#2c343c",border_color="#661ae6")
            self.option_menu.place(x=320, y= 120)

        else:
            self.option_menu = ctk.CTkComboBox(self.tab1,
                                     values=self.elements,
                                     width=220,height=35, state='readonly',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected)
            self.option_menu.place(x=320, y= 120)
        
            
        
    def display_selected(self, *args):
        self.path_imagen="MRI/patient/"+self.option_menu.get()
        self.init_plot()
        self.update_combox()

    def init_plot(self):
        self.img = nib.load(self.path_imagen)
        self.data = self.img.get_fdata()
        # Mostrar la imagen en un lienzo
        self.canvas.delete("all")
        
        # Crear una figura y un objeto de plot       
        self.fig, self.ax= plt.subplots()
        # Mostrar la imagen en el plot
        self.ax.imshow(self.data[:,:,15])
        self.ax.set_aspect('auto', adjustable='box')
            
        #    Convertir la figura en un widget de Tkinter y mostrarla en el canvas
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().place( x=0, y=0,width=450, height=450)
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
    
    def display_selected2(self, *args):
        if self.segmentation_method.get()=='Thresholding':

            if self.entry is not None:
                self.entry.destroy()
            if self.entry2 is not None:
                self.entry2.destroy()
            if self.entry3 is not None:
                self.entry3.destroy()
            if self.entry4 is not None:
                self.entry4.destroy()
            
            self.entry = ctk.CTkEntry(self.tab1, placeholder_text="Tau", height=32 ,font =("Lucida Grande",15),border_color="#661ae6")
            self.entry.place(x=110, y=320)

            self.entry2 = ctk.CTkEntry(self.tab1, placeholder_text="Tolerance", height=32 ,font =("Lucida Grande",15),border_color="#661ae6")
            self.entry2.place(x=290, y=320)

            self.btn = tk.Button(self.tab1, image=self.img_boton2, bg="#2c343c", borderwidth=0, command= lambda: self.callfunction("1"))
            self.btn.place(x=500, y= 310, width=80,height=50)

        if self.segmentation_method.get()=='Region growing':

            if self.entry is not None:
                self.entry.destroy()
            if self.entry2 is not None:
                self.entry2.destroy()
            if self.entry3 is not None:
                self.entry3.destroy()
            if self.entry4 is not None:
                self.entry4.destroy()
            
            self.entry = ctk.CTkEntry(self.tab1, placeholder_text="Tolerance", width=80, height=32 ,font =("Lucida Grande",15),border_color="#661ae6")
            self.entry.place(x=80, y=320)

            self.entry2 = ctk.CTkEntry(self.tab1, placeholder_text="X", width=80, height=32 ,font =("Lucida Grande",15),border_color="#661ae6")
            self.entry2.place(x=170, y=320)

            self.entry3 = ctk.CTkEntry(self.tab1, placeholder_text="Y", width=80, height=32 ,font =("Lucida Grande",15),border_color="#661ae6")
            self.entry3.place(x=260, y=320)

            self.entry4 = ctk.CTkEntry(self.tab1, placeholder_text="Z", width=80, height=32 ,font =("Lucida Grande",15),border_color="#661ae6")
            self.entry4.place(x=350, y=320)

            self.btn = tk.Button(self.tab1, image=self.img_boton2, bg="#2c343c", borderwidth=0, command= lambda: self.callfunction("2"))
            self.btn.place(x=500, y= 310, width=80,height=50)
        
        if self.segmentation_method.get()=='K-means':

            if self.entry is not None:
                self.entry.destroy()
            if self.entry2 is not None:
                self.entry2.destroy()
            if self.entry3 is not None:
                self.entry3.destroy()
            if self.entry4 is not None:
                self.entry4.destroy()
            
            self.entry = ctk.CTkEntry(self.tab1, placeholder_text="K's", height=32 ,font =("Lucida Grande",15),border_color="#661ae6")
            self.entry.place(x=110, y=320)

            self.entry2 = ctk.CTkEntry(self.tab1, placeholder_text="Iterations", height=32 ,font =("Lucida Grande",15),border_color="#661ae6")
            self.entry2.place(x=290, y=320)

            self.btn = tk.Button(self.tab1, image=self.img_boton2, bg="#2c343c", borderwidth=0, command= lambda: self.callfunction("3"))
            self.btn.place(x=500, y= 310, width=80,height=50)

        
        if self.segmentation_method.get()=='Gaussian mixture':

            if self.entry is not None:
                self.entry.destroy()
            if self.entry2 is not None:
                self.entry2.destroy()
            if self.entry3 is not None:
                self.entry3.destroy()
            if self.entry4 is not None:
                self.entry4.destroy()
            
            self.entry = tk.Label(self.tab1, text ="No input data required",  font=self.fontStyle3, bg="#2c343c",fg="#a7a1a5" )
            self.entry.place(x=150, y=320, width=250,height=25)
    
            self.btn = tk.Button(self.tab1, image=self.img_boton2, bg="#2c343c", borderwidth=0, command= lambda: self.callfunction("4"))
            self.btn.place(x=500, y= 310, width=80,height=50)


    def display_selected3(self,*args):

        if self.axis.get()=='Axis x' :
            self.size = (self.data.shape[0])-1
        elif self.axis.get()=='Axis y' :
            self.size = (self.data.shape[1])-1
        elif self.axis.get()=='Axis z' :
            self.size = (self.data.shape[2])-1
        else:
            self.size=10
        self.barra_valores = ctk.CTkSlider(self.tab1, from_=0, to=self.size, width=450,button_color="#661ae6",
                                         button_hover_color="white",fg_color="white",progress_color="white",command=self.visualize) 
    
        self.barra_valores.place(x=700, y= 500)

    def update_combox(self):
        self.axis = ctk.CTkComboBox(self.tab1,
                                        values=['Axis x','Axis y','Axis z'],
                                        width=220,height=35, state='readonly',
                                        fg_color="#2c343c",border_color="#661ae6", command=self.display_selected3)
        self.axis.place(x=320, y= 175)

        self.segmentation_method = ctk.CTkComboBox(self.tab1,
                                     values=['Thresholding','Region growing', 'K-means', 'Gaussian mixture'],
                                     width=220,height=35, state='readonly',
                                     fg_color="#2c343c",border_color="#661ae6", command=self.display_selected2)
        self.segmentation_method.place(x=320, y= 230) 

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
            
            self.ax.set_aspect('auto', adjustable='box')
            # Convertir la figura en un widget de Tkinter y mostrarla en el canvas
            self.canvas_widget.draw()
        else:
            messagebox.showwarning(message="An image has not been uploaded", title="WARNINGN")

    def callfunction(self,method):
        if method=="1":
            self.data = self.img.get_fdata()
            self.data=segmentation.tresholding(self.data, float(self.entry.get()), int(self.entry2.get()))
            self.visualize()
        
        elif method=="2":
            self.data = self.img.get_fdata()
            self.data=denoise.median_filter(self.data)
            self.data=segmentation.growing(self.data, int(self.entry.get()), int(self.entry2.get()),int(self.entry3.get()),int(self.entry4.get()))
            
            if self.clicked_point is not None:
                self.clicked_point.remove()

            self.visualize()
           
        elif method=="3":
            self.data = self.img.get_fdata()
            self.data=denoise.median_filter(self.data)
            self.data=segmentation.k_means(self.data, int(self.entry.get()), int(self.entry2.get()))
            self.visualize()

        elif method=="4":
            self.data = self.img.get_fdata()
            self.data=denoise.median_filter(self.data)
            self.data=segmentation.GMM(self.data)
            self.visualize()
    
    def bordersbutton(self):
        self.data=borders.border_magnitude(self.data) 

    def onclick(self,event):
        if self.clicked_point is not None:
            self.clicked_point.remove()

        x, y = event.xdata, event.ydata
        if self.ax.contains(event)[0] and self.segmentation_method.get()=='Region growing':
            if self.axis.get()=='Axis x':

                self.entry2.delete(0,5)
                self.entry2.insert(0, int(self.barra_valores.get()))

                self.entry3.delete(0,5)
                self.entry3.insert(0, int(event.ydata))

                self.entry4.delete(0,5)
                self.entry4.insert(0, int(event.xdata))

            elif self.axis.get()=='Axis y':
                self.entry2.delete(0,5)
                self.entry2.insert(0, int(event.ydata))

                self.entry3.delete(0,5)
                self.entry3.insert(0, int(self.barra_valores.get()))

                self.entry4.delete(0,5)
                self.entry4.insert(0, int(event.xdata))
        
            elif self.axis.get()=='Axis z':
            
                self.entry2.delete(0,5)
                self.entry2.insert(0, int(event.xdata))

                self.entry3.delete(0,5)
                self.entry3.insert(0, int(event.ydata))

                self.entry4.delete(0,5)
                self.entry4.insert(0, int(self.barra_valores.get()))

            self.clicked_point=self.ax.scatter(x, y, c='r')  

        self.canvas_widget.draw()
        print(f"Coordenada del clic: x={x}, y={y}")
            