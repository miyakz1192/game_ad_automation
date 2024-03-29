
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import array_to_img
import pickle
import uuid
import datetime

#this calss is entity of image log(log with image)
class GAAImageLogEntry:
    def __init__(self, log_id=None, cv2_image=None, dres=None):
        self.cv2_image = cv2_image
        self.dres = dres
        self.log_id = log_id

    def save(self, file_name):
        with open(file_name, 'wb') as f:
            data = [self.log_id, self.cv2_image, self.dres]
            pickle.dump(data, f)

    def save_image(self, file_name):
        cv2.imwrite(file_name, self.cv2_image)

    def load(self, file_name):
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
            self.log_id    = data[0]
            self.cv2_image = data[1]
            self.dres      = data[2]

class GAALogger:
    def __init__(self, log_dir="./gaa_log/", debug_result_show=True, wait_sec=3):
        self.debug_result_show = debug_result_show
        self.log_dir = log_dir
        self.image_log_dir = self.log_dir + "/imagelog/"
        self.temp_file_name = "./gaa_log_image_temp.jpg"
        self.wait_sec = wait_sec
        self.log_file_name = self.log_dir + "messages.log"
        self.image_logging_uuid_str = ";GAA_IMAGE_LOGGING_UUID="

    #screen_shot_image: ScreenShotImage Object
    #dres: list of DetectionResult or DetectionResultContainer
    def __write_res_to_image(self, screen_shot_image, dres, plt):
        currentAxis = plt.gca()
        color = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()[0]

        if type(dres) == list:
            targets = dres
        else:
            targets = dres.res

        for i in targets:
            display_txt = '%s: %.2f'%(i.label, i.score)
            coords = ((i.rect.x, i.rect.y), i.rect.width, i.rect.height)
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(i.rect.x, i.rect.y, display_txt, bbox={'facecolor':color, 'alpha':0.5})

    def __image_log(self, screen_shot_image, dres=None):
        plt.figure(figsize=(8,8))
        rgb_image = array_to_img(screen_shot_image.image,scale=False)
        plt.imshow(rgb_image)

        log_id = str(uuid.uuid4())

        if dres is not None:
            self.__write_res_to_image(screen_shot_image, dres, plt)

        plt.savefig(self.temp_file_name)
        img = cv2.imread(self.temp_file_name)

        ile_file_name = self.image_log_dir + log_id + ".data"
        GAAImageLogEntry(log_id, img, dres).save(ile_file_name)

        if self.debug_result_show is True:
            cv2.imshow(self.temp_file_name , img)
            cv2.waitKey(1000 * self.wait_sec)
            cv2.destroyWindow(self.temp_file_name)

        return log_id

    #message: string of message text(str)
    #screen_shot_image: ScreenShotImage Object
    #dres: list of DetectionResult or DetectionResultContainer
    def __log(self, message , severity, screen_shot_image=None, dres=None):
        dt_now = str(datetime.datetime.now())
        image_log_id = None

        #write image log
        if screen_shot_image:
            image_log_id = self.__image_log(screen_shot_image, dres)

        #write text log
        with open(self.log_file_name, "a") as f:
            if image_log_id is None:
                print("[%s] %s %s" % (dt_now, severity, message), file=f)
                print("[%s] %s %s" % (dt_now, severity, message))
            else:
                print("[%s] %s %s %s%s" % (dt_now, severity, message, self.image_logging_uuid_str, image_log_id), file=f)
                print("[%s] %s %s %s%s" % (dt_now, severity, message, self.image_logging_uuid_str, image_log_id))

    def info(self, message, screen_shot_image=None, dres=None):
        self.__log(message, severity="INFO", screen_shot_image=screen_shot_image, dres=dres)

    def warn(self, message, screen_shot_image=None, dres=None):
        self.__log(message, severity="WARN", screen_shot_image=screen_shot_image, dres=dres)

    def error(self, message, screen_shot_image=None, dres=None):
        self.__log(message, severity="ERROR", screen_shot_image=screen_shot_image, dres=dres)


class GAALoggerModel(GAALogger):
    #default log dir will be chosen if log_dir is None
    def __init__(self, log_dir=None, debug_result_show=True, wait_sec=3):
        super().__init__(log_dir=log_dir, debug_result_show=debug_result_show, wait_sec=wait_sec)

        #https://note.nkmk.me/python-import-usage/
        with open(self.log_file_name) as f:
            self.log_list = f.readlines()


    def get_image_log(self, log_text):
        temp = log_text.split(self.image_logging_uuid_str)

        if len(temp) == 1:
            return None

        res = GAAImageLogEntry()
        uuid_str = temp[1].rstrip()
        res.load(self.image_log_dir + uuid_str + ".data")

        return res
