import configparser
from pi_alarm.wakeup_time import WakeupTime
import threading


class ConfigMgr:
    __CONFIG_FILE = 'config.ini'
    __DISABLED = 'disabled'
    __HOURS = 'hours'
    __MINUTES = 'minutes'
    __SLEEP_HELPER_GAIN = 'sleep_helper_gain'
    __DEFAULT = 'config'

    def __init__(self) -> None:
        self.__lock = threading.RLock()
        self.__config = configparser.ConfigParser()
        self.__read()
        if ConfigMgr.__DEFAULT not in self.__config.sections():
            self.__config[ConfigMgr.__DEFAULT] = {
                ConfigMgr.__HOURS: '0',
                ConfigMgr.__MINUTES: '0',
                ConfigMgr.__DISABLED: 'False',
                ConfigMgr.__SLEEP_HELPER_GAIN: '0.20'
            }
            self.__write()

    def __read(self):
        self.__config.read(ConfigMgr.__CONFIG_FILE)

    def __write(self):
        with open(ConfigMgr.__CONFIG_FILE, 'w') as configfile:
            self.__config.write(configfile)

    def __set_value(self, key: str, value: str):
        # Only one value will be able to be written at a time, ensuring no data is lost by writing 2 updates at the same time, creating a race condition
        with self.__lock:
            self.__config[self.__DEFAULT][key] = str(value)
            self.__write()

    def __get_value(self, key: str):
        return self.__config[self.__DEFAULT][key]

    @property
    def disabled(self) -> bool:
        try:
            return self.__get_value(ConfigMgr.__DISABLED) == 'True'
        except KeyError as error:
            # If not set, default to False
            return False

    @disabled.setter
    def disabled(self, disabled: bool):
        self.__set_value(ConfigMgr.__DISABLED, disabled)

    @property
    def wakeup_time(self) -> WakeupTime:
        return WakeupTime(int(self.__get_value(ConfigMgr.__HOURS)), int(self.__get_value(ConfigMgr.__MINUTES)))

    @wakeup_time.setter
    def wakeup_time(self, wakeup_time: WakeupTime):
        self.__set_value(ConfigMgr.__HOURS, wakeup_time.hours)
        self.__set_value(ConfigMgr.__MINUTES, wakeup_time.minutes)
    
    @property
    def sleep_helper_gain(self) -> str:
        return self.__get_value(ConfigMgr.__SLEEP_HELPER_GAIN)

    @sleep_helper_gain.setter
    def sleep_helper_gain(self, gain: str):
        if float(gain) < 0:
            gain = '0'
        self.__set_value(ConfigMgr.__SLEEP_HELPER_GAIN, gain)
        print('new gain: ' + self.sleep_helper_gain)
        

#global singleton
CONFIG: ConfigMgr = ConfigMgr()