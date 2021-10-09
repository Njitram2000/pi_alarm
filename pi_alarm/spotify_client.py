import requests


class SpotifyClient:
  BASE_URL = 'http://localhost:24879'
  PLAYER_URL = BASE_URL + '/player'
  PLAYLIST_ID = 'spotify:playlist:7i067dOx4lUCBeewVE1wem'

  def __init__(self) -> None:
    self.__isPlaying = False
    self.__reset()

  def __checkPlayer(self):
    resp = self.__sendRequest(SpotifyClient.PLAYER_URL + '/status', False)
    # 500 means the client is not the one connected to spotify atm
    if resp.status_code != 200:
      self.__reset()

  # To reset, load the playlist (look up the id in a real spotify client) and do not play. From that point the play status is known
  def __reset(self):
    self.__sendRequest(SpotifyClient.PLAYER_URL + '/load?uri=' + SpotifyClient.PLAYLIST_ID +'&play=false', False)
    self.__isPlaying = False

  def __sendRequest(self, url, check_player:bool=True):
    if check_player:
      self.__checkPlayer()
    resp = requests.post(url)
    return resp.status_code == 200

  def play(self):
    self.__sendRequest(SpotifyClient.PLAYER_URL + '/resume')
    self.__isPlaying = True

  def pause(self):
    self.__sendRequest(SpotifyClient.PLAYER_URL + '/pause')
    self.__isPlaying = False

  def play_pause(self):
    if self.__isPlaying:
      self.pause()
    else:
      self.play()

  def next(self):
    self.__sendRequest(SpotifyClient.PLAYER_URL + '/next')
