import pyaudio
import threading
import wave

class Player(object):
    @staticmethod
    def play(filename):
        chunk = 1024
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(
            format = p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True)
        data = wf.readframes(chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
        print('done')


class Recorder(object):
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
    def start(self):
        threading._start_new_thread(self.__recording, ())
    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while(self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
 
        stream.stop_stream()
        stream.close()
        p.terminate()
 
    def stop(self):
        self._running = False
 
    def save(self, filename):
        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
