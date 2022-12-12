#!/usr/bin/env python3

import os
import time
import subprocess
from signal import SIGINT
import random


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

class ScreenShot():
    def __init__(self, file_path):
        self.file_path = file_path

    def file_path():
        return self.file_path
        
    
class ScrcpyService(Service):
    def __init__(self,name):
        super().__init__(name)

    def phone(self):
        return os.environ["SCRCPY_PHONE"]

    def get_screen_shot(self):
        print("TRACE: get_screen_shot")
        command = ["/usr/local/bin/scrcpy", "--tcpip=" + self.phone(), "--verbosity=verbose", "--record=/tmp/a.mp4"]
        print("DEBUG: %s" % " ".join(command))
        proc = subprocess.Popen(command)
        time.sleep(5)
        proc.send_signal(SIGINT)
        time.sleep(5)
        command = ["ffmpeg", "-i", "/tmp/a.mp4",  "-frames:v", "1", "/tmp/gaa_screen_temp.jpg", "-y"]
        #subprocess.check_output(command)
        subprocess.call(command)
        return ScreenShot("/tmp/gaa_screen_temp.jpg")

    def touch_position(self, pos):
        #TODO:
        print("INFO: touch_position %s" % str(pos))

class PytorchService(Service):
    def __init__(self,name):
        super().__init__(name)

    def get_close_position(self, screen_shot):
        #TODO:
        #send screen shot to pytorch service
        #request to AI program
        #parse result and extract close position
        #None is no position found, otherwise return (x,y)
        if int(random.random() * 10) % 2 == 0:
            return (1192, 1192)

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
