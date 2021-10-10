from pi_alarm.talk_to_me import TalkToMe
from pi_alarm.config_mgr import CONFIG
import subprocess
import platform

class SleepHelper:
    def __init__(self):
        self.__vlcProcess = None
    
    def start(self):
        # Cannot have 2 processes running at the same time
        if self.isRunning():
            return
        
        if platform.system() == 'Windows':
            self.__vlcProcess = subprocess.Popen(['tools/vlc-3.0.11/vlc', '-I dummy', '--dummy-quiet',
                            '.\\audio_samples\\ocean_sample.mp3'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        else:
            # Make a symbolic link from /home/pi/audio/sleep_helper.mp3 to the actual audio file to easily switch which file to play
            self.__vlcProcess = subprocess.Popen(['cvlc', '--play-and-exit', '-I dummy', '--quiet', '--gain', self.gain,
                            '/home/pi/audio/sleep_helper.mp3'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    
    def stop(self):
        if self.isRunning():
           self.__vlcProcess.terminate()

    def isRunning(self) -> bool:
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
    @property
    def gain(self) -> str:
        return CONFIG.sleep_helper_gain

    def increaseGain(self):
        new_gain = float(CONFIG.sleep_helper_gain) + 0.01
        CONFIG.sleep_helper_gain = format(new_gain, '.2f')
        TalkToMe.speak(CONFIG.sleep_helper_gain)
    
    def decreaseGain(self):
        new_gain = float(CONFIG.sleep_helper_gain) - 0.01
        if(new_gain < 0):
            new_gain = 0
        CONFIG.sleep_helper_gain = format(new_gain, '.2f')
        TalkToMe.speak(CONFIG.sleep_helper_gain)