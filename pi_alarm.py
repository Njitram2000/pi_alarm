from pi_alarm.config_mgr import CONFIG
from pi_alarm.mpd_client import AlarmMPDClient
from pi_alarm.numpad_capture import NumpadCapture
from pi_alarm.alarm import Alarm
from pi_alarm.sleep_helper import SleepHelper


def main():
    client = AlarmMPDClient()
    sleep_helper = SleepHelper()
    alarm = Alarm(client, sleep_helper)
    # # Call start last as it will pause the tread
    NumpadCapture(client, alarm, sleep_helper).start()


# Will only be true if this is the class called by python.
if __name__ == "__main__":
    main()
