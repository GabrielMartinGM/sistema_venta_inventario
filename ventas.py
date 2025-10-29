from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import letter   #--para usar reportes PDF
from reportlab.pdfgen import canvas   #--reportes PDF
from reportlab.platypus import Table    #tabla---
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  #stilos
import sys
import os #--visualizar pdf en el archivo--
import datetime  #--hora fecha


class Ventas(tk.Frame):
    db_name = "database_mercadito.db" #llama al archivo y conecta
       #---llamamos a las siguientes funciones--
    def __init__(self, parent):
        super().__init__(parent)
        self.numero_factura_actual = self.obtener_numero_factura_actual()
        self.widgets()
        self.mostrar_numero_factura()
        #-----la funcion rutas nos permite transformar de manera correcta a.EXE sin perder imagenes ni q tengamos errores
    def rutas(self,ruta):
        try:
            rutabase=sys._MEIPASS  #--ME VA A BUSCAR LOS ARCHIVOS imagenes etc
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta)    
        
    def widgets(self):
        
        frame1 = tk.Frame(self, bg="#dddddd",highlightbackground="gray", highlightthickness=2)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100) 
        
        titulo = tk.Label(self, text="VENTAS", bg="#dddddd", font="sans 30 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
        
        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        #labelframe va contener varios elementos
        lblframe = LabelFrame(frame2, text="Información de la venta", bg="#C6D9E3", font= "sans 16 bold")
        lblframe.place(x=10, y=10, width=1060, height=80)
        
        label_numero_factura = tk.Label(lblframe, text="Numero de \nfactura", bg="#C6D9E3", font="sans 12 bold")
        label_numero_factura.place(x=10, y=5)
        #variable para el nro de factura
        self.numero_factura = tk.StringVar()
                                                                                             #bloqueado para que solo se puedan ver los prod cargados de la base d dats               
        self.entry_numero_factura = ttk.Entry(lblframe, textvariable=self.numero_factura, state="readonly", font="sans 12 bold")
        self.entry_numero_factura.place(x=100, y=5, width=80) #siempre tenemos q posicionar con place las variables
        
        label_nombre = tk.Label(lblframe, text="Productos:  ",bg="#C6D9E3", font="sans 12 bold")
        label_nombre.place(x=200,y=12)
           #----combobox me despliega una lista para seleccionar un producto registrado y solo leerlo----
        self.entry_nombre = ttk.Combobox(lblframe,font="sans 12 bold",state="readonly")
        self.entry_nombre.place(x=280, y=10, width=180) #width = ancho
        #--lamamos la funcion combobox---y se me cargan los productos registrados en la base de datos
        self.cargar_productos()
        
        
    
        
        label_valor = tk.Label(lblframe, text="Precio: ",bg="#C6D9E3", font="sans 12 bold")
        label_valor.place(x=470,y=12)
        
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold",state="readonly")
        self.entry_valor.place(x=540,y=10,width=180)
        
        #--se carga el precio del producto llamado de la base de datos y actualizamos el precio con dicha funcion
        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_precio)
        
        #llamo al producto, me carga el precio y le indico cuanta cantidad vendere
        label_cantidad = tk.Label(lblframe, text="Cantidad: ",bg="#C6D9E3",font="sans 12 bold")
        label_cantidad.place(x=730,y=12)
        self.entry_cantidad = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x=820,y=10)
        #ubicamos en el marco 2(frame2)
        treFrame = tk.Frame(frame2, bg="#C6D9E3")
        treFrame.place(x=150,y=120,width=800,height=200)
        #barra vertical
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)
        #barra horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM,fill=X)
        #tabla  self.para llamarla desde otras funciones ---- #variable self.tree dentro de treframe                                       #muestra encabezados
        self.tree = ttk.Treeview(treFrame, columns=("Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)
        #config encabezados
        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")
        #config columnas
        self.tree.column("Producto", anchor="center")
        self.tree.column("Precio", anchor="center")
        self.tree.column("Cantidad", anchor="center")
        self.tree.column("Subtotal", anchor="center")
        
        self.tree.pack(expand=True, fill=BOTH)
        
        #-----creamos variable generamos un marco inferior y agregaremos un boton que diga agregar para los productos-----
        lblframe1 = LabelFrame(frame2, text="Opciones",bg="#C6D9E3",font="sans 12 bold")
        lblframe1.place(x=10,y=380,width=1060,height=100)
        #----boton---agregar-----
        boton_agregar = tk.Button(lblframe1,text="Agregar artículo",bg="#dddddd",font="sans 12 bold",command=self.registrar)
        boton_agregar.place(x=50,y=10,width=240,height=50)
        #----boton---pagar-------
        boton_pagar = tk.Button(lblframe1,text="Pagar",bg="#dddddd",font="sans 12 bold",command=self.abrir_ventana_pago)
        boton_pagar.place(x=400,y=10,width=240,height=50)
        #----boton---facturas----
        boton_ver_facturas = tk.Button(lblframe1,text="Ver facturas",bg="#dddddd",font="sans 12 bold",command=self.abrir_ventana_factura)
        boton_ver_facturas.place(x=750,y=10,width=240,height=50)
        #--label q muestra el total de los productos q ingresan a la tabla
        self.label_suma_total = tk.Label(frame2,text="total a pagar: pesos $ 0",bg="#C6D9E3",font="sans 25 bold")
        self.label_suma_total.place(x=360,y=335)
        
    def cargar_productos(self):
        #---usamos bucle para condiciones --- try--
        try:
            conn = sqlite3.connect(self.db_name)
            #--creeamos cursor para que nos cargue la base de datos-    
            c = conn.cursor()
            #---ejecuta la consulta que le hacemos de la base de datos con nombre de inventario
            c.execute("SELECT nombre FROM inventario")
            #---fetchall es para obtener resultados de la consulta realizada 
            productos = c.fetchall()
            self.entry_nombre["values"] = [producto[0] for producto in productos]
            #--si de la base de datos no hay un producto registrado me genera el mensaje de alerta-- 
            if not productos:
                print("No se encontraron productos en la base de datos")
                conn.close()
        except sqlite3.Error as e:
            print("Error al cargar productos desde la base de datos", e)        
        #--creamos funcion para actualizar precio---    
    def actualizar_precio(self,event):
        #creamos variable nva y similar a cargar_productos
        nombre_producto = self.entry_nombre.get()
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio FROM inventario WHERE nombre = ?",(nombre_producto,))   
            precio = c.fetchone()
            if (precio):
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0,tk.END)
                self.entry_valor.insert(0,precio[0])
                self.entry_valor.config(state="readonly")
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0,tk.END)
                self.entry_valor.insert(0,"Precio no disponible") #error sin precio
                self.entry_valor.config(state="readonly")    
        
        except sqlite3.Error as e:
            messagebox.showerror("Error",f"Error al obtener el precio: {e}")   
        #--cierra y finaliza la funcion luego de esa consulta
        finally:
            conn.close()         
            
    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])  # 3 = precio
            total += subtotal
        self.label_suma_total.config(text=f"Total a pagar: ${total:.0f}")
        
    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()
        
        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto,cantidad):
                    messagebox.showerror("Error","Stock insuficiente para el producto seleccionado")
                    return
                precio = float(precio)
                subtotal = cantidad*precio
            #----una vez verificado q haya stock ingrese al treview--   .0f significa sin decimales
                self.tree.insert("","end",values =(producto,f"{precio:.0f}",cantidad,f"{subtotal:.0f}"))
                #--una vez ingresado el producto en la tabla, limpiamos para ingresar el siguiente producto--
                self.entry_nombre.set("") #limpia el comboobox
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0,tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0,tk.END)
                
                self.actualizar_total()
            except ValueError:
                messagebox.showerror("Error","Cantidad o precio no validos")
        else:
            messagebox.showerror("Error","Debe completar todos los campos")  
            #funcion verificar stock----
    def verificar_stock(self,nombre_producto,cantidad):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM inventario WHERE nombre = ?",(nombre_producto,)) #consulta la base de dats
            stock = c.fetchone()
            if stock and stock[0] >= cantidad: #va verificar si hay stock mayor o igual a 0
                return True #acepta que si
            return False #si no hay suficiente stock regresa y genera error--
        except sqlite3.Error as  e:   #messagebox = mensaje
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False
        finally:
            conn.close()
            
    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3]) # 3=subtotal
            total += subtotal
        return total                             
       #--funcion abrir ventana pago----
    def abrir_ventana_pago(self):
        if not self.tree.get_children(): # si no hay productos en la tabla
            messagebox.showerror("Error","no hay articulos para pagar")
            return
        
        ventana_pago = Toplevel(self)
        ventana_pago.title("Realizar pago")  #titulo
        ventana_pago.geometry("400x400") #tamaño
        ventana_pago.config(bg="#C6D9E3")
        ventana_pago.resizable(False,False)  #mantiene el mismo tamaño
        
        label_total = tk.Label(ventana_pago,bg="#C6D9E3",text=f"Total a pagar: pesos ${self.obtener_total():.0f}",font="sans 18 bold") 
        label_total.place(x=70,y=20)
        
        label_cantidad_pagada = tk.Label(ventana_pago,bg="#C6D9E3",text="Cantidad pagada",font="sans 14 bold")
        label_cantidad_pagada.place(x=100,y=90)
        entry_cantidad_pagada = ttk.Entry(ventana_pago,font="sans 14 bold")
        entry_cantidad_pagada.place(x=100,y=130)
        #me muestra el cambio si pagan con mayor valor
        label_cambio = tk.Label(ventana_pago,bg="#C6D9E3",text="",font="sans 14 bold")
        label_cambio.place(x=100,y=190)
        #funcion calcular cambio---
        def calcular_cambio():
            try:  #cantidad pagada - el total
                cantidad_pagada = float(entry_cantidad_pagada.get())
                total = self.obtener_total()
                cambio = cantidad_pagada - total #total resultado ( vuelto)
                if cambio < 0:
                    messagebox.showerror("Error","La cantidad pagada es insuficiente")
                    return
                label_cambio.config(text=f"Vuelto: pesos ${cambio:.0f}")  #cambio se actualiza
            except ValueError:
                messagebox.showerror("Error","Cantidad ñpagada no válida")
                
        #---creamos dos botones---calcular---
        boton_calcular = tk.Button(ventana_pago,text="Calcular vuelto",bg="white",font="sans 12 bold",command=calcular_cambio)
        boton_calcular.place(x=100,y=240,width=240,height=40)
        #---boton pagar----
        boton_pagar = tk.Button(ventana_pago,text="Pagar",bg="white",font="sans 12 bold",command=lambda:self.pagar(ventana_pago,entry_cantidad_pagada,label_cambio))
        boton_pagar.place(x=100,y=300,width=240,height=40)
        
    def pagar(self,ventana_pago,entry_cantidad_pagada,label_cambio):
        try:
            cantidad_pagada = float(entry_cantidad_pagada.get())  #--indicamos que es un nro float y indicamos qe lo vamos a obtener
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio < 0:
                messagebox.showerror("Error","La cantidad pagada es insuficiente")
                return
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            try:  #--los datos qe se obtengan de esa tabla
                productos = []
                for child in self.tree.get_children():
                    item = self.tree.item(child,"values")
                    precio = item[1]
                    producto = item[0]
                    cantidad_vendida = int(item[2])  #--2 = cantidad
                    subtotal = float(item[3])
                    productos.append([producto,precio,cantidad_vendida,subtotal])
                    
                    
                    
                    c.execute("INSERT INTO ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal) VALUES (?,?,?,?,?)",
                              (self.numero_factura_actual, producto,float(precio),cantidad_vendida,subtotal))
                    #--me actualice esa factura
                    c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?",(cantidad_vendida,producto))
                    # --cerramos consultas y se termina de registrar la venta
                conn.commit() #--se guarda en la tabla
                messagebox.showinfo("Exito","Venta registrada exitosamente")
                    
                    #--crearemos dos funciones con las q indicaremos que se incremente el nro de factura de a uno en uno--
                self.numero_factura_actual += 1
                self.mostrar_numero_factura()
                    
                for child in self.tree.get_children():
                    self.tree.delete(child)  #--cuando se guarde la factura la tabla qeda en blanco para generar nueva venta
                self.label_suma_total.config(text="Total a pagar; pesos $0")
                    
                ventana_pago.destroy()   #--cierra la ventana
                
                fecha = datetime.datetime.now().strftime("%y-%m-&d %H:%M:%S")  #---fecha actual
                
                #--realizamos el llamado de la factura una vez realizada el pago--
                self.generar_factura_pfd(productos,total,self.numero_factura_actual -1, fecha)
                    
            except sqlite3.Error as e:
                conn.rollback()  #--variable revierte la transaccion en caso de error y no se guarde nro de factura asi no molesta en la prox factura
                messagebox.showerror("Error",f"Error al registrar la venta: {e}") 
            finally:
                conn.close()
                
        except ValueError:  #--cerramos un TRY mas arriba 
            messagebox.showerror("Error","Cantidad pagada no válida")
    #--funcion PDF con sus parametros--creamos la ruta
    def generar_factura_pfd(self,productos,total,factura_numero,fecha):
        archivo_pdf = f"facturas/factura_{factura_numero}.pdf"  #este va ser el nombre del archivo qe se va generar
        #--configuramos lienzo
        c = canvas.Canvas(archivo_pdf,pagesize=letter)
        width, height = letter
        
        styles = getSampleStyleSheet()
        estilo_titulo = styles["Title"]
        estilo_normal = styles["Normal"]
        
        c.setFont("Helvetica-Bold",16)
        c.drawString(100,height - 50,f"Factura#{factura_numero}")
        
        c.setFont("Helvetica-Bold",12)
        c.drawString(100,height - 70,f"Frcha: {fecha}")
        
        c.setFont("Helvetica-Bold",12)
        c.drawString(100,height - 100,"Informacion de la venta")
        #--creamos la tabla qe va encapsular los datos de la lista arriba--
        data = [["Producto","Precio","Cantidad","Subtotal"]] + productos #variable qe creamos en los pagos"productos
        table = Table(data) #los productos q creamos arriba van a estar en esta tabla, se lo indicamos asi
        table.wrapOn(c,width,height) #-wrapon ajusta la tabla al tamaño del canvas
        table.drawOn(c,100,height - 200)
        #--necesito qe me muestre la faqctura con total
        c.setFont("Helvetica-Bold",16)
        c.drawString(100,height - 250,f"Total a pagar: pesos{total:.0f}")
        #--mensaje qe diga: gracias por la venta o algo similar
        c.setFont("Helvetica-Bold",12)
        c.drawString(100,height - 400,"Gracias por su compra, vuelva pronto <3")
        
        #--metodo save para guardar esa factura en el PFD qe se genera en la carpeta facturas con su nro correspondiente
        c.save()
        messagebox.showinfo("Factura generada",f"La factura #{factura_numero} ha sido creada exitosamente!!")
        
        #--usamos el OS para qe esa factua guardada me la muestre automaticamente en el sistema
        os.startfile(os.path.abspath(archivo_pdf)) #--con la ruta del archivo
        
            
    def obtener_numero_factura_actual(self):
       #recibimos el dato de la base de datos asi que nos conectamos---
        conn = sqlite3.connect(self.db_name)   
        c = conn.cursor()
        try:
            c.execute("SELECT MAX(factura) FROM ventas")  #--realiza la consulta
            max_factura = c.fetchone()[0]
            if max_factura:
                return max_factura +1  # si es 10 la ultima, se suma 1 y la prox seria la 11
            else: 
                return 1  # --si no hay facturas regresa 1. seria la 1ra de todas las facturas ya que estara vacia la base
        except sqlite3.Error as e:
            messagebox.showerror("Error",f"Error al obtener el numero de factura: {e}")
            return 1
        finally:
            conn.close()  #cerramos conexion----
            
    def mostrar_numero_factura(self):
        self.numero_factura.set(self.numero_factura_actual) #funcion para qe nos muetre con set el nro
                
    #--funcion abrir ventana facturas---
    def abrir_ventana_factura(self):  #--sin self no me mostraba facturas emitidas
        ventana_facturas = Toplevel(self)
        ventana_facturas.title("Factura")
        ventana_facturas.geometry("800x500")
        ventana_facturas.config(bg="#C6D9E3")
        ventana_facturas.resizable(False,False)
        #  ---tipo label, esta en ventana facturas,bg,text, etc
        facturas = Label(ventana_facturas, bg="#C6D9E3",text="facturas registradas",font="sans 36 bold") 
        facturas.place(x=150,y=15)
        
        #treframe donde vamos a almacenar la tabla del treview q vamos a crear--
        treFrame = tk.Frame(ventana_facturas,bg="#C6D9E3")
        treFrame.place(x=10,y=100,width=780,height=380)
        
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)
        #barra horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM,fill=X)
        #tabla  self.para llamarla desde otras funciones ---- #variable self.tree dentro de treframe                                       #muestra encabezados
        tree_facturas = ttk.Treeview(treFrame, columns=("ID", "Factura", "Producto", "Precio","Cantidad","Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=tree_facturas.yview)
        scrol_x.config(command=tree_facturas.xview)
        
        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#4", text="Cantidad")
        tree_facturas.heading("#4", text="Subtotal")
        
        
        #config columnas
        tree_facturas.column("ID", anchor="center")
        tree_facturas.column("Factura", anchor="center")
        tree_facturas.column("Producto", anchor="center")
        tree_facturas.column("Precio", anchor="center")
        tree_facturas.column("Cantidad", anchor="center")
        tree_facturas.column("Subtotal", anchor="center")
        
        tree_facturas.pack(expand=True,fill=BOTH)
        
        self.cargar_facturas(tree_facturas)
        
    def cargar_facturas(self, tree):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            facturas = c.fetchall() #--fetchall es para obtener todos los datos que se hacen en la consulta arriba   
            for factura in facturas:
                tree.insert("","end",values=factura)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error",f"Error al cargar las facturas: {e}")     
        
              
            
                              
           
                    
                
        
        
                        