import subprocess
import platform
import urllib.parse


class TalkToMe:
    @staticmethod
    def speak(text: str):
        if platform.system() == 'Windows':
            subprocess.run(['tools/vlc-3.0.11/vlc', '-I dummy', '--dummy-quiet',
                            'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q='+urllib.parse.quote(text)+'&tl=en', 'vlc://quit'])
        else:
            subprocess.run(['/usr/bin/mplayer', '-ao alsa', '-really-quiet', '-noconsolecontrols',
                            'http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q='+urllib.parse.quote(text)+'&tl=en'])