#!/usr/bin/env python3

import os
import time
import subprocess
from signal import SIGINT


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
        time.sleep(3)
        proc.send_signal(SIGINT)
        time.sleep(5)
        command = ["ffmpeg", "-i", "/tmp/a.mp4",  "-frames:v", "1", "/tmp/gaa_screen_temp.jpg", "-y"]
        subprocess.check_output(command)
        return ScreenShot("/tmp/gaa_screen_temp.jpg")

class PytorchService(Service):
    def __init__(self,name):
        super().__init__(name)

class GameAdAutomation():

    def __init__(self):
        self.scrcpy_s = ScrcpyService("scrcpy")
        self.pytorch_s = ScrcpyService("pytorch")
        self.scrcpy_s.show()
        self.pytorch_s.show()
    
    def wait_for_close(self, timeout=10):
        print("TRACE:wait_for_close. timeout=%d" % (timeout) )
    
    def touch_to_close(self):
        print("TRACE:touch_to_close")

    def naive_algo(self):
        screen_shot = self.scrcpy_s.get_screen_shot()
        self.wait_for_close()
        self.touch_to_close()


def main():
    print("INFO: start game ad automation !!!")
    GameAdAutomation().naive_algo()
    print("INFO: end game ad automation !!!")

if __name__ == "__main__":
    main()
