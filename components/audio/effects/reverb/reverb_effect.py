import librosa
import soundfile as sf
import numpy as np
import pyroomacoustics as pra

class reverb_effect:
    def __init__(self, in_audio_file, out_audio_file):
        self.in_audio_file = in_audio_file
        self.out_audio_file = out_audio_file
        self.room_size = [0, 0, 0]
        self.room_type = pra.ShoeBox
        self.microphone_source = [0,0,0]
        self.reverb_absortion = 0

    def set_reverb_room_size(self, x, y, z):
        self.room_size = [x, y, z]

    def set_room_type(self, room_type):
        self.room_type = room_type

    def set_microphone_source(self, x, y, z):
        self.microphone_source = [x,y,z]

    def set_absorption(self, absortion):
        self.reverb_absortion = absortion

    def add_reverb_to_file(self):
        y, sr = librosa.load(self.in_audio_file)
        room_dim = self.room_size
        room = self.room_type(room_dim, fs=sr, max_order=15, absorption=self.reverb_absortion)
        room.add_source([2, 3, 2], signal=y)
        room.add_microphone_array(pra.MicrophoneArray(np.array([[7, 8, 1.5]]).T, room.fs))
        room.compute_rir()
        y_reverb = np.convolve(room.rir[0][0], y)
        # If necessary, normalize the output
        y_reverb /= np.max(np.abs(y_reverb))
        sf.write(self.out_audio_file, y_reverb, sr)
