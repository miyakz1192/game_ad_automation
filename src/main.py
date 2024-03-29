#!/usr/bin/env python3

import warnings
warnings.resetwarnings()
warnings.simplefilter('ignore')

import cv2

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

import gaa_lib_loader
import gaa_constants
from detection_result import *
from easy_sshscp import *
from number_suffix import *

from image_log import *

import torch
import json

import pdb

from matplotlib import pyplot as plt

import re
import sys


##### INIT GAALogger #####
global_gaa_logger = GAALogger()

def gaa_info(message, screen_shot_image=None, dres=None):
    global global_gaa_logger
    global_gaa_logger.info(message, screen_shot_image, dres)

def gaa_warn(message, screen_shot_image=None, dres=None):
    global global_gaa_logger
    global_gaa_logger.warn(message, screen_shot_image, dres)

def gaa_error(message, screen_shot_image=None, dres=None):
    global global_gaa_logger
    global_gaa_logger.error(message, screen_shot_image, dres)
##########################

def big_log(message):
    gaa_info("==========================================")
    gaa_info("==========================================")
    gaa_info(message)
    gaa_info("==========================================")
    gaa_info("==========================================")

def mid_log(message):
    gaa_info("==========================================")
    gaa_info(message)
    gaa_info("==========================================")


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
        gaa_info("[TRACE] " + self.name + " service configuration")

    def ssh(self, cmd):
        #sshpass -p <passwd> ssh -o StrictHostKeyChecking=no <user>@<host> <cmd>
        command = ["sshpass", "-p" , self.passwd(), "ssh", "-o" , "StrictHostKeyChecking=no" , self.user()+"@"+self.host()] + cmd
        #print("DEBUG: %s" % " ".join(command))
        res = subprocess.check_output(command)
        #print("DEBUG: %s" % str(res.decode()))

    def scp_upload(self,path_from, path_to): #path_from(local) , path_to(remote)
        # sshpass -p a scp -o StrictHostKeyChecking=no <path_from> <user>@<host>:<path_to>
        command = ["sshpass", "-p" , self.passwd(), "scp", "-o" , "StrictHostKeyChecking=no" , path_from, self.user()+"@"+self.host()+":"+path_to]
        #print("DEBUG: %s" % " ".join(command))
        res = subprocess.check_output(command)
        #print("DEBUG: %s" % str(res))

    def scp_download(self,path_from, path_to): #path_from(remote) , path_to(local)
        # sshpass -p a scp -o StrictHostKeyChecking=no <path_from> <user>@<host>:<path_to>
        command = ["sshpass", "-p" , self.passwd(), "scp", "-o" , "StrictHostKeyChecking=no" , self.user()+"@"+self.host()+":"+path_from, path_to]
        #print("DEBUG: %s" % " ".join(command))
        res = subprocess.check_output(command)
        #print("DEBUG: %s" % str(res))


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

    def extract_left_upper(self, width=400, height=400, remain_height=200):
        left_upper = self.image[0:height,0:width]
        #left_upper[remain_height:height, 0:width] = 0
        return ScreenShotImage(left_upper)

    def extract_right_upper(self, width=400, height=400, remain_height=200):
        ymax = self.image.shape[0]
        xmax = self.image.shape[1]
        right_upper = self.image[0:height,xmax-width:xmax]
        #right_upper[remain_height:height, 0:width] = 0
        return ScreenShotImage(right_upper)

    #start_pos = (x,y) #tuple
    #size = (w,h) #tuple
    def extract(self, start_pos, size):
        ymax = self.image.shape[0]
        xmax = self.image.shape[1]
        x = start_pos[0]
        y = start_pos[1]
        w = size[0]
        h = size[1]

        if x + w > xmax:
            w = xmax - x

        if y + h > ymax:
            h = ymax - y

        temp = self.image[y:y+h,x:x+w]

        return ScreenShotImage(temp)

    #detection_result: DetectionResult
    def extract_with_DR(self, detection_result):
        #give short name
        r = detection_result.rect
        start_pos = (r.x, r.y)
        size = (r.width, r.height)
        return self.extract(start_pos, size)

    #this core retrun True is self and target_screen_shot_image shape is same. return False if different pixels are over threshold between self and target_screen_shot_image's
    def eq(self, target_screen_shot_image, threshold=0.5):
        if self.image.shape != target_screen_shot_image.image.shape:
            return False

        #give short name
        this = self.image
        target = target_screen_shot_image.image

        count = np.count_nonzero(this == target) / this.size

        return count > threshold

class GAAFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def file_path(self):
        return self.file_name

    def remove_file(self):
        if self.exists_file() is True:
            os.remove(self.file_name)

    def exists_file(self):
        return os.path.isfile(self.file_name)


class Mp4File(GAAFile):
    def __init__(self, file_name):
        super().__init__(file_name)

    def get_duration(self):
        dur = 0.0
        for i in range(5):
            try:
                gaa_info("get_duration")
                #ffprobe -v quiet -print_format json -show_format -show_streams  -i /tmp/a.mp4
                command = ["ffprobe", "-v", "quiet",  "-print_format", "json", "-show_streams", "-i", self.file_name]
                res = subprocess.run(command, capture_output=True, text=True).stdout
                print(res)
                dur = float(json.loads(res)["streams"][0]["duration"])
            except:
                gaa_warn("get_duration err retry")
        return dur


    def get_last_sec(self):
        return int(self.get_duration())

class ScrcpyService(Service):
    TEMP_MP4_PATH = "/tmp/a.mp4"
    WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED = 15
    RETRY_COUNT_SCRCPY_CMD = 10
    RETRY_COUNT_CMD        = 10

    def __init__(self,name):
        super().__init__(name)

    def phone(self):
        return os.environ["SCRCPY_PHONE"]

    def __cmd_with_timeout(self, command, timeout=3):
        try:
            subprocess.run(command , shell=True, timeout=timeout)
        except subprocess.TimeoutExpired as e:
            gaa_warn("INFO: timed out with %d" % (str(timeout)))

    def __call_scrcpy_cmd_with_retry(self):
        #command = ["/usr/local/bin/scrcpy", "--tcpip=" + self.phone(), "--verbosity=verbose", "--record=%s" % (self.TEMP_MP4_PATH)]
        command = ["/usr/local/bin/scrcpy", "--tcpip=" + self.phone(), "--record=%s" % (self.TEMP_MP4_PATH)]

        for i in range(self.RETRY_COUNT_SCRCPY_CMD):
            mp4 = Mp4File(self.TEMP_MP4_PATH)
            mp4.remove_file()
            #print("DEBUG(%d): %s" % (i, " ".join(command)))
            proc = subprocess.Popen(command)
            #print("INFO: enter sleep")
            time.sleep(self.WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED)
            #FIXME: this code is buggy. if process(scrcpy) already done. send_signal send to unexpeced another process!!! only if OS get same PID
            #print("INFO: SIGINT")
            proc.send_signal(SIGINT)
            if mp4.exists_file() is True:
                #print("INFO: OK")
                break
            gaa_warn("ERROR: mp4 file get failed from scrcpy retry")

    def __call_ffmpeg_cmd(self, mp4_file, jpg_file):
        for i in range(self.RETRY_COUNT_CMD):
            jpg_file.remove_file()
            command = ["ffmpeg", "-i", mp4_file.file_path(), "-ss", str(mp4_file.get_last_sec()) , "-frames:v", "1", jpg_file.file_path(), "-y"]
            #subprocess.check_output(command)
            #TODO: if ffmpeg is failed gaa..jpg should not be created
            res = subprocess.call(command)
            if res == 0 and jpg_file.exists_file() is True:
                return True
            else:
                gaa_warn("ERROR: ffmpeg returned not 0(%d). retry" % (res))

        return False

    #WARN: this code is not thread safe!!
    def get_screen_shot(self, file_name="/tmp/gaa_screen_temp.jpg"):
        retry_count = 0
        ok_flg = False
        while ok_flg == False:
            gaa_warn("TRACE: get_screen_shot(try=%d) with %s" % (retry_count, file_name))
            self.__call_scrcpy_cmd_with_retry()
            time.sleep(5)
            mp4 = Mp4File(self.TEMP_MP4_PATH)
            #print(f"[DEBUG] MP4 = {mp4.get_last_sec()}")
            jpg_file = GAAFile(file_name)
            ok_flg = self.__call_ffmpeg_cmd(mp4, jpg_file)
            retry_count += 1

        #TODO: consider is gaa...jpg is not found
        return ScreenShotFile(file_name)

    def touch_position(self, pos):
        gaa_info("TRACE: touch position")

        if pos is None:
            gaa_info("INFO: touch_position called with None. may be touch position will be not found")
            return

        for try_count in range(self.RETRY_COUNT_SCRCPY_CMD):
            gaa_info("TRACE: touch position=%d,%d" % (pos.rect.x, pos.rect.y))
    #        #scrcpy --tcpip=192.168.110.178:38665 --verbosity=verbose & sleep 10 ; echo "152,192" > mdown_input_pipe
            #TODO: retry if connection error

            command = ["scrcpy", "--tcpip=" + self.phone(), "--verbosity=verbose"]
            proc = subprocess.Popen(command)
            gaa_info("[DEBUG] wait for %d" % (self.WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED))
            time.sleep(self.WAIT_TIME_FOR_WIRELESS_DEBUG_DIALOG_VANISHED)

            if proc.poll() is None: # scrcpy command is still active
                gaa_info("[DEBUG] touch pos!!!")
                command = "echo " + str(int(pos.rect.x+pos.rect.width/2)) + "," + str(int(pos.rect.y+pos.rect.height/2)) + " > " + "mdown_input_pipe"
                self.__cmd_with_timeout(command)
                time.sleep(5)
                proc.send_signal(SIGINT)
                break
            else: #scrcpy command already vanished due to some reason
                gaa_warn("ERROR: scrcpy already ended retry")

    def wait_screen_changed(self, before_screen_shot_f):
        after_screen_shot_f = self.get_screen_shot(file_name="/tmp/after.jpg")
        before_image = before_screen_shot_f.load()
        after_image  = after_screen_shot_f.load()

        while before_image.eq(after_image):
            gaa_info("INFO: before_image and after_image are eq")
            time.sleep(5)
            after_screen_shot_f = self.get_screen_shot(file_name="/tmp/after.jpg")
            after_image  = after_screen_shot_f.load()
        gaa_info("INFO: before_image and after_image are CHANGED!!!")



class PytorchService(Service):
    REMOTE_RESULT_JPG_FILE_PATH = "~/game_eye/result.jpg"
    LOCAL_RESULT_JPG_FILE_PATH = "./data/result.jpg"
    REMOTE_PICKLE_FILE_PATH = "~/game_eye/eye_result_data.pickle"
    LOCAL_PICKLE_FILE_PATH = "./data/eye_result_data.pickle"

    def __init__(self,name):
        super().__init__(name)
        self.cyclic_ad_button_pusher = CyclicAdButtonPusher(self)

    def call_predictor(self, screen_shot_file, algo="all"):
        #get pickle result file from pytorch_ssd service to this
        #save result.jpg to debugging
        res = DetectionResultContainer()
        self.ssh(["cd ~/game_eye; ./src/game_eye.py %s --algo %s" % (screen_shot_file.file_path, algo)])
        self.scp_download(self.REMOTE_RESULT_JPG_FILE_PATH, self.LOCAL_RESULT_JPG_FILE_PATH)
        self.scp_download(self.REMOTE_PICKLE_FILE_PATH    , self.LOCAL_PICKLE_FILE_PATH)

        res.load(self.LOCAL_PICKLE_FILE_PATH)
        return res

    def debug_result_show(self, screen_shot_image, res, file_name="./debug_result_show.jpg", wait_sec=15):
        plt.figure(figsize=(8,8))
        rgb_image = array_to_img(screen_shot_image.image,scale=False)
        color = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()[0]
        plt.imshow(rgb_image)
        currentAxis = plt.gca()

        if type(res) == list:
            targets = res
        else:
            targets = res.res

        for i in targets:
            display_txt = '%s: %.2f'%(i.label, i.score)
            coords = ((i.rect.x, i.rect.y), i.rect.width, i.rect.height)
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(i.rect.x, i.rect.y, display_txt, bbox={'facecolor':color, 'alpha':0.5})


        #plt.savefig("./debug_result_show.jpg")
        plt.savefig(file_name)
        gaa_info("[DEBUG] wait for input")

        img = cv2.imread(file_name)
        cv2.imshow(file_name , img)
        #cv2.waitKey(0)
        cv2.waitKey(1000 * wait_sec)
        cv2.destroyWindow(file_name)

        #input()

    #con: DetectionResultContainer
    def __select_best_close(self, con, threshold = 0.99):
        r = re.compile(r'.*close.*')

        closes = con.res
        closes = list(filter(lambda x: r.match(x.label) and x.score >= threshold , closes))

        best_close = None
        best_score = sys.maxsize
        for close in closes:
            score = abs(close.rect.width - close.rect.height)
            if score < best_score:
                best_score = score
                best_close = close

        return best_close

    #WARN: this code is not thread safe!!
    def get_close_position(self, screen_shot_file):
        gaa_info("[DEBUG] get_close_position")
        gaa_info(screen_shot_file.file_path)

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

        #print("[DEBUG] DetectionResultContainer res")
        #res.print()

        self.debug_result_show(screen_shot_image, res)

        gaa_info("get close pos", screen_shot_image, res)

        best_close = self.__select_best_close(res)

        #for debug_result_show only
        if best_close is not None:
            gaa_info("INFO: best close found !!!!!!!!!!!!!", screen_shot_image, [best_close])
        ##########################

        return best_close

class CyclicAdButtonPusher:
    def __init__(self, pytorch_s):
        self.counter = 0
        self.virtical_stride = 1
        #window_size = (w,h)
        self.window_size = (264, 200)
        #FIXME(start_pos): if phone display resolution changed , this code would not work
        #start_pos = (x,y)
        self.start_pos = (600, 700) 
        self.pytorch_s = pytorch_s

    def __get_next_pos(self, screen_shot_image):
        ymax = screen_shot_image.image.shape[0]
        
        pos_y = self.counter * self.virtical_stride * self.window_size[1] + self.start_pos[1]
        if pos_y > ymax:
            #recalc pos_y
            self.counter = 0
            return self.__get_next_pos(screen_shot_image)
        
        pos_x = self.start_pos[0]

        return (pos_x, pos_y)
    
    #det_res is DetectionResult instance
    def __window_coordinate_system_to_normal(self, det_res):
        pos_x = self.start_pos[0]
        pos_y = self.counter * self.virtical_stride * self.window_size[1] + self.start_pos[1]
        det_res.rect.x += pos_x
        det_res.rect.y += pos_y


    #TODO: now implemantaion only support "virtical"
    def push(self, screen_shot_file, direction="virtical"):
        gaa_info("INFO: push Ad Button start")
        screen_shot_image = screen_shot_file.load()
        pos = self.__get_next_pos(screen_shot_image)
        gaa_info("INFO: PUSH POS => [%d]@%s" % (self.counter,str(pos)))
        adbutton_img = screen_shot_image.extract(pos, self.window_size)
        adbutton_f = ScreenShotFile("/tmp/adbutton.jpg")
        adbutton_f.associate_image(adbutton_img)
        adbutton_f.save()
        file_path = adbutton_f.file_path

        ssh = EasySSHSCP()
        ssh.upload(file_path, "gameeye", file_path)
        res = DetectionResultContainer()
        res_adbutton = self.pytorch_s.call_predictor(adbutton_f, algo="ssd")
        res.merge(res_adbutton)
        res.sort_by_score()
        #res.print()

        #FIXME: to be DRY(Do not Repeat Yourself)
        button_res = None
        if len(res.res) > 0:
            temp = list(filter(lambda x: x.label == "adbutton", res.res))
            if len(temp) > 0:
                button_res =  temp[0]
                gaa_info("INFO: Ad Button info")
                #button_res.print()
                self.__window_coordinate_system_to_normal(button_res)
                #print("INFO: __window_coordinate_system_to_normal")
                #button_res.print()

                gaa_info("push ad button", screen_shot_image, [button_res])
                if button_res.score < 0.1:
                    gaa_info("INFO: this ad button ignored due to low score")
                    button_res = None

        self.counter += 1
        gaa_info("INFO: push Ad Button end")
        return button_res


class GameAdAutomation():

    STATE_INITIAL = "state_initial"
    STATE_AD      = "state_ad"

    RES_POS_NOT_FOUND               = 0
    RES_TRY_NEXT_AD_BUTTON          = 1
    RES_RESCAN_CLOSE                = 2
    RES_SCENE_CHANGED_INITIAL_TO_AD = 3
    RES_SCENE_CHANGED_AD_TO_INITIAL = 4

    def __init__(self):
        self.scrcpy_s = ScrcpyService("scrcpy")
        self.pytorch_s = PytorchService("pytorch")
        self.scrcpy_s.show()
        self.pytorch_s.show()
        self.state = self.STATE_INITIAL

    def __print_state(self):
        mid_log("STATE=%s" % self.state)

    def __get_initial_scene(self):
        big_log("GET INITIAL SCENE")
        self.initial_screen_shot_file = self.scrcpy_s.get_screen_shot(file_name="/tmp/gaa_initial.jpg")

        gaa_info("initial scene", self.initial_screen_shot_file.load())

    def __wait_scene_initial_to_ad(self):
        res = self.__wait_scene_common("WAIT FOR SCENE INITIAL TO AD", False)
        self.state = self.STATE_AD
        return res

    def __wait_scene_ad_to_initial(self):
        res = self.__wait_scene_common("WAIT FOR SCENE AD TO INITIAL", True)
        self.state = self.STATE_INITIAL
        return res

    def __wait_scene_common(self, message, finish_cond, try_count=10):
        for i in range(try_count): 
            big_log(message)
            self.__print_state()
            target_screen_shot_file = self.scrcpy_s.get_screen_shot(file_name="/tmp/gaa_wait_scene_common_target.jpg")
            initial_image = self.initial_screen_shot_file.load()
            target_image = target_screen_shot_file.load()

            gaa_info("initial image", initial_image)
            gaa_info("target image", target_image)

            if initial_image.eq(target_image) == finish_cond:
                gaa_info("INFO: initial_image.eq(target_image) == %s" % (str(finish_cond)))
                return True

        gaa_info("INFO: initial_image.eq(target_image) != %s" % (str(finish_cond)))
        return False

    def __push_ad_button(self):
        big_log("PUSH AD BUTTON")
        screen_shot = self.scrcpy_s.get_screen_shot()
        pos = self.pytorch_s.cyclic_ad_button_pusher.push(screen_shot)
        if pos is None:
            mid_log("INFO: pos is not found")
            return self.RES_TRY_NEXT_AD_BUTTON 

        self.scrcpy_s.touch_position(pos)
        if self.__wait_scene_initial_to_ad() is False:
            mid_log("INFO: screen not changed. try next ad button")
            return self.RES_TRY_NEXT_AD_BUTTON

        return self.RES_SCENE_CHANGED_INITIAL_TO_AD

    #src_screen_shot_file: ScreenShotFile
    #src_pos_dr: DetectionResult
    def __save_img_at(self, src_screen_shot_file, src_pos_dr, directory, file_name_prefix):
        mid_log("INFO: saving close")
        nsf = NumberSuffixFile(directory_path=directory)
        img = src_screen_shot_file.image.extract_with_DR(src_pos_dr)
        img_f = ScreenShotFile(directory + "/" + file_name_prefix+ "_" + str(nsf.next()) + ".jpg")

        img_f.associate_image(img)
        img_f.save()

    def __save_true_close(self, src_screen_shot_file, src_pos_dr):
        self.__save_img_at(src_screen_shot_file, src_pos_dr, gaa_constants.GAA_AUTO_GEN_DIR_CLOSE_TRUE, "close")

    def __save_false_close(self, src_screen_shot_file, src_pos_dr):
        self.__save_img_at(src_screen_shot_file, src_pos_dr, gaa_constants.GAA_AUTO_GEN_DIR_CLOSE_FALSE, "close")

    def __push_close_button(self):
        big_log("PUSH CLOSE BUTTON")
        screen_shot = self.scrcpy_s.get_screen_shot()
        pos = self.pytorch_s.get_close_position(screen_shot)
        if pos is None:
            mid_log("INFO: pos is not found")
            return self.RES_RESCAN_CLOSE

        self.scrcpy_s.touch_position(pos)
        time.sleep(10)
        if self.__wait_scene_ad_to_initial() is False:
            mid_log("INFO: screen not changed. try scaning close again")
            self.__save_false_close(screen_shot, pos)
            return self.RES_RESCAN_CLOSE

        self.__save_true_close(screen_shot, pos)
        return self.RES_SCENE_CHANGED_AD_TO_INITIAL
    
    def naive_algo(self):
        gaa_info("INFO: naive_algo")
        self.__get_initial_scene()
        while True:
            while True:
                res = self.__push_ad_button()
                if res == self.RES_SCENE_CHANGED_INITIAL_TO_AD:
                    break

            gaa_info("INFO: sleep 60")
            time.sleep(60)

            while True:
                res = self.__push_close_button()
                if res == self.RES_SCENE_CHANGED_AD_TO_INITIAL:
                    break

            gaa_info("INFO: sleep 10")
            time.sleep(10)


def main():
    gaa_info("INFO: start game ad automation !!!")
    GameAdAutomation().naive_algo()
    gaa_info("INFO: end game ad automation !!!")

def for_debug_issue18():
    initial_f = ScreenShotFile("/home/a/game_ad_automation/bad_case/issue_18/gaa_initial.jpg")
    target_f = ScreenShotFile("/home/a/game_ad_automation/bad_case/issue_18/gaa_wait_scene_common_target.jpg")

    initial_image = initial_f.load()
    target_image = target_f.load()

    if initial_image.eq(target_image) == True:
        print("INFO: eq")
    else:
        print("INFO: NOT EQ")

def for_debug_number_suffix():
    nsf = NumberSuffixFile(directory_path=gaa_constants.GAA_AUTO_GEN_DIR_CLOSE_TRUE)
    print(nsf.numbers)
    print(nsf.max())
    print(nsf.next())

if __name__ == "__main__":
    main()
#    for_debug_issue18()
#    for_debug_number_suffix()
