from mpd import MPDClient

class AlarmMPDClient:
    def __init__(self):
        self.client = MPDClient()
        self.client.timeout = 10  # network timeout in seconds (floats allowed), default: None
        self.client.idletimeout = None  # timeout for fetching the result of the idle command is handled seperately, default: None
    
    def connect(self):
        self.client.connect("localhost", 6600)  # connect to localhost:6600
        
    def disconnect(self):
        self.client.close()
        self.client.disconnect()  # disconnect from the server

    def play_pause(self):
        status = self.client.status()
        if status['state'] == 'stop' or status['state'] == 'pause':
            self.client.play()
        else:
            self.client.pause()
    
    def stop(self):
        self.client.stop()
        
    def prev_song(self):
        self.client.previous()

    def next_song(self):
        self.client.next()

    def get_current_playlist(self):
        return self.client.playlist()

    def next_playlist(self):
        current_playlist = self.get_current_playlist()
        print(current_playlist)
        # playlist_id = current_playlist['playlist']
        # print(playlist_id)
        # self.client.clear()
        # self.client.load('Jojo')
        # print(self.client.playlist())
        # print(self.client.listplaylists()[1]['playlist'])
        
    def prev_playlist(self):
        i = 0