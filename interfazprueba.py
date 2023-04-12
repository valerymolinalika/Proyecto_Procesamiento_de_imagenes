from tkinter.font import Font
from tkinter import ttk,messagebox
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from segmentation import segmentation

class interfaz():
    def __init__(self):
        # Creacion de la ventana
        self.ventana =  tk.Tk()
        self.ventana.geometry("1200x610")
        self.ventana.configure(bg='#00415d')
        self.path_imagen=""
        self.size=10
        
        # Crear un widget Notebook con dos pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña 1: Interfaz de usuario
        self.tab1 = tk.Frame(self.notebook,bg='#00415d')
        self.notebook.add(self.tab1, text='Upload Image')

        self.tab2 = tk.Frame(self.notebook, bg='#00415d')
        self.notebook.add(self.tab2, text='More Information')
        
        # Cargar fuentes e imagenes
        img_boton = tk.PhotoImage(file="images\_folder.png")
        self.img_boton2 = tk.PhotoImage(file="images\_ok.png")
        self.fontStyle1 = Font(family="Tw Cen MT", size=35, weight="bold", slant="roman", underline=0, overstrike=0)
        self.fontStyle2 = Font(family="Lucida Grande", size=25)
        self.fontStyle3 = Font(family="Lucida Grande", size=20)

        # Crear un lienzo para mostrar la imagen
        self.canvas = tk.Canvas(self.ventana, bg='#00415d')
        self.canvas.place(x=700, y= 60, width=450, height=450)

        # Titulo de la app
        self.title =  tk.Label(self.tab1, text ="UPLOAD YOUR IMAGE", font=self.fontStyle1, bg="#00415d",fg="white" )
        self.title.place(x=10, y= 10, width=680,height=100)

        # Crear un botón para abrir la ventana de selección de archivo
        self.btn = tk.Button(self.tab1, image=img_boton, bg="#00415d", borderwidth=0, command=self.open_file)
        self.btn.place(x=300, y= 140, width=80,height=50)
        self.label1 =  tk.Label(self.tab1, text ="Select your image:", font=self.fontStyle2, bg="#00415d",fg="white" )
        self.label1.place(x=10, y= 110, width=300,height=100)

        # Controles
        self.variable =  tk.StringVar()
        self.variable.set("Select") # default value
        self.labelAxis =  tk.Label(self.tab1, text ="Select the axis to move: ", font=self.fontStyle2, bg="#00415d",fg="white" )
        self.labelAxis.place(x=10, y= 200, width=375,height=50)
        self.w =  tk.OptionMenu(self.tab1, self.variable, 'Axis x','Axis y','Axis z',command=self.display_selected2)
        self.w.place(x=480, y= 210, width=150,height=40)
        print (self.variable.get())

        self.segmentation_method =  tk.StringVar()
        self.segmentation_method.set("Select") # default value
        self.labelMethod =  tk.Label(self.tab1, text ="Select segmentation method: ", font=self.fontStyle2, bg="#00415d",fg="white" )
        self.labelMethod.place(x=10, y= 255, width=450,height=50)
       
        self.a =  tk.OptionMenu(self.tab1, self.segmentation_method, "Original","Thresholding", "Region growing", "Clustering", command=self.display_selected)
        self.a.place(x=480, y= 260, width=150,height=40)

        self.ventana.mainloop()

    #Funciones auxiliares 
    def callfunction(self,method):
        if method=="1":
            self.data = self.img.get_fdata()
            self.data=segmentation.tresholding(self.data, int(self.entry.get()), int(self.entry2.get()))
            self.visualize()
        elif method=="3":
            self.data = self.img.get_fdata()
            self.data=segmentation.k_means(self.data, int(self.entryk.get()))
            self.visualize()

    def onclick(self,event):
        if self.ax.contains(event)[0]:
            x = int(event.xdata)
            y = int(event.ydata)
        print(f"Coordenada del clic: x={x}, y={y}")

    def display_selected(self, *args):
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

            
        elif self.segmentation_method.get()=='Region growing' and self.path_imagen!="" :
            print("hola, aun no sirve, vuelve pronto")

        elif self.segmentation_method.get()=='Clustering' and self.path_imagen!="":
            self.ks = tk.Label(self.tab1, text ="k's quantity:", font=self.fontStyle3, bg="#00415d",fg="white" )
            self.ks.place(x=50, y= 300, width=150,height=100)
            self.entryk = tk.Entry(justify="center")
            self.entryk.insert(0, "2")
            self.entryk.place(x=60, y=400,width=150,height=40)

            self.btn = tk.Button(self.tab1, image=self.img_boton2, bg="#00415d", borderwidth=0, command= lambda: self.callfunction("3"))
            self.btn.place(x=400, y= 370, width=80,height=50)

    def display_selected2(self, *args):
        if self.variable.get()=='Axis x' and self.path_imagen!="" :
            self.size = (self.data.shape[0])-1
        elif self.variable.get()=='Axis y' and self.path_imagen!="" :
            self.size = (self.data.shape[1])-1
        elif self.variable.get()=='Axis z' and self.path_imagen!="":
            self.size = (self.data.shape[2])-1
        else:
            self.size=10
        self.barra_valores = tk.Scale(self.tab1, label=self.variable.get(),from_=0, to=self.size, orient='horizontal', bg="#00415d",fg="white",command=self.visualize)
        self.barra_valores.place(x=700, y= 500, width=450,height=70)
        
    def open_file(self):
        # Obtener la ruta del archivo seleccionado
        self.file_path = filedialog.askopenfilename()
        self.path_imagen=self.file_path
        # Cargar la imagen nii utilizando nibabel
        self.img = nib.load(self.path_imagen)
        self.data = self.img.get_fdata()
        self.init_plot()

    
    def init_plot(self):
        
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
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def visualize (self,*args):
        
        if self.path_imagen!="":
            self.canvas.delete("all")

            # Mostrar la imagen en el plot
            
            if self.variable.get()=='Axis x':
                self.ax.imshow(self.data[self.barra_valores.get(),:,:])
            elif self.variable.get()=='Axis y':
                self.ax.imshow(self.data[:,self.barra_valores.get(),:])
            elif self.variable.get()=='Axis z':
                self.ax.imshow(self.data[:,:,self.barra_valores.get()])
            else:
                self.ax.imshow(self.data[:,:,5])

            # Convertir la figura en un widget de Tkinter y mostrarla en el canvas
            self.canvas_widget.draw()
        else:
            messagebox.showwarning(message="An image has not been uploaded", title="WARNINGN")



mi_interfaz = interfaz()
