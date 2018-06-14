#crated 14.06.18
#author Felix Teweleit

from Tkinter import *

def load_button():
    print("Clicked!")

#define ressources needed by Tkinter to draw
master = Tk();
window_height = 600
window_width = 800
control_area_height = 800
control_area_width = 200
inner_border = 5
element_space = 5


#draw main Window
drawing_device = Canvas(master, width = window_width, height = window_height)
drawing_device.create_rectangle(0, 0, control_area_width, control_area_height, fill="#fff")
drawing_device.pack()

#load_button = Button(master, text="Load", command=load_button())
#load_button.place(x = 0, y = 0)


mainloop()
