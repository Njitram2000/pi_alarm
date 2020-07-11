from pi_alarm.mpd_client import AlarmMPDClient
from pi_alarm.numpad_capture import NumpadCapture
from pi_alarm.alarm import Alarm


def main():
    client = AlarmMPDClient()
    alarm = Alarm(client)
    NumpadCapture(client)


# Will only be true if this is the class called by python.
if __name__ == "__main__":
    main()
