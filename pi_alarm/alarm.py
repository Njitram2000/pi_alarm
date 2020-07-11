import datetime
from datetime import date
from pi_alarm.talk_to_me import TalkToMe
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from pi_alarm.mpd_client import AlarmMPDClient
from typing import Final


class WakeupTime:
    def __init__(self, hours: int, minutes: int) -> None:
        self.__hours = hours
        self.__minutes = minutes
    
    @property
    def hours(self):
        return self.__hours

    @property
    def minutes(self):
        return self.__minutes

class Alarm:
    JOB_ID: Final = 'wakeup'

    def __init__(self, mpd_client: AlarmMPDClient):
        self.__wakeup_time: WakeupTime = None
        self.__mpd_client = mpd_client
        self.__scheduler = BackgroundScheduler()
        self.__scheduler.start()
        self.__reset_alarm()

    @property
    def wakeup_time(self):
        if self.__wakeup_time is not None:
            return self.__wakeup_time
        else:
            # Default wakeup time is midnight
            return WakeupTime(0, 0)

    @wakeup_time.setter
    def wakeup_time(self, wakeup_time: WakeupTime):
        if wakeup_time.hours == 99 and wakeup_time.minutes == 99:
            self.__disable_alarm()
            TalkToMe.speak('Disabled')
        elif wakeup_time.hours <= 23 and wakeup_time.minutes <= 59:
            self.__wakeup_time = wakeup_time
            self.__reset_alarm()
            TalkToMe.speak('Now set to ' + self.__spoken_wakeup_time())
        else:
            TalkToMe.speak('Invalid time. Still set to ' + self.__spoken_wakeup_time())

    def __spoken_wakeup_time(self):
        if self.wakeup_time.hours == 0 and self.wakeup_time.minutes == 0:
            return 'midnight'
        elif self.__is_disabled():
            return 'disabled'
        else:
            return str(self.wakeup_time.hours) + ' ' + str(self.wakeup_time.minutes)


    @property
    def __next_wakeup_time(self) -> datetime:
        now = datetime.datetime.now()
        # Apply the set hours and minutes to today's date and set seconds to 0
        new_wakeup_time = now.replace(hour=self.wakeup_time.hours, minute=self.wakeup_time.minutes, second=0, microsecond=0)
        # If wakeup time for today has already passed, set to for tomorrow
        if new_wakeup_time < now:
            new_wakeup_time += datetime.timedelta(days=1)
        return new_wakeup_time

    def __reset_alarm(self):
        self.__scheduler.add_job(self.__ring_alarm, 'date', run_date=self.__next_wakeup_time, id=self.JOB_ID, replace_existing=True)

    def __ring_alarm(self):
        self.__mpd_client.play()
        self.__reset_alarm()

    def __disable_alarm(self):
        try:
            self.__scheduler.remove_job(self.JOB_ID)
        except JobLookupError as e:
            pass
    
    def __is_disabled(self):
        return self.__scheduler.get_job(self.JOB_ID) is None

