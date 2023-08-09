#!/usr/bin/env python3

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

from collections import defaultdict

from image_log import *

import cv2

import sys

#thanks! https://qiita.com/derodero24/items/f22c22b22451609908ee
def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

class GAALogViewerView(tk.Tk):

    def __init_canvas(self, width=200, height=200):
        canvas = tk.Canvas(
            self,
            width=width,
            height=height
        )

        #self.tkimage["gaa_log_id_sample1"] = image_id
        #self.images.append(img1)

        #img1 = Image.open(open('./default2.jpg', 'rb'))
        #img1.thumbnail((500, 500), Image.ANTIALIAS)
        #img1 = ImageTk.PhotoImage(img1)

        #image_id = 0
        #image_id = canvas.create_image(  #image on canvas
        #    0,  # x
        #    0,  # y
        #    image=img1,
        #    anchor="nw",  # place origin is North West
        #)

        #self.tkimage["gaa_log_id_sample2"] = image_id
        #self.images.append(img1)
        #print("IMAGEID=%d" % image_id)
        return canvas

    def __main_canvas(self):
        return self.canvases[0]

    def __init__(self, search_word=None):
        super().__init__()

        self.search_word = search_word

        self.title("GAA LogVier")
        self.geometry("800x600")

        self.canvases = []
        #self.tkimage = defaultdict(int)
        self.tkimage = {}
        self.images = []

        #init main canvas
        can = self.__init_canvas(400, 800)
        img1 = Image.open(open('./default.jpg', 'rb'))
        img1.thumbnail((500, 500), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1)
        image_id = can.create_image(  #image on canvas
            0,  # x
            0,  # y
            image=img1,
            anchor="nw",  # place origin is North West
        )
        print("IMAGEID=%d" % image_id)
        self.tkimage["default"] = image_id
        self.images.append(img1)
        self.canvases.append(can)

        #init sub canvas
        can = self.__init_canvas(100,100)
        self.canvases.append(can)

        #init sub canvas
        can = self.__init_canvas(100,100)
        self.canvases.append(can)

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
        self.bind("<KeyPress>", self.__key_event)

        self.gaa_logger_model = GAALoggerModel()
        self.__read_log_into_log_list()

    def __key_event(self, event):
        if event.keysym != "w":
            return

        print("INFO: write image")
        index = event.widget.curselection()
        log   = event.widget.get(index)
        print("Line=%d" % index)

        img_log = self.gaa_logger_model.get_image_log(log)
        if img_log is None:
            print("INFO: image not found")
            return

        img_log.save_image("./image_box/" + img_log.log_id + ".jpg")
        print("INFO: saved")


    def __show_selected_log(self,event):
        index = event.widget.curselection()
        log   = event.widget.get(index)

        print("Line=%d" % index)

        self.logtext.delete("1.0", tk.END) #delete all from logtext
        self.logtext.insert("1.0", log)

        self.__main_canvas().lift(self.tkimage["default"])
        img_log = self.gaa_logger_model.get_image_log(log)
        if img_log is None: #normal text log
            return


        #log with image(image log)
        if img_log.log_id in self.tkimage:
            #already load, just lift that image to top 
            self.__main_canvas().lift(self.tkimage[img_log.log_id])
        else:
            #create new image and register to tkimage hash db
            #img1 = Image.open(open('/tmp/gaa_logviewer_temp.jpg', 'rb'))
            img1 = cv2pil(img_log.cv2_image)
            #if image or tubnail size bigger than canvas size
            #canvas would not show image
            img1.thumbnail((500, 500), Image.ANTIALIAS)
            #img1.thumbnail((200, 200), Image.ANTIALIAS)
            img1 = ImageTk.PhotoImage(img1)
            imgid=self.__main_canvas().create_image(0,0,image=img1,anchor=tk.NW)
            self.images.append(img1)
            self.tkimage[img_log.log_id] = imgid

#        for c in self.canvases:
#            c.delete("all")


#        if log == "log=10":
#            #case of read from new
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
#            i = 0
#            for c in self.canvases:
##                c.create_image(0,0, image=self.images[i], anchor=tk.NW)
#                #moveto is fast???
#                print(self.tkimage["gaa_log_id_sample1"])
#                #c.moveto(self.tkimage["gaa_log_id_sample1"],1,1)
#                #c.moveto(self.tkimage["gaa_log_id_sample2"],1,1)
#                c.lift(self.tkimage["gaa_log_id_sample1"])
#                i += 1

    def __read_log_into_log_list(self):
        count = 0
        for i in self.gaa_logger_model.log_list:
            if self.search_word is not None:
                if self.search_word in i:
                    self.log_list.insert("end", i)
                    count += 1
            else:
                self.log_list.insert("end", i)
                count += 1
        print(f"INFO: read log %d lines" % (count))


# アプリを起動する
if __name__ == "__main__":
    search_word = None
    if len(sys.argv) == 2:
        search_word = sys.argv[1]
    app = GAALogViewerView(search_word)
    app.mainloop()
