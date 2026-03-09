import sounddevice as sd
import numpy as np
import threading

class AudioRecorder:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.recording = False
        self.audio_data = []
        self._thread = None

    def _record(self):
        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='float32') as stream:
            while self.recording:
                data, overflowed = stream.read(1024)
                if overflowed:
                    print("Audio buffer overflowed")
                self.audio_data.append(data)

    def start(self):
        if not self.recording:
            self.recording = True
            self.audio_data = []
            self._thread = threading.Thread(target=self._record)
            self._thread.start()
            print("Recording started...")

    def stop(self):
        if self.recording:
            self.recording = False
            self._thread.join()
            print("Recording stopped.")
            if not self.audio_data:
                return np.array([], dtype='float32')
            return np.concatenate(self.audio_data, axis=0).flatten()
        return np.array([], dtype='float32')

if __name__ == "__main__":
    import time
    recorder = AudioRecorder()
    recorder.start()
    time.sleep(2)
    data = recorder.stop()
    print(f"Recorded {len(data)} samples")
