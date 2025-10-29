from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from PIL import Image, ImageTk
import sys
import os

#prueba a corregir d boton !!!!!!!!------------
#btninventario = Button( bg="blue", fg="white", text="Ir a Inventario")
#btninventario.place(x=500, y=130, width=240, height=60) 
#btninventario.mainloop()

#btnventas = Button( bg="green", fg="black", text="Ir a Ventas")
#btnventas.place(x=500, y=30, width=240, height=60)
#btnventas.mainloop()
class Container(tk.Frame):

    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack() #empaquetamos
        self.place(x=0, y=0, width=800, height=400)
        self.config(bg="#C6D9E3")
        self.widgets() #llamamos los widgets asi se ejecuta el programa
        
    
        # --------------------------

        self.widgets()  # Llamamos a los widgets


    
    
    def rutas(self,ruta):
        try:
            rutabase=sys._MEIPASS  #--ME VA A BUSCAR LOS ARCHIVOS imagenes etc
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta) #--va retornar e ingresar a esa carpeta    
        
        
        
        
       #vamos a crear una funcion q muestre las distintas ventanas que quiero para el proyecto
    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#C6D9E3")
        frame.pack(fill="both", expand=True)
        top_level.geometry("1100x650+120+20") #tamaño y posicion
        top_level.resizable(False, False)  #retraer la pantalla, con false no lo permite
        #---me coloca el ICONO en todas las interfaces-----
        ruta = self.rutas(r"icono_gm.ico")  #--dentro de la funcion ruta me busca el archivo icono
        #---colocamos el icono de la aplicacion---
        top_level.iconbitmap(ruta) #--llamamos a top_level<<<
        
        #---con esto corregimos que la ventana inicial se interponga siempre a la de ventas o inventarios----
        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()
        top_level.lift()
        
        
        
        #clases venta e inventario, se crea y se exportan los arch ventas e inv.
    
    
    
    def ventas(self):
        self.show_frames(Ventas)
        

    def inventario(self):
        self.show_frames(Inventario)
        #creamos botones q llaman a las funciones ventas invent
    def widgets(self): #interfaz grafica del proyecto
        
        frame1 = tk.Frame(self, bg="#C6D9E3")
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)
        
        ruta=self.rutas(r"imagenes/btn_ventas.png") #---me crea la ruta--
        #-vamos a colocar imagen en el boton
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((50,50)) #con resize configuramos lel tamaño para que no se expanda
        imagen_tk = ImageTk.PhotoImage(imagen_resize) #--se redirecciona la imagen--
    
                                              #fg= color de la letra / command significa q cada vez q presionen ese boton nos lleva a ventas y eso los lleva a la carp Ventas
        btnventas = Button(frame1, bg="#334A8A", fg="white",font="sans 18 bold", text="Ir a Ventas", command=self.ventas)
        btnventas.config(image=imagen_tk, compound=LEFT,padx=50) #--configuramos e ubicamos con compound la imagen a la izq del texto --padx es para el espaciado vertical
        btnventas.image = imagen_tk
        btnventas.place(x=500, y=30, width=240, height=60)
        
        
        ruta=self.rutas(r"imagenes/inventory.png") #---me crea la ruta--
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((50,50)) #con resize configuramos lel tamaño para que no se expanda
        imagen_tk = ImageTk.PhotoImage(imagen_resize) #--se redirecciona la imagen--
    
        
        
        btninventario = Button(frame1, bg="#334A8A", fg="white",font="sans 18 bold", text="Ir a Inventario", command=self.inventario)
        btninventario.config(image=imagen_tk, compound=LEFT,padx=10) #--configuramos e ubicamos con compound la imagen a la izq del texto --padx es para el espaciado vertical
        btninventario.image = imagen_tk                    #Padx es para dar distancia entre imagn y texto del botn
        
        btninventario.place(x=500, y=130, width=240, height=60) #cambiamos el boton de Y asi no nos queda superpuesto
        
        ruta=self.rutas(r"imagenes/icono_gm.png") #---me crea la ruta--
        self.logo_image = Image.open(ruta) #--.open indica qe abrimos la imagen
        self.logo_image = self.logo_image.resize((280,280)) #config el tamaño de la imagen--
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image=self.logo_image, bg="#C6D9E3")
        self.logo_label.place(x=100, y=30)
        
        copyright_label = tk.Label(frame1, text="Copyright 2025 GM Tech. Todos los derechos reservados", font="sans 12 bold", bg="#C6D9E3", fg="black")
        copyright_label.place(x=182, y=350)
        