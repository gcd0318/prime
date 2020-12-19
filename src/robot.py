from config import TMP_PATH, FACE_REGS, VOICE_REGS, NLP_REGS

from face import Face
from base.gcai import GCAI, KEYS
from gcutils import timestamp
from nlp import NLP
from voice import Voice
from voice.sound import Player, Recorder

import os
import time

class Robot(GCAI):
    def __init__(self, name):
        self.name = name
        self.ai = GCAI(qad = {'你是谁': '我是' + self.name, self.name: '干什么',})
        self.voice = Voice(VOICE_REGS)
        self.nlp = NLP(NLP_REGS)

    def chat(self):
        res = '听不懂'
        stop = False

        while not stop:
            rec_filename = self.voice.listen()
            r = self.voice.stt(rec_filename)
            os.remove(rec_filename)
            if 0 == r.get('err_no'):
                txt = r.get('result')
                if (txt is not None) and (0 < len(r)):
                    t = txt[0]
                else:
                    t = ''
                print(t)
                res = self.ai.answer(t)
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
