#!/usr/bin/env python3

import os
import time
import subprocess
from signal import SIGINT
import random

import keras.utils.image_utils as image
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import array_to_img

from detection_result import *

import torch
import json

import pdb

from matplotlib import pyplot as plt



#necessary environments values
class Service:
    def __init__(self, name):
        self.name = name

    def user(self):
        return os.environ[self.name.upper() + "_USER"]

    def passwd(self):
        return os.environ[self.name.upper() + "_PASSWD"]

    def host(self):
        return os.environ[self.name.upper() + "_HOST"]

    def show(self):
        print("[TRACE] " + self.name + " service configuration")
        print(self.user())
        print(self.passwd())
        print(self.host())

    def ssh(self, cmd):
        #sshpass -p <passwd> ssh -o StrictHostKeyChecking=no <user>@<host> <cmd>
        command = ["sshpass", "-p" , self.passwd(), "ssh", "-o" , "StrictHostKeyChecking=no" , self.user()+"@"+self.host()] + cmd
        print("DEBUG: %s" % " ".join(command))
        res = subprocess.check_output(command)
        print("DEBUG: %s" % str(res))

    def scp_upload(self,path_from, path_to): #path_from(local) , path_to(remote)
        # sshpass -p a scp -o StrictHostKeyChecking=no <path_from> <user>@<host>:<path_to>
        command = ["sshpass", "-p" , self.passwd(), "scp", "-o" , "StrictHostKeyChecking=no" , path_from, self.user()+"@"+self.host()+":"+path_to]
        print("DEBUG: %s" % " ".join(command))
        res = subprocess.check_output(command)
        print("DEBUG: %s" % str(res))

    def scp_download(self,path_from, path_to): #path_from(remote) , path_to(local)
        # sshpass -p a scp -o StrictHostKeyChecking=no <path_from> <user>@<host>:<path_to>
        command = ["sshpass", "-p" , self.passwd(), "scp", "-o" , "StrictHostKeyChecking=no" , self.user()+"@"+self.host()+":"+path_from, path_to]
        print("DEBUG: %s" % " ".join(command))
        res = subprocess.check_output(command)
        print("DEBUG: %s" % str(res))


class ScreenShotFile():
    def __init__(self, file_path):
        self.file_path = file_path
        self.image = None

    def load(self):
        self.associate_image(ScreenShotImage(np.array(image.load_img(self.file_path))))
        return self.image

    def save(self):
        image.save_img(self.file_path, array_to_img(self.image.image, scale = False))

    def associate_image(self, screen_shot_image):
        self.image = screen_shot_image

class CoordinateSystem():
    def right_upper_to_normal(self, res_ru, screen_shot_image, width=400):
        for i in res_ru.res:
            xorg = screen_shot_image.image.shape[1] - width
            if xorg < 0:
                xorg = 0
            temp = i.rect.x
            i.rect.x = i.rect.x + xorg
#            print("[DEBUG] before=%d, after=%d id=%d" % (temp, i.rect.x, id(i)))

#retain image as numpy array
class ScreenShotImage():
    def __init__(self, image):
        self.image = image

    def extract_left_upper(self, width=400, height=400):
        left_upper = self.image[0:height,0:width]
        return ScreenShotImage(left_upper)

    def extract_right_upper(self, width=400, height=400):
        ymax = self.image.shape[0]
        xmax = self.image.shape[1]
        right_upper = self.image[0:height,xmax-width:xmax]
        return ScreenShotImage(right_upper)

class Mp4Information:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_duration(self):
        #ffprobe -v quiet -print_format json -show_format -show_streams  -i /tmp/a.mp4
        command = ["ffprobe", "-v", "quiet",  "-print_format", "json", "-show_streams", "-i", self.file_name]
        res = subprocess.run(command, capture_output=True, text=True).stdout
        return float(json.loads(res)["streams"][0]["duration"])

    def get_last_sec(self):
        return int(self.get_duration())
    
class ScrcpyService(Service):
    TEMP_MP4_PATH = "/tmp/a.mp4"
    WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED = 15

    def __init__(self,name):
        super().__init__(name)

    def phone(self):
        return os.environ["SCRCPY_PHONE"]

    def get_screen_shot(self):
        print("TRACE: get_screen_shot")
        #TODO: retry is server connection error
        command = ["/usr/local/bin/scrcpy", "--tcpip=" + self.phone(), "--verbosity=verbose", "--record=/tmp/a.mp4"]
        print("DEBUG: %s" % " ".join(command))
        proc = subprocess.Popen(command)
        time.sleep(self.WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED)
        proc.send_signal(SIGINT)
        time.sleep(5)
        mp4 = Mp4Information(self.TEMP_MP4_PATH)
        print(f"[DEBUG] MP4 = {mp4.get_last_sec()}")
        command = ["ffmpeg", "-i", "/tmp/a.mp4", "-ss", str(mp4.get_last_sec()) , "-frames:v", "1", "/tmp/gaa_screen_temp.jpg", "-y"]
        #subprocess.check_output(command)
        #TODO: if ffmpeg is failed gaa..jpg should not be created
        subprocess.call(command)
        #TODO: consider is gaa...jpg is not found
        return ScreenShotFile("/tmp/gaa_screen_temp.jpg")

    def touch_position(self, pos):
        print("TRACE: touch position")

        if pos is None:
            return

        print("TRACE: touch position=%d,%d" % (pos.rect.x, pos.rect.y))

#        #scrcpy --tcpip=192.168.110.178:38665 --verbosity=verbose & sleep 10 ; echo "152,192" > mdown_input_pipe
        #TODO: retry if connection error
        command = ["scrcpy", "--tcpip=" + self.phone(), "--verbosity=verbose"]
        proc = subprocess.Popen(command)
        print("[DEBUG] wait for %d" % (self.WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED))
        time.sleep(self.WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED)
        print("[DEBUG] touch pos!!!")
        command = "echo " + str(int(pos.rect.x+pos.rect.width/2)) + "," + str(int(pos.rect.y+pos.rect.height/2)) + " > " + "mdown_input_pipe"
        subprocess.run(command , shell=True)
        time.sleep(5)
        proc.send_signal(SIGINT)


class PytorchService(Service):
    REMOTE_RESULT_JPG_FILE_PATH = "~/game_eye/result.jpg"
    LOCAL_RESULT_JPG_FILE_PATH = "./data/result.jpg"
    REMOTE_PICKLE_FILE_PATH = "~/game_eye/eye_result_data.pickle"
    LOCAL_PICKLE_FILE_PATH = "./data/eye_result_data.pickle"

    def __init__(self,name):
        super().__init__(name)

    def call_predictor(self, screen_shot_file):
        #get pickle result file from pytorch_ssd service to this
        #save result.jpg to debugging
        res = DetectionResultContainer()
        self.ssh(["cd ~/game_eye; ./src/game_eye.py %s" % screen_shot_file.file_path])
        self.scp_download(self.REMOTE_RESULT_JPG_FILE_PATH, self.LOCAL_RESULT_JPG_FILE_PATH)
        self.scp_download(self.REMOTE_PICKLE_FILE_PATH    , self.LOCAL_PICKLE_FILE_PATH)

        res.load(self.LOCAL_PICKLE_FILE_PATH)
        return res

    def debug_result_show(self, screen_shot_image, res):
        plt.figure(figsize=(8,8))
        rgb_image = array_to_img(screen_shot_image.image,scale=False)
        color = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()[0]
        plt.imshow(rgb_image)
        currentAxis = plt.gca()
        for i in res.res:
            display_txt = '%s: %.2f'%(i.label, i.score)
            coords = ((i.rect.x, i.rect.y), i.rect.width, i.rect.height)
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(i.rect.x, i.rect.y, display_txt, bbox={'facecolor':color, 'alpha':0.5})


        plt.savefig("./debug_result_show.jpg")
        print("[DEBUG] wait for input")
        input()

    def get_close_position(self, screen_shot_file):
        print("[DEBUG] get_close_position")
        print(screen_shot_file.file_path)

        #extract left upper and right upper from screen_shot_file
        screen_shot_image = screen_shot_file.load()
        lu_img = screen_shot_image.extract_left_upper()
        ru_img = screen_shot_image.extract_right_upper()

        lu_f = ScreenShotFile("/tmp/lu.jpg")
        ru_f = ScreenShotFile("/tmp/ru.jpg")

        lu_f.associate_image(lu_img)
        ru_f.associate_image(ru_img)

        lu_f.save()
        ru_f.save()

        #send lu and ru to pytorch service
        self.scp_upload(lu_f.file_path, lu_f.file_path)
        self.scp_upload(ru_f.file_path, ru_f.file_path)

        #analyze image file by pytorch service and get result
        res = DetectionResultContainer()

        res_lu = self.call_predictor(lu_f)

        #adjust ru result from ru space to true screen_shot space
        res_ru = self.call_predictor(ru_f)
        c = CoordinateSystem()
        c.right_upper_to_normal(res_ru,screen_shot_image)

        res.merge(res_lu)
        res.merge(res_ru)

        res.sort_by_score()

        print("[DEBUG] DetectionResultContainer res")
        res.print()

        self.debug_result_show(screen_shot_image, res)

        if len(res.res) > 0:
            return res.res[0]

        return None


class GameAdAutomation():

    def __init__(self):
        self.scrcpy_s = ScrcpyService("scrcpy")
        self.pytorch_s = PytorchService("pytorch")
        self.scrcpy_s.show()
        self.pytorch_s.show()
    
    def naive_algo(self):
        print("INFO: naive_algo")
        while True:
            screen_shot = self.scrcpy_s.get_screen_shot()
            pos = self.pytorch_s.get_close_position(screen_shot)
            if pos is not None:
                self.scrcpy_s.touch_position(pos)
            else:
                print("INFO: no position found")
            print("INFO: sleep 10")
            time.sleep(10)


def main():
    print("INFO: start game ad automation !!!")
    GameAdAutomation().naive_algo()
    print("INFO: end game ad automation !!!")

if __name__ == "__main__":
    main()
