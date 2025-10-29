from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys
import os

class Inventario(tk.Frame):
    db_name = "database_mercadito.db"  #--ruta donde esta ubicada la base de datos
    
    
    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.conn = sqlite3.connect(self.db_name) #--conectamos la base de datos
        self.cursor = self.conn.cursor()
        self.widgets()
      #---si tengo imagenes en botones---habilitamos o no!!---  
    #def rutas(self,ruta):
    #    try:
    #        rutabase=sys._MEIPASS  #--ME VA A BUSCAR LOS ARCHIVOS imagenes etc
     #   except Exception:
    #        rutabase = os.path.abspath(".")
     #   return os.path.join(rutabase,ruta)    
        
    def widgets(self):
          #---frame 1 contiene el cuadro donde tenemos la palabra inventarios----
        frame1 = tk.Frame(self, bg="#dddddd",highlightbackground="gray", highlightthickness=2)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100) 
        
        titulo = tk.Label(self, text="INVENTARIOS", bg="#dddddd", font="sans 30 bold",anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
         #---en este sector estaran todos los widgets que estaran en la parte inferior de la pantalla----
        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        #labelframe va contener varios elementos
        labelframe = LabelFrame(frame2, text="Producto", bg="#C6D9E3", font= "sans 16 bold")
        labelframe.place(x=20, y=30, width=400, height=500)
        #label para registrar productos---dentro del labelframe de arriba--
        lblnombre = Label(labelframe, text="Nombre: ", bg="#C6D9E3", font="sans 12 bold")
        lblnombre.place(x=10, y=20)
        #variable para llamarlo fuera de widgets y no genere problemas
        self.nombre = ttk.Entry(labelframe, font="sans 14 bold")
        self.nombre.place(x=140,y=20,width=240,height=40)
        #---lbl para registrar al proveedor---
        lblproveedor = Label(labelframe,text="proveedor",bg="#C6D9E3", font="sans 12 bold")
        lblproveedor.place(x=10,y=80)
        self.proveedor = ttk.Entry(labelframe, font="sans 14 bold")
        self.proveedor.place(x=140,y=80,width=240,height=40)
        #--creamos variable precio--
        lblprecio = Label(labelframe,text="Precio",bg="#C6D9E3", font="sans 12 bold")
        lblprecio.place(x=10,y=140)
        self.precio = ttk.Entry(labelframe,font="sans 14 bold")
        self.precio.place(x=140,y=140,width=240,height=40)
        #---label costo--
        lblcosto = Label(labelframe,text="Costo",bg="#C6D9E3", font="sans 12 bold")
        lblcosto.place(x=10,y=200)
        self.costo = ttk.Entry(labelframe,font="sans 14 bold")
        self.costo.place(x=140,y=200,width=240,height=40)              
        #---label stock----control existencia--
        lblstock = Label(labelframe,text="Stock",bg="#C6D9E3", font="sans 12 bold")
        lblstock.place(x=10,y=260)
        self.stock = ttk.Entry(labelframe,font="sans 14 bold")
        self.stock.place(x=140,y=260,width=240,height=40)
        #--botones----                                                                         #-con command relacionamos la funcion al boton               
        boton_agregar = tk.Button(labelframe,text="Ingresar",font="sans 14 bold",bg="#dddddd",command=self.registrar) # en este caso registrar
        boton_agregar.place(x=80,y=340,width=240,height=40)
        
        boton_editar = tk.Button(labelframe,text="Editar",font="sans 14 bold",bg="#dddddd",command=self.editar_producto) #en este editar prodcuto
        boton_editar.place(x=80,y=400,width=240,height=40)
        
        #--Tabla--
        treframe = Frame(frame2, bg="white")
        treframe.place(x=440,y=50,width=620,height=400)
        #.--barra desplazamiento dentro de treframe se posiciona con pack no place
        scrol_y = ttk.Scrollbar(treframe)
        scrol_y.pack(side=RIGHT,fill=Y)
        #--barra q por defecto viene vertical, aclaramos HORIZONTAL
        scrol_x = ttk.Scrollbar(treframe, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM,fill=X)
        #--creamos la tabla --  .set para qe se ejecute
        self.tre = ttk.Treeview(treframe, yscrollcommand=scrol_y.set,xscrollcommand=scrol_x.set,height=40,columns=("ID","PRODUCTO","PROVEEDOR", "PRECIO","COSTO","STOCK" ),show="headings")
        self.tre.pack(expand=True,fill=BOTH)
        #---config el scrol---
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)
        #--para que se muetre la tabla---encabezados y culomnas---
        self.tre.heading("ID",text="ID")
        self.tre.heading("PRODUCTO",text="PRODUCTO")
        self.tre.heading("PROVEEDOR",text="PROVEEDOR")
        self.tre.heading("PRECIO",text="PRECIO")
        self.tre.heading("COSTO",text="COSTO")
        self.tre.heading("STOCK",text="STOCK")
        #--COLUMNAS---
        self.tre.column("ID",width=70,anchor="center")
        self.tre.column("PRODUCTO",width=100,anchor="center")
        self.tre.column("PROVEEDOR",width=100,anchor="center")
        self.tre.column("PRECIO",width=100,anchor="center")
        self.tre.column("COSTO",width=100,anchor="center")
        self.tre.column("STOCK",width=70,anchor="center")
        
        self.mostrar() #--con esto llamamos la funcion qe creamos "mostrar" y nos muiestra lo que tenemos en la base de datos 
                                                                      #--con ese boton llamamos la funcion de actualizar--
        btn_actualizar = Button(frame2,text="Actualizar",font="sans 14 bold",command=self.actualizar_inventario) #---si vendo quiero qe se actualice en tiempo real el stock sin cerrar y abrir el programa
        btn_actualizar.place(x=440,y=480,width=260,height=50)
        
        
        
    #--funcion eje consulta permitira realizar las consultas que queramos
    def eje_consulta(self,consulta,parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta,parametros)  #--obtenemos resultado ejecutamos,
            conn.commit()#---esa conexion guarda los cambios    
        return result  #.--nos devuelve los resultados
    #---funcion para validar los datos que se agregan al stock--
    def validacion(self,nombre,prov,precio,costo,stock):
        if not (nombre and prov and precio and costo and stock):
            return False   #--si no hay un nombre prov precio costo o stock, si no estan diligenciados me devolvera falso, no podre proseguir con el registro
        try:  #--requiero qe sean numericos precio costo y stock
            float(precio)
            float(costo)
            int(stock)
        except ValueError:
            return False    #---si esas casillas no son numeros me retornara falso, no podre continuar con el registro
        return True  #---si se registra todo bien, genial me guarda el registro
    
    #--funcion qe permita mostrar en la tabla lo que tenemos registrado en la base de datos    
    def mostrar(self):
        #--creamos variable de consulta---
        consulta = "SELECT * FROM inventario ORDER BY id DESC"
        result = self.eje_consulta(consulta)
        for elem in result: # por caada elemento en el resultado
            try:
                precio_pesos = " {:,.0f}".format(float(elem[3])) if elem[3] else ""#--3 = precio
                costo_pesos = " {:,.0f}".format(float(elem[4])) if elem[4] else ""  #--costo es el elemento = 4
            
            except ValueError:
                precio_pesos = elem[3]
                costo_pesos = elem[4]     #--refiere a la modificacion al ingresar stock
            self.tre.insert("",0,text=elem[0],values=(elem[0],elem[1],elem[2],precio_pesos,costo_pesos,elem[5]))  #--significa qe los elementos que formateamos al ingresar stock son o 1 2      
                
                
    def actualizar_inventario(self):
        for item in self.tre.get_children():
            self.tre.delete(item)  #--me actualiza los item dentro de la tabla
            
        self.mostrar()   #muestra actualizada la lista
        
        messagebox.showinfo(("Actualizacion","El inventario a sido actualizado correctamente"))    
            
    #--vamos a registrar productos en la base de datos-- y tmb al treview para que los muestre--   
    def registrar(self):
        result = self.tre.get_children()
        for i in result:
            self.tre.delete(i) 
        nombre = self.nombre.get()
        prov = self.proveedor.get()  #--get es para que reciba los datos que recibimos en los entry arriba  
        precio = self.precio.get()
        costo = self.costo.get()
        stock = self.stock.get()
        if self.validacion(nombre,prov,precio,costo,stock):
            try:
                consulta = "INSERT INTO inventario VALUES(?,?,?,?,?,?)"
                parametros = (None,nombre,prov,precio,costo,stock)
                #--se ejecuta la consulta para qe se ingresse en la tabla
                self.eje_consulta(consulta,parametros)
                self.mostrar()
                self.nombre.delete(0,END)  #--una vez se registre, se borra de los entry cad unop de los datos qe se ingresa
                self.proveedor.delete(0,END)
                self.precio.delete(0,END)   #--borramos los datos del entry con esa funcion
                self.costo.delete(0,END)
                self.stock.delete(0,END)
                
            except Exception as e:
                messagebox.showwarning(title="Error",message=f"Error al registrar el producto: {e}")
                
        else:
            messagebox.showwarning(title="Error",message="Rellene todos los campos correctamente")
            self.mostrar()   #cerramos la funcion con mostrar, para ver que casillero nos falta rellenar en el registro
                     
                
                
      #---funcion editar producto--- 
    def editar_producto(self):
        seleccion = self.tre.selection()                               
        if not seleccion:   #--si no se selecciona ninguno no tira mensaje
            messagebox.showwarning("Editar producto","Seleccione un producto para editar.")
            return
    
    #--vamos a obtener los datos del item seleccionado....
        item_id = self.tre.item(seleccion)["text"]
        item_values = self.tre.item(seleccion)["values"]
        #se editan mediante un toplevel--
        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")  #titulo
        ventana_editar.geometry("400x400")   #tamaño
        ventana_editar.config(bg="#C6D9E3")   #fondo
        
        lbl_nombre = Label(ventana_editar,text="Nombre:",font="sans 14 bold",bg="#C6D9E3")
        lbl_nombre.grid(row=0,column=0,padx=10,pady=10)  #posicionamos con metodo grid mas rapido
        entry_nombre = Entry(ventana_editar,font="sans 14 bold")
        entry_nombre.grid(row=0,column=1,padx=10,pady=10)
        entry_nombre.insert(0,item_values[1])
        
        lbl_proveedor = Label(ventana_editar,text="Proveedor:",font="sans 14 bold",bg="#C6D9E3")
        lbl_proveedor.grid(row=1,column=0,padx=10,pady=10)  #posicionamos con metodo grid mas rapido
        entry_proveedor = Entry(ventana_editar,font="sans 14 bold")
        entry_proveedor.grid(row=1,column=1,padx=10,pady=10)
        entry_proveedor.insert(0,item_values[2])
        
        lbl_precio = Label(ventana_editar,text="Precio:",font="sans 14 bold",bg="#C6D9E3")
        lbl_precio.grid(row=2,column=0,padx=10,pady=10)  #posicionamos con metodo grid mas rapido
        entry_precio = Entry(ventana_editar,font="sans 14 bold")
        entry_precio.grid(row=2,column=1,padx=10,pady=10)
        entry_precio.insert(0,item_values[3].split()[0].replace(",",""))  #--reemplaza la coma 
        
        lbl_costo = Label(ventana_editar,text="Costo:",font="sans 14 bold",bg="#C6D9E3")
        lbl_costo.grid(row=3,column=0,padx=10,pady=10)  #posicionamos con metodo grid mas rapido
        entry_costo = Entry(ventana_editar,font="sans 14 bold")
        entry_costo.grid(row=3,column=1,padx=10,pady=10)
        entry_costo.insert(0,item_values[4])
        
        lbl_stock = Label(ventana_editar,text="Stock:",font="sans 14 bold",bg="#C6D9E3")
        lbl_stock.grid(row=4,column=0,padx=10,pady=10)  #posicionamos con metodo grid mas rapido
        entry_stock = Entry(ventana_editar,font="sans 14 bold")
        entry_stock.grid(row=4,column=1,padx=10,pady=10)
        entry_stock.insert(0,item_values[5])
        
        #--creamos funcion guardar cambios
        def guardar_cambios():
            nombre = entry_nombre.get() #--para obtener los datos qe se introduzcan es el GET
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo = entry_precio.get()
            stock = entry_stock.get()
            
            if not (nombre and proveedor and precio and costo and stock):
                messagebox.showwarning("Guardar cambios","Rellene todos los campos")
                return
            
            try:   #--formateamos
                precio  = float(precio.replace(",",""))
                costo = float(costo.replace(",",""))
            except ValueError:
                messagebox.showwarning("Guardar cambios","Ingrese valores numericos validos para precio y costo")
                return
            
            consulta = "UPDATE inventario SET nombre =?, proveedor=?, precio=?, costo=?, stock=? WHERE id=?"
            parametros = (nombre,proveedor,precio,costo,stock,item_id)
            self.eje_consulta(consulta, parametros)
            #--llamamos a la funcion actualizar invent
            self.actualizar_inventario()
            #--ventana editar se destruye una vez actualizado los datos--
            ventana_editar.destroy()
           #--con este boton ejecutamos guardar los cambios-- 
        btn_guardar = Button(ventana_editar,text="Guardar cambios",font="sans 14 bold",command=guardar_cambios)
            #--ese boton se indica qe esta en ventana editar, su texto, su fuente,....etc-----
        
        btn_guardar.place(x=80,y=250,width=240,height=40)  #--posicionamos en la ventana 
                
            
        
        
        