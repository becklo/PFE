import time
from os import listdir
import Tkinter as tk
from PIL import ImageTk, Image

class GuiDesign(tk.Frame):
    def __init__(self, parent):
        """
        init function create a frame that contains a text and a scrollbar on the right part of the window.
        Then it calls the start() function
        :param parent:
        """
        global txt_2, root
        tk.Frame.__init__(self, parent)
        txt_2 = tk.Text(self, relief="sunken", wrap="none", bg="#333333")
        scrollb = tk.Scrollbar(command=txt_2.yview, bg='#f5f5f5')
        # scrollb.grid(row=0, column=1, sticky='nsew')
        txt_2.configure(yscrollcommand=scrollb.set)
        scrollb.pack(side="right", fill="y")
        txt_2.pack(fill="both", expand=True)
        self.start()

    def start(self):
        """
        This function check all the file present in a given folder and create a button for each of them. To make it
        more user friendly the name are without the extension and the 'MS_' header
        On click of a button the show_text() function is called.
        :return:
        """
        listfile = []
        for file in listdir("/home/loula/Documents/MicroServices/Receive"):
            listfile += {file}
        print(listfile)
        vars = {}
        i=0
        img = ImageTk.PhotoImage(Image.open("GUI/map.png"))
        for f in listfile:
            print(f)
            name = f.replace("_", " ")
            name = name.replace(".txt", "")
            var = tk.Button(self, text=name, command=lambda f=f: self.show_text(f), wraplength=340, height=3, width=10, font=(40, 40), bg="#cccccc", foreground ="#666666" )
            # var = tk.Button(root, image=img, bg='#c0c0c0', command=lambda f=f: self.show_text(f),)
            txt_2.window_create("end", window=var)
            if i != 0 and i % 3 == 0:
                txt_2.insert("end", "\n\n")
                i = 0
            else:
                txt_2.insert("end", "  ")
                i += 1
            vars[f] = var
            txt_2.pack()
        txt_2.configure(state="disabled")

    def close_window(self, window):
        """
        Close the window entered in param.
        :param window:
        :return:
        """
        window.destroy()

    def show_text(self,file):
        """
        This function create a frame that contains a text and a scrollbar on the right part of the window.
        The text is a raw display of the content of the file given in param.
        :param file:
        :return:
        """
        root_2 = tk.Tk()
        root_2.attributes("-zoomed", True)
        f = open("Receive/"+file, "r")
        content = f.read()
        # create a Frame for the Text and Scrollbar
        txt_frm = tk.Frame(root_2, width=600, height=600, bg="#333333")
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

        # create a Text widget
        txt = tk.Text(txt_frm, borderwidth=3, relief="sunken", bg="#bbbbbb")
        txt.config(font=("consolas", 18), undo=True, wrap='word')
        txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        txt.insert("end", str(content))
        # create a Scrollbar and associate it with txt
        scrollb = tk.Scrollbar(txt_frm, command=txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        txt['yscrollcommand'] = scrollb.set

        # create a button

        button = tk.Button(txt_frm, text="OK", command=lambda: self.close_window(root_2), font=(20, 20),
                           bg="#bebebe", foreground="#ff6666")
        button.grid(row=1, column=0, sticky='nsew')
        txt['button'] = button.focus_set()


if __name__ == '__main__':
    # create a Tk object
    root = tk.Tk()
    root.attributes("-zoomed", True)
    # call GUIDesign methods
    GuiDesign(root).pack(fill="both", expand=True)
    # loop forever
    root.mainloop()
