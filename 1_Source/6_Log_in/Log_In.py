from Tkinter import *
from Tkinter import Tk
from Tkinter import PhotoImage
import webbrowser

def callback(event):
    webbrowser.open_new(r"https://www.sat.gob.mx/personas/ayuda")
def exit(self):
    global gui
    gui.destroy()

gui = Tk()
gui.geometry("500x500")
#make sure first is capital and second is not
gui.title("Log in")
FACTURAS_text = Text(gui, height = 10, width =15)
FACTURAS_text.grid(column=0,row=1)
FACTURAS_text.insert(INSERT,"Factura 01\n")
FACTURAS_text.insert(INSERT,"Factura 02\n")
FACTURAS_text.insert(END   ,"Factura 03")
XMLS           = Label(gui ,text="XML's").grid(row=0,column = 0)
RFC            = Label(gui ,text="R.F.C").grid(row=1,column = 1)
PASSWORD       = Label(gui ,text="Password").grid(row=2,column=1)
RFC_TEXTO      = Entry(gui).grid(row=1,column=2)
PASSWORD_TEXTO = Entry(gui).grid(row=2,column=2)
SUBMIT = Button(gui ,text="Submit").grid(row=2,column=3)
Devolucion_Label = Label(gui, text="Tu devolucion").grid(row=6 , column =1)
Devolucion_Entry      = Entry(gui).grid(row=7,column=1)
Reporte_Label    = Label(gui, text="Reporte").grid(row=6 , column = 2)
Enviar           = Button(gui ,text="enviar").grid(row=7, column=2)
link = Label(gui, text="Ayuda", fg="blue", cursor="hand2")
link.grid(column = 4, row = 0)
link.bind("<Button-1>", callback)
link = Label(gui, text="Salir", fg="blue", cursor="hand2")
link.grid(column = 5, row = 0)
link.bind("<Button-1>", exit)

gui.mainloop()