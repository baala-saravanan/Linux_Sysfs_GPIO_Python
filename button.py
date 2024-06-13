import numpy as np
from time import sleep
import vlc
import gpio as GPIO
import os
import time
import sys
import atexit
import subprocess
from what.what import SSD
from money.yolov5.money import Money
from online_features.online_feature import Reader
from change_language.change_language import CHLANG
from play_audio import GTTSA
from pydub import AudioSegment
from config import *
from set_face_who.Add_Face import Recognizer
from voice import Voice_Recognizer
from env.say import tts

# Clear and refresh cache memory with sudo
subprocess.run(["sudo", "sync"])
subprocess.run(["sudo", "sh", "-c", "echo 1 > /proc/sys/vm/drop_caches"])
os.system("python /home/rock/Desktop/HS/env/camera_reload.py")

def cleanup():
    os.system("python /home/rock/Desktop/HS/env/tts.py")
        
class HearsightAudioVision:
    def __init__(self):
        self.count = -1
        
        self.feature_names = [
            "HearSight Vision AI", "visionary_ai_stream", "HearSight Voice Assistive AI", "walk", "go_see", "what", "money", "person", "colors", "read","time_and_date", "settings", "off",
        ]
        
        GPIO.setup([450, 421, 447, 448, 502], GPIO.IN)
        self.what_obj = SSD()
        self.face_obj = Recognizer()
        self.mon_obj = Money()
#        #self.online_feature_obj = Reader()
#        #self.color_obj = Color_detection()
##        self.machineVoice_obj = MachineVoices()
        self.play_audio = GTTSA()
        self.lang_obj = CHLANG()
        self.voice_obj = Voice_Recognizer()
        
    def confirm_action(self):
        if GPIO.input(447):
            sleep(0.1)
            feature_name = self.feature_names[self.count]
            self.play_audio.play_machine_audio("feature_confirmed.mp3")
            self.handle_feature(feature_name)
            
    def rotate_feature(self, direction):
        self.count = (self.count + direction) % len(self.feature_names)
        print(self.count)
        self.play_audio.play_machine_audio("{}.mp3".format(self.feature_names[self.count]))

    def handle_feature(self, feature_name):
        
        if feature_name == "HearSight Vision AI":
            os.system("python3.9 /home/rock/Desktop/HS/vision/vision2.0.py")
            self.play_audio.play_machine_audio("Thank You.mp3")
                
        elif feature_name == "visionary_ai_stream":
            env_path = "env_httpx_0_13_3"
            python_cmd = f"{env_path}/bin/python3.9 /home/rock/Desktop/HS/visionary_ai_stream/visionary_AI_stream.py"
            subprocess.run(python_cmd, shell=True)

            self.play_audio.play_machine_audio("Thank You.mp3")

        elif feature_name == "HearSight Voice Assistive AI":
            os.system("python3.9 /home/rock/Desktop/HS/chatbot/chatai.py")
            self.play_audio.play_machine_audio("Thank You.mp3")

        elif feature_name == "time_and_date":
            os.system("python /home/rock/Desktop/HS/time/time.py")
            #self.time_obj.tellTime()
            self.play_audio.play_machine_audio("Thank You.mp3")
        
        elif feature_name == "walk":
            sleep(3)
            os.system("python /home/rock/Desktop/HS/walk/walk.py")
            self.play_audio.play_machine_audio("Thank You.mp3")

        elif feature_name == "money":
            self.mon_obj.pred_1()
            self.play_audio.play_machine_audio("Thank You.mp3")
            
        elif feature_name == "colors":
            os.system("python /home/rock/Desktop/HS/colors/colors.py")
            self.play_audio.play_machine_audio("Thank You.mp3")

        elif feature_name == "settings":
            self.settings()

        elif feature_name == "person":
            self.handle_face_feature()

        elif feature_name == "what":
            self.what_obj.detect()
            self.play_audio.play_machine_audio("Thank You.mp3")
            
        elif feature_name == "read":
            os.system("python /home/rock/Desktop/HS/read/read.py")
            self.play_audio.play_machine_audio("Thank You.mp3")
            
        elif feature_name == "hearsight_app":
            os.system("python /home/rock/Desktop/HS/hearsight_app/hearsight_app.py")
            self.play_audio.play_machine_audio("Thank You.mp3")
            
        elif feature_name in ["go_see","off"]:
            self.handle_other_features(feature_name)

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
                self.play_audio.play_machine_audio("Add_face.mp3" if counts == 0 else "who_is_this.mp3" if counts == 1 else "delete face.mp3")
            
            elif input_state2:
                counts = (counts - 1) % 3
                self.play_audio.play_machine_audio("Add_face.mp3" if counts == 0 else "who_is_this.mp3" if counts == 1 else "delete face.mp3")
                
            elif input_state3 == True and counts == 0:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                    
#                while len(self.face_obj.persons) <= 200:
                self.face_obj.add_person()
                self.play_audio.play_machine_audio("Thank You.mp3")
#                    break
#                break
            
            elif input_state3 == True and counts == 1:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.face_obj.recognize()
                self.play_audio.play_machine_audio("Thank You.mp3")
#                break
            
            elif input_state3 == True and counts == 2:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.face_obj.remove_person()
                self.play_audio.play_machine_audio("Thank You.mp3")
#                break
        
            elif input_state4 == True:
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
                counts = (counts + 1) % 6  # Use % 5 since you have 5 cases
                audio_files = [
                    "change_language.mp3",
                    "user_guide.mp3",
                    "volume.mp3",
                    "battery_percentage.mp3",
                    "temperature.mp3",
                    "wifi_setup.mp3"
                ]
                audio_file = audio_files[counts]
                self.play_audio.play_machine_audio(audio_file)

            if input_state2:
                counts = (counts - 1) % 6  # Use % 5 since you have 5 cases
                audio_files = [
                    "change_language.mp3",
                    "user_guide.mp3",
                    "volume.mp3",
                    "battery_percentage.mp3",
                    "temperature.mp3",
                    "wifi_setup.mp3"
                ]
                audio_file = audio_files[counts]
                self.play_audio.play_machine_audio(audio_file)
                
            if input_state3 == True and counts == 0:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                self.lang_obj.handle_lang()
                self.play_audio.play_machine_audio("Thank You.mp3") 
            
            if input_state3 == True and counts == 1:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/HS/user_guide/user_guide.py")
                self.play_audio.play_machine_audio("Thank You.mp3") 
            
            if input_state3 == True and counts == 2:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/HS/volume/volume.py")
                self.play_audio.play_machine_audio("Thank You.mp3") 
            
            if input_state3 == True and counts == 3:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/HS/battery_percentage/battery_percentage.py")
                self.play_audio.play_machine_audio("Thank You.mp3")
            
            if input_state3 == True and counts == 4:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/HS/temperature/temperature.py")
                self.play_audio.play_machine_audio("Thank You.mp3")
                            
            if input_state3 == True and counts == 5:
                self.play_audio.play_machine_audio("feature_confirmed.mp3")
                os.system("python /home/rock/Desktop/HS/wifi_setup/wifi_setup.py")
                self.play_audio.play_machine_audio("Thank You.mp3")
                    
            if input_state4 == True:
                self.play_audio.play_machine_audio("feature_exited.mp3")
                self.play_audio.play_machine_audio("Thank You.mp3")
                break
                
    def handle_other_features(self, feature_name):  
        if feature_name != "off":
            os.system(f"python /home/rock/Desktop/HS/{feature_name}/{feature_name}.py")
            self.play_audio.play_machine_audio("Thank You.mp3")

        if feature_name == "off":
            os.system("python /home/rock/Desktop/HS/off/off.py")
            self.play_audio.play_machine_audio("Thank You.mp3")
            
    def voice_callback(self):
        input_state3 = GPIO.input(502)
        if not input_state3:  # Button pressed
            self.play_audio.play_machine_audio("Mic_Activated.wav")
            self.voice_obj.recording = True
            match, conf = self.voice_obj.recognize()
            if match in self.feature_names and conf > 60:
                print(f"{match} feature activated")
                self.play_audio.play_machine_audio(f"{match}.mp3")
                self.handle_feature(feature_name = match)
                
            elif match in ["change_language","user_guide","volume","battery_percentage","temperature","wifi_setup","off_device"]:
                if match == "off_device":
                    match = "off"
                print(f"{match} feature activated")
                self.play_audio.play_machine_audio(f"{match}.mp3")
                if match == "change_language":
                    self.lang_obj.handle_lang()
                else:
                    self.handle_other_features(match)
                
            elif match == "who_is_this":
                print(f"{match} feature activated")
                self.play_audio.play_machine_audio(f"{match}.mp3")
                self.face_obj.recognize()
                self.play_audio.play_machine_audio("Thank You.mp3")
                                               
            else:
                e = "sorry, can't understand you clearly, please check your mic and try again"
                tts(e)
        else:
            self.voice_obj.recording = False
#            print("stop recording")
                 
                
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
            
            #Voice
            self.voice_callback()

if __name__ == "__main__":
    atexit.register(cleanup)
    hearsight = HearsightAudioVision()
    hearsight.run()
