from config import VOICE_APP_ID, VOICE_API_KEY, VOICE_SECRET_KEY
from config import NLP_APP_ID, NLP_API_KEY, NLP_SECRET_KEY

from err_no import err_no
from gcai import GCAI, KEYS
from sound import Player, Recorder
from utils import timestamp
from voice import Voice

from pydub import AudioSegment

import os
import time
import wave

class Robot(GCAI):
    def __init__(self, name):
        self.name = name
        self.ai = GCAI(qad = {'你是谁': '我是' + self.name, self.name: '干什么',})
        self.voice = Voice(VOICE_APP_ID, VOICE_API_KEY, VOICE_SECRET_KEY)
        self.nlp = NLP(NLP_APP_ID, NLP_API_KEY, NLP_SECRET_KEY)

    def chat(self):
        default_res = '听不懂'
        stop = False

        while not stop:
            rec_filename = self.voice.listen()
            r = self.voice.stt(rec_filename)
            os.remove(rec_filename)
            eno = r.get('err_no')
            if 0 == eno:
                txt = r.get('result')
                if (txt is not None) and (0 < len(r)):
                    t = txt[0]
                else:
                    t = ''
                print(t)
                res = self.voice.answer(t)
            else:
                res = err_no.get(eno, default_res)
            res = res.strip()
            if '' == res:
                res = default_res
            reply_filename = self.voice.tts(res, 'reply_' + timestamp() + '.wav')
            Player.play(reply_filename)
            os.remove(reply_filename)

            stop = ('再见' == res)


if __name__ == "__main__":
    prime = Robot('大丞相')
    prime.chat()