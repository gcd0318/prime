from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
sys.path.append(os.path.abspath('..'))
import time
import wave

from aip import AipSpeech
from pydub import AudioSegment

from config import TMP_PATH
from .sound import Player, Recorder
from base.utils import timestamp

class Voice(object):

    def __init__(self, regs):
        self.rec = Recorder()
        app_id, api_key, secret_key = regs
        self.client = AipSpeech(app_id, api_key, secret_key)

    def listen(self):
        input('enter to start:')
        begin = time.time()
        print("Start recording")
        self.rec.start()
        input('enter to stop:')
        print("Stop recording")
        self.rec.stop()
        print('录音时间为: ', time.time() - begin, 'secs')
        rec_filename = TMP_PATH + 'rec_' + timestamp() + '.wav'
        self.rec.save(rec_filename)
        return rec_filename

    def stt(self, filename):
        res = None
        f = None
        with open(filename, 'rb') as fp:
            f = fp.read()
        if f is not None:
            res = self.client.asr(f, 'wav', 16000, {'dev_pid': 1536,})
        return res

    def tts(self, txt, filename):
        mp3_name = TMP_PATH + filename + '.mp3'
        r = self.client.synthesis(txt,'zh', 1, {'vol': 5, 'per': 1,})

        if not isinstance(r, dict):
            with open(mp3_name, 'wb') as f:
                f.write(r)
        sound = AudioSegment.from_file(mp3_name, format = 'MP3')
        os.remove(mp3_name)
        wav_filename = TMP_PATH + filename
        wav = wave.open(wav_filename, 'wb')
        wav.setnchannels(1)   # 频道数
        wav.setsampwidth(2)   # 量化位数
        wav.setframerate(16000)   # 取样频率
        wav.setnframes(len(sound._data))   # 取样点数，波形数据的长度
        wav.writeframes(sound._data)   # 写入波形数据
        wav.close()

        return wav_filename

