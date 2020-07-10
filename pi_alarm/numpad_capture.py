from pi_alarm.alarm_mpd_client import AlarmMPDClient
import keyboard
import platform
import subprocess

from apscheduler.schedulers.background import BackgroundScheduler


class NumpadCapture:
    def __init__(self, mpd_client: AlarmMPDClient):
        self.mpd_client = mpd_client
        self.isWindows = platform.system() == 'Windows'
        # self.scheduler = BackgroundScheduler()
        # self.job = self.scheduler.add_job(self.printMe, 'interval', seconds=1)
        # self.scheduler.add_job(printMe, 'date')
        # self.scheduler.start()
        # self.job.remove()
        keyboard.on_release(lambda e: self.processKey(e.name, e.scan_code))
        keyboard.wait('esc')

    def processKey(self, name, scan_code):
        if name == 'enter':
            self.mpd_client.play_pause()
        elif name == 'backspace':
            self.mpd_client.stop()
        elif name == '-':
            self.mpd_client.prev_song()
        elif name == '+':
            self.mpd_client.next_song()
        elif name == '+':
            self.mpd_client.next_song()
        elif name == 'right':
            self.mpd_client.next_playlist()
        elif name == 'left':
            self.mpd_client.prev_playlist()
        # *
        elif scan_code == 55:
            # cancel
            i = 0
        # / on windows
        elif scan_code == 53 & self.isWindows == True:
            # set time
            i = 0
            # subprocess.run(['tools/vlc-3.0.11/vlc', '-I dummy', '--dummy-quiet', 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q='+name+'&tl=en', 'vlc://quit'])
        # / on linux
        elif scan_code == 98 & self.isWindows == False:
            # set time
            i = 0
            # subprocess.run(['tools/vlc-3.0.11/vlc', '-I dummy', '--dummy-quiet', 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q='+name+'&tl=en', 'vlc://quit'])
        else:
            try:
                number = int(name)
                # process number input
            except ValueError as e:
                pass
