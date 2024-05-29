import tkinter as tk
import calculos
import os
import threading
import queue

from os import mkdir
from os.path import join,dirname,realpath

def mostrar_popup(parent):
    global popup
    popup = tk.Toplevel(parent.root)
    popup.title("Cargando")
    label = tk.Label(popup, text="Cargando, por favor espere...")
    label.pack(padx=20, pady=20)
    popup.grab_set()  # Deshabilita otras ventanas mientras se muestra el pop-up
    popup.protocol("WM_DELETE_WINDOW", lambda: None)  # Deshabilita el botón de cerrar

cola = queue.Queue()
def cerrar_popup():
    popup.grab_release()  # Libera la ventana principal
    popup.destroy()  # Destruye el pop-up

def calcgen(starting_location, places_list,q):
    data = calculos.sort_places_by_proximity(starting_location, places_list)
    cerrar_popup()
    q.put(data)
def iniciar_proceso(starting_location, places_list,parent):
    mostrar_popup(parent)
    hilo = threading.Thread(target=calcgen, args=(starting_location, places_list,cola,))
    hilo.start()
    parent.root.after(1000, revisar_cola,parent)

def revisar_cola(parent):
    if cola.empty():
        parent.root.after(1000, revisar_cola,parent)
    else:
        resultado = cola.get_nowait()
        parent.order = resultado
        parent.showres = 1

class ad():
    def __init__(self,parent,title,text):
        self.root= tk.Toplevel(parent.root)
        self.root.resizable(0,1)
        self.root.geometry('240x100')
        self.root.title(title)
        
        self.a1 = tk.Frame(self.root, width=200, height=100)
        self.a1l = tk.Label(self.a1, text=text, anchor="center")
        self.a1l.grid(row=1,column=0, pady=10)
        self.b1 = tk.Button(self.a1, width=3, height=1 ,text='Ok', command= self.root.destroy)
        self.b1.grid(row=3,column=0, sticky='nsew')
        self.a1.pack()
        self.root.transient(parent.root)
        self.root.mainloop()

class savepopup():
    def __init__(self,parent,master):
        self.root= tk.Toplevel(parent.root)
        self.root.resizable(0,0)
        self.root.geometry('240x100')
        self.root.title('Save')
        def check():
            if self.text.get() != '':
                try:
                    mkdir(join(dirname(realpath(__file__)),self.text.get()))
                except:
                    pass

                doc = open(join(join(dirname(realpath(__file__)),self.text.get()),'places.txt'),'w')
                loc = master.order[1]
                t = ''
                for v in loc:
                    try:
                        v0 = int(int(v[0].km)/1000)
                    except:
                        v0 = int(v[0]/1000)
                    t += f'{v0} km , {v[1]}\n'
                doc.write(t)
                doc.close()
                text = calculos.html(master.starting_location,master.order[0])
                loc = open(join(join(dirname(realpath(__file__)),self.text.get()),'map.html'),'w')
                loc.write(text)
                loc.close()

                self.root.destroy()
            else:
                ad(self,'Error', 'Not valid name for saving')
        
        self.a1 = tk.Frame(self.root, width=200, height=100)
        self.a1.pack()
        self.a1l = tk.Label(self.a1, text='Save as:', anchor="center")
        self.a1l.grid(row=1,column=0, pady=5)
        self.text = tk.Entry(self.a1,width=10)
        self.text.grid(row=2,column=0,pady=0)
        self.b1 = tk.Button(self.a1, width=3, height=1 ,text='Save', command= lambda: check())
        self.b1.grid(row=3,column=0, sticky='nsew')
        
        self.root.transient(parent.root)
        self.root.mainloop()
class results():
    def __init__(self,parent):
        
        self.root = tk.Toplevel(parent.root)
        self.root.resizable(0,0)
        self.root.title('Results')
        
        self.a1 = tk.Frame(self.root, width = 220, height = 200)
        self.a1.grid(row=1, column=0, sticky='nsew', pady=10)
        
        def order():
            loc = parent.order[1]
            t = ''
            for v in loc:
                try:
                    v0 = int(int(v[0].km)/1000)
                except:
                    v0 = int(v[0]/1000)
                t += f'{v0} km , {v[1]}\n'
            ad(self,'Order of countries',t)

        def html():
            text = calculos.html(parent.starting_location,parent.order[0])
            loc = open('loc.html','w')
            loc.write(text)
            loc.close()
            os.system('open loc.html')

        def save():
            savepopup(self,parent)

        self.b1 = tk.Button(self.a1, text = 'Order', width=2, padx=5, pady=0, command = lambda: order())
        self.b1.grid(row=0, column=0,rowspan = 2,padx=5, pady=5)
        
        self.b2 = tk.Button(self.a1, text = 'Map', width=6, padx=5, pady=0, command = lambda: html())
        self.b2.grid(row=0, column=1,padx=5, pady=5)
        
        self.b3 = tk.Button(self.a1, text = 'Save', width=6, padx=5, pady=0, command = lambda: save())
        self.b3.grid(row=0, column=2,padx=5, pady=5)
        
        
        self.root.transient(parent.root)
        self.root.mainloop()


class main():
    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Distancias')

        self.order = []
        self.showres = 0

        self.a3 = tk.Frame(self.root)
        self.a3.grid(row=0, column=0, sticky='nsew', pady=0)
        self.a1 = tk.Frame(self.a3)
        self.a1.grid(row=0, column=0, sticky='nsew', pady=10)
        self.a4= tk.Frame(self.a3)
        self.a4.grid(row=0, column=1, rowspan = 2, sticky='nsew')
        self.a2= tk.Frame(self.a3)
        self.a2.grid(row=1, column=0, columnspan = 2, sticky='nsew')
        
        tk.Label(self.a1, text = 'Starting place: ').grid(row=0,column=0, padx=5, pady=5)
        self.sp = tk.Entry(self.a1,  width=15)
        self.sp.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.a2, text = 'Places: ').grid(row=0,column=0, padx=5, pady=5,columnspan=2)
                
        self.a = tk.Entry(self.a2,  width=15)
        self.a.grid(row=1, column=0, padx=5, pady=5)
        self.b = tk.Entry(self.a2,  width=15)
        self.b.grid(row=1, column=1, padx=5, pady=5)
        self.entries = [self.a,self.b]

        self.x = 1
        self.y = 1
        def add():
            if self.y == 0:
                self.y = 1
                locentry = tk.Entry(self.a2,  width=15)
                locentry.grid(row=self.x, column=self.y, padx=5, pady=5)
                self.entries.append(locentry)
            elif self.x < 10:
                self.y = 0
                self.x += 1
                locentry = tk.Entry(self.a2,  width=15)
                locentry.grid(row=self.x, column=self.y, padx=5, pady=5)
                self.entries.append(locentry)
        def remove():
            if [self.x,self.y] != [1,1]:
                if self.y == 0:
                    self.y = 1
                    self.x -= 1
                elif self.y == 1:
                    self.y = 0
                v = self.entries.pop().grid_forget()
        def calc():
            self.starting_location = self.sp.get()
            places_list = []
            for v in self.entries:
                places_list.append(v.get())
            iniciar_proceso(self.starting_location,places_list,self)
            
        def res():
            if self.showres == 1:
                results(self)
            else:
                ad(self,'No results', 'Click results to get \n values')

        self.add = tk.Button(self.a2, text = 'Add', width=6,padx=5,pady=0, command = lambda: add())
        self.add.grid(row=0, column=0,padx=5, pady=5)
        
        self.remove = tk.Button(self.a2, text = 'Remove', width=6,padx=5,pady=0, command = lambda: remove())
        self.remove.grid(row=0, column=1,padx=5, pady=5)
        
        self.calc = tk.Button(self.a4, text = 'Calc', width=6,padx=5,pady=0, command = lambda: calc())
        self.calc.grid(row=0, column = 0, sticky = 'E',padx=5, pady=0)
        self.open = tk.Button(self.a4, text = 'Results', width=6,padx=5,pady=0, command = lambda: res())
        self.open.grid(row=1, column=0,padx=5, pady=0)
        self.root.mainloop()

if __name__ == "__main__":
    main()
