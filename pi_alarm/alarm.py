import datetime
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from pi_alarm.mpd_client import AlarmMPDClient
from typing import Final


class Alarm:
    JOB_ID: Final = 'wakeup'

    def __init__(self, mpd_client: AlarmMPDClient):
        self.wakeup_time = {
            'hour': 15,
            'minute': 3
        }
        self.mpd_client = mpd_client
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.set_alarm()

    def get_wakeup_time(self) -> datetime:
        now = datetime.datetime.now()
        # Apply the set hours and minutes to today's date and set seconds to 0
        wakeup_time = now.replace(hour=self.wakeup_time['hour'], minute=self.wakeup_time['minute'], second=0, microsecond=0)
        # If wakeup time for today has already passed, set to for tomorrow
        if wakeup_time < now:
            wakeup_time += datetime.timedelta(days=1)
        return wakeup_time

    def set_alarm(self):
        self.scheduler.add_job(self.ring_alarm, 'date', run_date=self.get_wakeup_time(), id=self.JOB_ID, replace_existing=True)

    def ring_alarm(self):
        self.mpd_client.play()
        self.set_alarm()

    def disable_alarm(self):
        self.scheduler.remove_job(self.JOB_ID)
