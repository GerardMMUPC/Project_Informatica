from tkinter import *
from tkinter import ttk

window = Tk()
frame = ttk.Frame(window)
frame.grid()


a = ttk.Label(frame, text="")
a.grid(column=0, row=2)

def hide_label():
    a.config(text="Vuelve a pensarlo")

ttk.Label(frame, text="Prueba").grid(column=0, row=1)


ttk.Button(frame, text="Sí", command=window.destroy).grid(column=1, row=1)
ttk.Button(frame, text="No", command=hide_label).grid(column=2, row=1)

window.mainloop()
