import keyboard
import platform
import subprocess

class NumpadCapture:
  def __init__(self):  # TODO: add class to call
    self.isWindows = platform.system() == 'windows'
    keyboard.on_release(lambda e: self.processKey(e.name, e.scan_code))
    keyboard.wait('esc')

  def processKey(self, name, scan_code):
    print(name)
    if self.isWindows:
      subprocess.run(['tools/vlc-3.0.11/vlc', '-I dummy', '--dummy-quiet', 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q='+name+'&tl=en', 'vlc://quit'])
    else:
      # speech.sh
      subprocess.run(['tools/vlc-3.0.11/vlc', '-I dummy', '--dummy-quiet', 'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q='+name+'&tl=en', 'vlc://quit'])

