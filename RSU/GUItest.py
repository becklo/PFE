# from tkinter import *
# import Tkinter as tk
# from os import listdir
# from PIL import ImageTk, Image
#
#
# def show_text(f):
#     root_2 = tk.Tk()
#     f = open("Receive/test.txt", "r")
#     content = f.read()
#     # create a Frame for the Text and Scrollbar
#     txt_frm = tk.Frame(root_2, width=600, height=600, bg="#000")
#     txt_frm.pack(fill="both", expand=True)
#     # ensure a consistent GUI size
#     txt_frm.grid_propagate(False)
#     # implement stretchability
#     txt_frm.grid_rowconfigure(0, weight=1)
#     txt_frm.grid_columnconfigure(0, weight=1)
#
#     # create a Text widget
#     txt = tk.Text(txt_frm, borderwidth=3, relief="sunken", bg="#bbbbbb")
#     txt.config(font=("consolas", 18), undo=True, wrap='word')
#     txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
#     txt.insert("end", str(content))
#     # create a Scrollbar and associate it with txt
#     scrollb = tk.Scrollbar(txt_frm, command=txt.yview)
#     scrollb.grid(row=0, column=1, sticky='nsew')
#     txt['yscrollcommand'] = scrollb.set
#
#     # create a button
#
#     button = tk.Button(txt_frm, text="OK", command=lambda: close_window(root_2), font=(20, 20), bg="#bebebe",
#                        foreground="#ff6666")
#     button.grid(row=1, column=0, sticky='nsew')
#     txt['button'] = button.focus_set()
#
#
# def close_window(window):
#     """
#     Close the window entered in param.
#     :param window:
#     :return:
#     """
#     window.destroy()
#
#
# root = Tk()
# listfile = []
# for file in listdir("/home/loula/Documents/MicroServices/Receive"):
#     listfile += {file}
# print(listfile)
# vars = {}
# i=0
# c=0
# l=0
# Parking = ImageTk.PhotoImage(Image.open("GUI/parking.png"))
# Sensors = ImageTk.PhotoImage(Image.open("GUI/unnamed.png"))
# GPS = ImageTk.PhotoImage(Image.open("GUI/map.png"))
# Weather = ImageTk.PhotoImage(Image.open("GUI/weather2.ico"))
# Traffic = ImageTk.PhotoImage(Image.open("GUI/traffic.png"))
# BLE = ImageTk.PhotoImage(Image.open("GUI/bluetooth.ico"))
# for f in listfile:
#     print(f)
#     name = f.replace("_", " ")
#     name = name.replace(".txt", "")
#     if name == "test":
#         img = BLE
#     elif name == "test1" or name == "test5":
#         img = GPS
#     elif name == "test2" or name == "test6":
#         img = Sensors
#     elif name == "test3":
#         img = Traffic
#     elif name == "Metz parking price":
#         img = Parking
#     elif name == "test4":
#         img = Weather
#
#     # if name == "BLE":
#     #     img = BLE
#     # elif name == "GPS":
#     #     img = GPS
#     # elif name == "Sensor":
#     #     img = Sensors
#     # elif name == "Traffic information":
#     #     img = Traffic
#     # elif name == "Weather":
#     #     img = Weather
#     # elif name == "Metz parking price":
#     #     img = Parking
#     var = Button(root, image=img, bg='#c0c0c0', command=lambda f=f: show_text(f))
#     l = i/4
#     c = i%4
#     var.grid(row=l, column=c)
#     i += 1
#     vars[f] = var
#
# root.mainloop()

import tkinter as tk

def add_image():
    # text.image_create(tk.END, image = img) # Example 1
    text.window_create(tk.END, window = tk.Label(text, image = img)) # Example 2

root = tk.Tk()

text = tk.Text(root)
text.pack(padx = 20, pady = 20)

tk.Button(root, text = "Insert", command = add_image).pack()


root.mainloop()