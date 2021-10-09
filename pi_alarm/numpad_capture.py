from abc import ABC, abstractmethod
from pi_alarm.alarm import Alarm, WakeupTime
from pi_alarm.talk_to_me import TalkToMe
from pi_alarm.mpd_client import AlarmMPDClient
from pi_alarm.sleep_helper import SleepHelper
import keyboard
import platform


class NumpadCapture:
    def __init__(self, mpd_client: AlarmMPDClient, alarm: Alarm, sleep_helper: SleepHelper):
        self.__mpd_client = mpd_client
        self.__isWindows = platform.system() == 'Windows'
        self.__current_key_sequence: KeySequence = None
        self.__alarm = alarm
        self.__sleep_helper = sleep_helper
        keyboard.on_release(lambda e: self.processKey(e.name, e.scan_code))

    def start(self):
        print('Numpad ready')
        keyboard.wait('esc')

    def processKey(self, name, scan_code):
        # Will check if the connection has timed out and reconnect if needed
        self.__mpd_client.keep_alive()

        if name == 'enter':
            self.__mpd_client.play_pause()
        elif name == 'backspace':
            self.__mpd_client.stop()
            self.__sleep_helper.stop()
        elif name == '-':
            self.__mpd_client.prev_song()
        elif name == '+':
            self.__mpd_client.next_song()
        elif name == 'right':
            self.__mpd_client.next_playlist()
        elif name == 'left':
            self.__mpd_client.prev_playlist()
        elif name == 'up':
            self.__sleep_helper.increaseGain()
        elif name == 'down':
            self.__sleep_helper.decreaseGain()
        # *
        elif scan_code == 55:
            if self.__current_key_sequence is not None:
                self.__current_key_sequence = None
                TalkToMe.speak('Cancelled. Still set to ' + self.__alarm.spoken_wakeup_time())
        # / on windows
        elif scan_code == 53 and self.__isWindows == True:
            self.__input_time()
        # / on linux
        elif scan_code == 98 and self.__isWindows == False:
            self.__input_time()
            i = 0
        elif self.__current_key_sequence is not None:
            try:
                # check if it can be converted to int (so is number input)
                int(name)
                self.__current_key_sequence.input(name)
                if self.__current_key_sequence.isComplete():
                    self.__current_key_sequence.onComplete()
                    self.__current_key_sequence = None
            except ValueError as e:
                pass
        # Start sleep helper and stop alarm
        elif name == '0':
            self.__mpd_client.stop()
            self.__sleep_helper.start()
    
    def __input_time(self):
        self.__current_key_sequence = WakeupTimeKeySequence(self.__alarm)
        TalkToMe.speak('Set time')

class KeySequence(ABC):
    __sequence = []

    def __init__(self, max_length: int) -> None:
        self.__max_length = max_length

    def input(self, key: str):
        self.sequence = self.sequence + [key]

    def isComplete(self) -> bool:
        return len(self.__sequence) == self.__max_length

    @abstractmethod
    def onComplete(self):
        pass

    @property
    def sequence(self) -> str:
        return self.__sequence

    @sequence.setter
    def sequence(self, new_sequence):
        if not self.isComplete():
            self.__sequence = new_sequence


class WakeupTimeKeySequence(KeySequence):
    def __init__(self, alarm: Alarm) -> None:
        super().__init__(4)
        self.__alarm = alarm

    @property
    def wakeup_time(self) -> WakeupTime:
        if self.isComplete():
            return WakeupTime(int(''.join(self.sequence[0:2])), int(''.join(self.sequence[2:4])))
    
    def onComplete(self):
        print('on complete')
        wakeup_time = self.wakeup_time
        self.__alarm.wakeup_time = wakeup_time