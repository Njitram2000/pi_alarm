from mpd import MPDClient


class Alarm:
    def __init__(self):
        self.client = MPDClient()
        self.client.timeout = 10  # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None  # timeout for fetching the result of the idle command is handled seperately, default: None
        self.client.connect("localhost", 6600)  # connect to localhost:6600
        print(self.client.play())
        self.client.close()  # send the close command
        self.client.disconnect()  # disconnect from the server
