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

        self.logshow = ScrolledText(self, wrap=tk.WORD, width=100, height=5)

        #Log List Box
        self.log_list = tk.Listbox(self, bd=1)
        #set sample data
        for i in range(100):
            self.log_list.insert("end", "log=%d" % i)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.log_list.yview)
        self.log_list['yscrollcommand'] = self.scrollbar.set

        self.log_list.pack(side='left',fill="y",expand = False)
        self.scrollbar.pack(side='left', fill="y",expand = False)
        self.logshow.pack(side="bottom",expand=True)
        self.canvases[0].pack(side='left',fill="both",expand = True)
        self.canvases[1].pack(side='top',fill="both",expand = True)
        self.canvases[2].pack(side='bottom',fill="both",expand = True)

        #expand log list box to North and South
        #self.log_list.grid(row=0, column=0, sticky=tk.N+tk.S)
        #self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        #self.canvases[0].grid(row=0, column=2)
        #self.canvases[1].grid(row=0, column=3)
        #self.canvases[2].grid(row=0, column=4)

        #self.grid_columnconfigure(1, weight=1)
        #self.grid_rowconfigure(1, weight=1)
        

# アプリを起動する
if __name__ == "__main__":
    app = GAALogViewerView()
    app.mainloop()
