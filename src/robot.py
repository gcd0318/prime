from config import APP_ID, API_KEY, SECRET_KEY, SOUND_PATH
from err_no import err_no
from gcai import GCAI, KEYS
from sound import Player, Recorder
from utils import timestamp

from aip import AipSpeech
from pydub import AudioSegment

import os
import time
import wave

class Robot(GCAI):
    def __init__(self, name):
        GCAI.__init__(self)
        self.name = name
        self.rec = Recorder()
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    def listen(self):
        input('enter to start:')
        begin = time.time()
        print("Start recording")
        self.rec.start()
        input('enter to stop:')
        print("Stop recording")
        self.rec.stop()
        print('录音时间为: ', time.time() - begin, 'secs')
        rec_filename = SOUND_PATH + 'rec_' + timestamp() + '.wav'
        self.rec.save(rec_filename)
        return rec_filename


    def answer(self, msg=''):
        qad = {
            '你是谁': '我是' + self.name,
            self.name: '干什么',
            '你知道什么': ' '.join(KEYS),
            '没事了': '再见',
            '没事儿了': '再见',
            '': '听不懂'
        }

        res = qad.get(msg)

        if msg in KEYS:
            if '天气' in msg:
                res = self.get_weather()
            elif '时间' in msg:
                res = self.get_datetime()
        elif res is None:
            res = self.search(msg)
        return res

    def stt(self, filename):
        res = None
        f = None
        with open(filename, 'rb') as fp:
            f = fp.read()
        if f is not None:
            res = self.client.asr(f, 'wav', 16000, {'dev_pid': 1536,})
        return res

    def tts(self, txt, filename):
        mp3_name = SOUND_PATH + filename + '.mp3'
        r = self.client.synthesis(txt,'zh', 1, {'vol': 5, 'per': 1,})

        if not isinstance(r, dict):
            with open(mp3_name, 'wb') as f:
                f.write(r)
        sound = AudioSegment.from_file(mp3_name, format = 'MP3')
        os.remove(mp3_name)
        wav_filename = SOUND_PATH + filename
        wav = wave.open(wav_filename, 'wb')
        wav.setnchannels(1)   # 频道数
        wav.setsampwidth(2)   # 量化位数
        wav.setframerate(16000)   # 取样频率
        wav.setnframes(len(sound._data))   # 取样点数，波形数据的长度
        wav.writeframes(sound._data)   # 写入波形数据
        wav.close()

        return wav_filename

    def chat(self):
        default_res = '听不懂'
        stop = False

        while not stop:
            rec_filename = p.listen()
            r = p.stt(rec_filename)
            os.remove(rec_filename)
            eno = r.get('err_no')
            if 0 == eno:
                txt = r.get('result')
                if (txt is not None) and (0 < len(r)):
                    t = txt[0]
                else:
                    t = ''
                print(t)
                res = p.answer(t)
            else:
                res = err_no.get(eno, default_res)
            res = res.strip()
            if '' == res:
                res = default_res
            reply_filename = p.tts(res, 'reply_' + timestamp() + '.wav')
            Player.play(reply_filename)
            os.remove(reply_filename)

            stop = ('再见' == res)


if __name__ == "__main__":
    prime = Robot('大丞相')
    prime.chat()