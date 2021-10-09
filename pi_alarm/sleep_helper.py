import subprocess
import platform
import urllib.parse
import time
from datetime import datetime

class SleepHelper:
    def __init__(self):
        self.__vlcProcess = None
    
    def start(self):
        # Cannot have 2 processes running at the same time
        if self.isRunning():
            return
        
        testText = 'Hello world. I am the ruler and I am here to stay.'

        if platform.system() == 'Windows':
            self.__vlcProcess = subprocess.Popen(['tools/vlc-3.0.11/vlc', '-I dummy', '--dummy-quiet',
                            '.\\audio_samples\\ocean_sample.mp3'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        else:
            #subprocess.run(['cvlc', '--play-and-exit', '-I dummy', '--quiet', '--gain', '0.20',
            #                'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q='+urllib.parse.quote(testText)+'&tl=en'])
            self.__vlcProcess = subprocess.Popen(['cvlc', '--play-and-exit', '-I dummy', '--quiet', '--gain', '0.20',
                            '/home/pi/audio/ocean_10_hours.mp3'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    
    def stop(self):
        if self.isRunning():
           self.__vlcProcess.terminate()

    def isRunning(self):
        if self.__vlcProcess is None:
            return False
        else:
            # None means it is still running
            if self.__vlcProcess.poll() is None:
                return True
            else:
                # reset the member variable to have clean start
                self.__vlcProcess = None
                return False