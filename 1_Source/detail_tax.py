from Tkinter import *
from Tkinter import Tk
from Tkinter import PhotoImage
import ttk
import webbrowser

def callback(event):
    webbrowser.open_new(r"https://www.sat.gob.mx/personas/ayuda")
def exit(self):
    global gui
    gui.destroy()

gui = Tk()
gui.geometry("500x500")
gui.title("Detalle de calculo de impuetsos")
#linaks anterios y salir
link_anterior = Label(gui, text="Anterior", fg="blue", cursor="hand2")
link_anterior.grid(column = 0, row = 0)
link_anterior.bind("<Button-1>", callback)
link_anterior = Label(gui, text="Salir", fg="blue", cursor="hand2")
link_salir = Label(gui, text="Salir", fg="blue", cursor="hand2")
link_salir.grid(column = 1, row = 0)
link_salir.bind("<Button-1>", exit)
#concepto hacerlo variable
label_concepto = Label(gui ,text="Concepto").grid(row=1,column = 0)
text_concepto_1 =  Text(gui, height = 1, width =10)
text_concepto_1.grid(row=3, column = 0)
text_concepto_2 =  Text(gui, height = 1, width =10)
text_concepto_2.grid(row=5, column = 0)
text_concepto_3 =  Text(gui, height = 1, width =10)
text_concepto_3.grid(row=7, column = 0)
#A favor hacerlo variable
label_a_favor = Label(gui ,text="A favor").grid(row=1,column = 2)
text_a_favor_1 =  Text(gui, height = 1, width =10)
text_a_favor_1.grid(row=3, column = 2)
text_a_favor_2 =  Text(gui, height = 1, width =10)
text_a_favor_2.grid(row=5, column = 2)
text_a_favor_3 =  Text(gui, height = 1, width =10)
text_a_favor_3.grid(row=7, column = 2)
#A cargo hacerlo variable
label_a_cargo = Label(gui ,text="A cargo").grid(row=1,column = 5)
text_a_cargo_1 =  Text(gui, height = 1, width =10)
text_a_cargo_1.grid(row=3, column = 5)
text_a_cargo_2 =  Text(gui, height = 1, width =10)
text_a_cargo_2.grid(row=5, column = 5)
text_a_cargo_3 =  Text(gui, height = 1, width =10)
text_a_cargo_3.grid(row=7, column = 5)
####
label_total = Label(gui ,text="Total").grid(row=8,column = 4)
text_total_1 =  Text(gui, height = 1, width =10)
text_total_1.grid(row=8, column = 5)
label_total = Label(gui ,text="").grid(row=8,column = 5)
#A Cantidad a pagar hacerlo variable
label_cantidad_pagar = Label(gui ,text="Cantidada a pagar").grid(row=1,column = 7)
text_cantidad_pagar_1 =  Text(gui, height = 1, width =10)
text_cantidad_pagar_1.grid(row=3, column = 7)
text_cantidad_pagar_2 =  Text(gui, height = 1, width =10)
text_cantidad_pagar_2.grid(row=5, column = 7)
text_cantidad_pagar_3 =  Text(gui, height = 1, width =10)
text_cantidad_pagar_3.grid(row=7, column = 7)
#combobox
comboExample = ttk.Combobox(gui,
                            values=[
                                    "Excel",
                                    "PDF",
                                     ])
comboExample.grid(column=5, row=10)

gui.mainloop()