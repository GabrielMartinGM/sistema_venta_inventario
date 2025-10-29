from tkinter import Tk, Frame
from container import Container #las clases van con Mayuscuka, los archivos en minuscula
from ttkthemes import ThemedStyle #darle estilo a los widgets con un diseño elegido
import sys
import os


class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Caja registradora version 1.0")
        self.resizable(False, False)
        self.configure(bg="#122835")
        self.geometry("800x400+120+20") #tamaño de ventanaa
        ruta = self.rutas(r"icono_gm.ico")  #--dentro de la funcion ruta me busca el archivo icono
        #---colocamos el icono de la aplicacion---
        self.iconbitmap(ruta)  #--no me encuentra la ruta sino hubieramos creado la variable ruta--
        
        self.set_theme()  # 👈 MOVIDO ARRIBA (antes de Container) 
        
        self.container = Frame(self, bg="#C6D9E3")
        self.container.pack(fill="both", expand=True)
        
        #self.container.grid_rowconfigure(0, weight=1)  #-----
        #self.container.grid_columnconfigure(0, weight=1) #-----
        
        
        self.frames = {
            Container: None
        }
    
        self.load_frames() #---
        self.show_frame(Container) #-----
        #llamamos la nva funcion para que se aplique el tema
        self.set_theme()
        
        #-----creamos funcion para qe el sistema encuentre las rutas------
    def rutas(self,ruta):
        try:
            rutabase=sys._MEIPASS  #--ME VA A BUSCAR LOS ARCHIVOS imagenes etc
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta) #--va retornar e ingresar a esa carpeta    
                       
    def load_frames(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass]= frame
            #frame.frames[FrameClass] = frame #--
            
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()        
    
    def set_theme(self):
        style = ThemedStyle(self)  #funcion nueva
        style.set_theme("breeze") #diseño que escojemos: brezze que cambia los widgets
                        #se puede cambiar a otro diseño
                        
def main():
    app = Manager()
    app.mainloop()
    
if __name__== "__main__":
    main()
    
    #seejecuta el bucle y el script