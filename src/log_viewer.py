#!/usr/bin/env python3

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

class GAALogViewerView(tk.Tk):

    def __init_canvas(self, width=200, height=200):
        canvas = tk.Canvas(
            self,
            width=width,
            height=height
        )
        #using PIL for displaying Jpeg image
        img1 = Image.open(open('./default.jpg', 'rb'))
        img1.thumbnail((500, 500), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1)
        canvas.create_image(  #image on canvas
            0,  # x
            0,  # y
            image=img1,
            anchor="nw",  # place origin is North West
        )
        return canvas, img1

    def __init__(self):
        super().__init__()

        self.title("GAA LogVier")
        self.geometry("800x600")

        self.canvases = []
        self.images = []

        can, img = self.__init_canvas(400, 800)
        self.canvases.append(can)
        self.images.append(img)

        can, img = self.__init_canvas(100,100)
        self.canvases.append(can)
        self.images.append(img)

        can, img = self.__init_canvas(100,100)
        self.canvases.append(can)
        self.images.append(img)

        self.logtext = ScrolledText(self, wrap=tk.WORD, width=100, height=5)

        #Log List Box
        self.log_list = tk.Listbox(self, bd=1)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.log_list.yview)
        self.log_list['yscrollcommand'] = self.scrollbar.set

        self.log_list.pack(side='left',fill="y",expand=False)
        self.scrollbar.pack(side='left', fill="y",expand=False)
        self.logtext.pack(side="bottom",expand=True)
        self.canvases[0].pack(side='left',fill="both",expand=True)
        self.canvases[1].pack(side='top',fill="both",expand=True)
        self.canvases[2].pack(side='bottom',fill="both",expand=True)

        self.log_list.bind("<<ListboxSelect>>", self.__show_selected_log)

        self.__read_log_into_log_list()

    def __show_selected_log(self,event):
        #TODO: real routine
        index = event.widget.curselection()
        log   = event.widget.get(index)
        print(log)

        self.logtext.delete("1.0", tk.END) #delete all from logtext
        self.logtext.insert("1.0", log)

        for c in self.canvases:
            c.delete("all")


        if log == "log=10":
            #case of read from new
#            for c in self.canvases:
#                img1 = Image.open(open('./default.jpg', 'rb'))
#                #if image or tubnail size bigger than canvas size
#                #canvas would not show image
#                #img1.thumbnail((500, 500), Image.ANTIALIAS)
#                img1.thumbnail((200, 200), Image.ANTIALIAS)
#                img1 = ImageTk.PhotoImage(img1)
#                c.create_image(0,0,image=img1,anchor=tk.NW)
#                self.images.append(img1)
#        self.images = []

            #case of reuse
            i = 0
            for c in self.canvases:
                c.create_image(0,0, image=self.images[i], anchor=tk.NW)
                i += 1

    def __read_log_into_log_list(self):
        #set sample data
        #TODO: real log model
        for i in range(100):
            self.log_list.insert("end", "log=%d" % i)


# アプリを起動する
if __name__ == "__main__":
    app = GAALogViewerView()
    app.mainloop()
