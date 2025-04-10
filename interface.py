from tkinter import *
from tkinter import ttk

window = Tk()
frame = ttk.Frame(window)
frame.grid()

# Define the label 'a'
a = ttk.Label(frame, text="")
a.grid(column=0, row=2)

# Define a function to modify the label text
def hide_label():
    a.config(text="Vuelve a pensarlo")


# Add the second label
ttk.Label(frame, text="¿Es Gerard el más sexy?").grid(column=0, row=1)

# Add the buttons
ttk.Button(frame, text="Sí", command=window.destroy).grid(column=1, row=1)
ttk.Button(frame, text="No", command=hide_label).grid(column=2, row=1)

window.mainloop()
