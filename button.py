#!/usr/bin/env python3

import numpy as np
from time import sleep
import vlc
import gpio as GPIO
import os
import time
import sys
import atexit
import subprocess
from English.time.time import Tind
from English.what.what import SSD
from English.set_face_who.Add_Face import Recognizer
from English.money.yolov5.money import Money
from English.colors.colors import Color_detection 
#from English.machine_voice.machine_voice import MachineVoices
from English.online_features.online_feature import Reader
from English.change_language.change_language import CHLANG
from play_audio import GTTSA
from pydub import AudioSegment
from config import *

# Clear and refresh cache memory with sudo
subprocess.run(["sudo", "sync"])
subprocess.run(["sudo", "sh", "-c", "echo 1 > /proc/sys/vm/drop_caches"])

os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")

def cleanup():
    os.system("python3 /home/rock/Desktop/Hearsight/mycroft-precise/test/scripts/cleanup.py")
        
class HearsightAudioVision:
    def __init__(self):
        self.count = -1
#        self.feature_names = [
#            "change_language", "Time", "walk", "money", "colors", "set face", "person", "what",
#            "go_see", "voice", "read", "document", "book", "worksheet",
#            "bank", "temperature", "voice", "off"
#        ]
        
#        self.feature_names = [
#            "change_language", "Time", "walk", "money", "colors", "set face", "person", "what",
#            "go_see", "voice", "read", "hearsight_app", "document", "media", "temperature", "voice", "off"
#        ]
        
#        self.feature_names = [
#            "walk", "go_see", "what", "money", "person", "colors", "time_and_date", "read", "scan", "voice", "hearsight_app",
#            "document", "media", "temperature", "set face", "change_language", "user_guide", "volume", "off", "voice"
#        ]

#        self.feature_names = [
#            "walk", "go_see", "what", "money", "person", "colors", "time_and_date", "read", "voice", "hearsight_app",
#            "document", "media", "temperature", "set face", "change_language", "user_guide", "volume", "battery_percentage", "off", "voice"
#        ]
        
#        self.feature_names = [
#            "walk", "go_see", "what", "money", "person", "colors", "time_and_date", "read", "voice", "hearsight_app",
#            "document", "media", "Add_face", "settings", "off", "voice"
#        ]
        
        self.feature_names = [
            "walk", "go_see", "what", "money", "person", "colors", "read", "voice", "hearsight_app",
            "hearsight_storage", "time_and_date", "settings", "off", "voice"
        ]
        
        GPIO.setup([450, 421, 447, 448], GPIO.IN)
        self.time_obj = Tind()
        self.what_obj = SSD()
        self.face_obj = Recognizer()
        self.mon_obj = Money()
        self.online_feature_obj = Reader()
        self.color_obj = Color_detection()
#        self.machineVoice_obj = MachineVoices()
        self.play_audio = GTTSA()
        self.lang_obj = CHLANG()

    def confirm_action(self):
        if GPIO.input(447):
            sleep(0.1)
            self.play_audio.play_machine_audio("feature_confirmed.mp3")
            self.handle_feature()
            
    def rotate_feature(self, direction):
        self.count = (self.count + direction) % len(self.feature_names)
        print(self.count)
        self.play_audio.play_machine_audio("{}.mp3".format(self.feature_names[self.count]))

    def handle_feature(self):
        feature_name = self.feature_names[self.count]

        if feature_name == "time_and_date":
            self.time_obj.tellTime()
            self.play_audio.play_machine_audio("Thank You.mp3")
        
#        if feature_name == "change_language":
#            self.lang_obj.handle_lang()
        
        elif feature_name == "walk":
            sleep(3)
            os.system("python /home/rock/Desktop/Hearsight/English/walk/walk.py")
            self.play_audio.play_machine_audio("Thank You.mp3")

        elif feature_name == "money":
#            os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")
#            self.handle_money_feature()
            self.mon_obj.pred_1()
            self.play_audio.play_machine_audio("Thank You.mp3")
            
        elif feature_name == "colors":
#            os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")
            self.color_obj.color_det()
            self.play_audio.play_machine_audio("Thank You.mp3")

#        elif feature_name == "Add_face":
#            os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")
#            self.handle_face_feature()
            
        elif feature_name == "settings":
#            os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")
            self.settings()

        elif feature_name == "person":
#            os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")
            self.handle_face_feature()
#            self.face_obj.recognize()
#            self.play_audio.play_machine_audio("Thank You.mp3")

        elif feature_name == "hearsight_storage":
#            os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")
            self.hearsight_storage()

        elif feature_name == "what":
#            os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")
            self.what_obj.detect()
            self.play_audio.play_machine_audio("Thank You.mp3")
            
        elif feature_name == "read":
            os.system("python /home/rock/Desktop/Hearsight/English/read/read.py")
            self.play_audio.play_machine_audio("Thank You.mp3")
            
        elif feature_name == "hearsight_app":
            os.system("python /home/rock/Desktop/Hearsight/English/hearsight_app/hearsight_app.py")
            self.play_audio.play_machine_audio("Thank You.mp3")

#        elif feature_name in ["go_see", "voice", "scan", "temperature", "off"]:
#            self.handle_other_features(feature_name)
            
        elif feature_name in ["go_see", "voice", "off"]:
            self.handle_other_features(feature_name)
        
#        elif feature_name in ["document", "book", "worksheet", "bank"]:
#        elif feature_name in ["document", "media"]:
#            self.handle_read_features(feature_name)

#        elif feature_name == "off":
#            os.system("python /home/rock/Desktop/Hearsight/English/off/off.py")
                 
#    def handle_money_feature(self):
#        counts = 1
#        self.play_audio.play_machine_audio("press_feature_button.mp3")
#    
#        while True:
#            input_state1 = GPIO.input(450)
#            input_state2 = GPIO.input(421)
#            input_state3 = GPIO.input(447)
#            input_state4 = GPIO.input(448)
#            
#            if input_state1:
#                counts = (counts + 1) % 2
#                self.play_audio.play_machine_audio("single.mp3" if counts == 0 else "multi.mp3")
#            
#            if input_state2:
#                counts = (counts - 1) % 2
#                self.play_audio.play_machine_audio("single.mp3" if counts == 0 else "multi.mp3")
#                
#            if input_state3 == True and counts == 0:
#                self.play_audio.play_machine_audio("feature_confirmed.mp3")
#                self.mon_obj.pred()
#                break    
#            
#            if input_state3 == True and counts == 1:
#                self.play_audio.play_machine_audio("feature_confirmed.mp3")
#                self.mon_obj.pred_1()
#                break
#        
#            if input_state4 == True:
#                self.play_audio.play_machine_audio("exit_button_pressed.mp3")
#                break
#            
#        self.play_audio.play_machine_audio("Thank You.mp3")

    def handle_face_feature(self):
        counts = -1
        self.play_audio.play_machine_audio("press_feature_button.mp3")
    
        while True:
            input_state1 = GPIO.input(450)
            input_state2 = GPIO.input(421)
            input_state3 = GPIO.input(447)
            input_state4 = GPIO.input(448)
            
            if input_state1:
                counts = (counts + 1) % 3
#                self.play_audio.play_machine_audio("Add_face.mp3" if counts == 0 else "delete face.mp3")
                self.play_audio.play_machine_audio("Add_face.mp3" if counts == 0 else "who_is_this.mp3" if counts == 1 else "delete face.mp3")
            
            if input_state2:
                counts = (counts - 1) % 3
                self.play_audio.play_machine_audio("Add_face.mp3" if counts == 0 else "who_is_this.mp3" if counts == 1 else "delete face.mp3")
                
            if input_state3 == True and counts == 0:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                    
#                while len(self.face_obj.persons) <= 200:
                self.face_obj.add_person()
                self.play_audio.play_machine_audio("Thank You.mp3")
#                    break
#                break
            
            if input_state3 == True and counts == 1:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.face_obj.recognize()
                self.play_audio.play_machine_audio("Thank You.mp3")
#                break
            
            if input_state3 == True and counts == 2:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.face_obj.remove_person()
                self.play_audio.play_machine_audio("Thank You.mp3")
#                break
        
            if input_state4 == True:
                self.play_audio.play_machine_audio("feature_exited.mp3")
                self.play_audio.play_machine_audio("Thank You.mp3")
                break
            
#        self.play_audio.play_machine_audio("Thank You.mp3")

    def settings(self):
        counts = -1
        self.play_audio.play_machine_audio("press_feature_button.mp3")
    
        while True:
            input_state1 = GPIO.input(450)
            input_state2 = GPIO.input(421)
            input_state3 = GPIO.input(447)
            input_state4 = GPIO.input(448)
            
            if input_state1:
                counts = (counts + 1) % 5  # Use % 5 since you have 5 cases
                audio_files = [
                    "change_language.mp3",
                    "user_guide.mp3",
                    "volume.mp3",
                    "battery_percentage.mp3",
                    "temperature.mp3"
                ]
                audio_file = audio_files[counts]
                self.play_audio.play_machine_audio(audio_file)

            if input_state2:
                counts = (counts - 1) % 5  # Use % 5 since you have 5 cases
                audio_files = [
                    "change_language.mp3",
                    "user_guide.mp3",
                    "volume.mp3",
                    "battery_percentage.mp3",
                    "temperature.mp3"
                ]
                audio_file = audio_files[counts]
                self.play_audio.play_machine_audio(audio_file)
                
            if input_state3 == True and counts == 0:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.lang_obj.handle_lang()
                self.play_audio.play_machine_audio("Thank You.mp3") 
#                break
            
            if input_state3 == True and counts == 1:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/Hearsight/English/user_guide/user_guide.py")
                self.play_audio.play_machine_audio("Thank You.mp3") 
#                break
            
            if input_state3 == True and counts == 2:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/Hearsight/English/volume/volume.py")
                self.play_audio.play_machine_audio("Thank You.mp3") 
#                break
            
            if input_state3 == True and counts == 3:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/Hearsight/English/battery/battery_mean.py")
                os.system("python /home/rock/Desktop/Hearsight/English/battery/battery_raw.py")
                self.play_audio.play_machine_audio("Thank You.mp3") 
#                break
            
            if input_state3 == True and counts == 4:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/Hearsight/English/temperature/temperature.py")
                self.play_audio.play_machine_audio("Thank You.mp3") 
#                break
                    
            if input_state4 == True:
                self.play_audio.play_machine_audio("feature_exited.mp3")
                self.play_audio.play_machine_audio("Thank You.mp3")
                break
            
#        self.play_audio.play_machine_audio("Thank You.mp3")
                
    def handle_other_features(self, feature_name):  
        if feature_name != "off" and feature_name != "voice":
#            os.system("python /home/rock/Desktop/Hearsight/camera_reload.py")
            os.system(f"python /home/rock/Desktop/Hearsight/English/{feature_name}/{feature_name}.py")
            self.play_audio.play_machine_audio("Thank You.mp3")

        if feature_name == "voice":
            os.system("python /home/rock/Desktop/Hearsight/voice.py")
            self.play_audio.play_machine_audio("press your feature button now.mp3")

        if feature_name == "off":
            os.system("python /home/rock/Desktop/Hearsight/English/off/off.py")

    def hearsight_storage(self):
        counts = 0
        self.play_audio.play_machine_audio("press_feature_button.mp3")
        
        while True:
            input_state1 = GPIO.input(450)
            input_state2 = GPIO.input(421)
            input_state3 = GPIO.input(447)
            input_state4 = GPIO.input(448)
        
            if input_state1:
#                sleep(1)
                counts = (counts + 1) % 2
                self.play_audio.play_machine_audio("document.mp3" if counts == 1 else "media.mp3")

            if input_state2:
#                sleep(1)
                counts = (counts - 1) % 2
                self.play_audio.play_machine_audio("document.mp3" if counts == 1 else "media.mp3")

            if input_state3 and counts == 1:
#                sleep(1)
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.handle_document_features()
#                self.online_feature_obj.play_audio(feature_name)
#                self.play_audio.play_machine_audio("Thank You.mp3")
#                break

            if input_state3 and counts == 0:
#                sleep(1)
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.handle_media_features()
#                self.online_feature_obj.remove_file(feature_name)
#                self.play_audio.play_machine_audio("Thank You.mp3")
#                break
            
            if input_state4:
#                sleep(1)
                self.play_audio.play_machine_audio("feature_exited.mp3")
                self.play_audio.play_machine_audio("Thank You.mp3")
                break

    def handle_document_features(self):
        counts = 0
        self.play_audio.play_machine_audio("press_feature_button.mp3")
        
        while True:
            input_state1 = GPIO.input(450)
            input_state2 = GPIO.input(421)
            input_state3 = GPIO.input(447)
            input_state4 = GPIO.input(448)
        
            if input_state1:
#                sleep(1)
                counts = (counts + 1) % 2
                self.play_audio.play_machine_audio("read_document.mp3" if counts == 1 else "delete_document.mp3")

            if input_state2:
#                sleep(1)
                counts = (counts - 1) % 2
                self.play_audio.play_machine_audio("read_document.mp3" if counts == 1 else "delete_document.mp3")

            if input_state3 and counts == 1:
#                sleep(1)
                feature_name = "document"
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.online_feature_obj.play_audio(feature_name)
                self.play_audio.play_machine_audio("Thank You.mp3")
                break

            if input_state3 and counts == 0:
#                sleep(1)
                feature_name = "document"
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.online_feature_obj.remove_file(feature_name)
                self.play_audio.play_machine_audio("Thank You.mp3")
                break
            
            if input_state4:
#                sleep(1)
                self.play_audio.play_machine_audio("exit_document.mp3")
                self.play_audio.play_machine_audio("Thank You.mp3")
                break
            
    def handle_media_features(self):
        counts = 0
        self.play_audio.play_machine_audio("press_feature_button.mp3")
        
        while True:
            input_state1 = GPIO.input(450)
            input_state2 = GPIO.input(421)
            input_state3 = GPIO.input(447)
            input_state4 = GPIO.input(448)
        
            if input_state1:
#                sleep(1)
                counts = (counts + 1) % 2
                self.play_audio.play_machine_audio("read_media.mp3" if counts == 1 else "delete_media.mp3")

            if input_state2:
#                sleep(1)
                counts = (counts - 1) % 2
                self.play_audio.play_machine_audio("read_media.mp3" if counts == 1 else "delete_media.mp3")

            if input_state3 and counts == 1:
#                sleep(1)
                feature_name = "media"
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.online_feature_obj.play_audio(feature_name)
                self.play_audio.play_machine_audio("Thank You.mp3")
                break

            if input_state3 and counts == 0:
#                sleep(1)
                feature_name = "media"
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.online_feature_obj.remove_file(feature_name)
                self.play_audio.play_machine_audio("Thank You.mp3")
                break
            
            if input_state4:
#                sleep(1)
                self.play_audio.play_machine_audio("exit_media.mp3")
                self.play_audio.play_machine_audio("Thank You.mp3")
                break
                
    def run(self):
        self.play_audio.play_machine_audio("welcome to hearsight audio vision for the visually impaired.mp3")
        self.play_audio.play_machine_audio("press your feature button now.mp3")

        while True:
            input_state1 = GPIO.input(450)
            input_state2 = GPIO.input(421)

            if input_state1:
                self.rotate_feature(1)

            if input_state2:
                self.rotate_feature(-1)

            self.confirm_action()

if __name__ == "__main__":
    atexit.register(cleanup)
    hearsight = HearsightAudioVision()
    hearsight.run()
