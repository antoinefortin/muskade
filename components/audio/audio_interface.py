import librosa
import soundfile as sf
import numpy as np
import pyroomacoustics as pra
import random

class audio_interface:
    def __init__(self, in_file, in_buffer):
        self.in_file = in_file
        self.in_buffer = False
        self.original_audio_buffer = False
        self.sample_rate = False
        self.out_buffer = False

    def reasign_audio_interface_buffer(self, new_buffer):
        self.original_audio_buffer = new_buffer

    def load_buffer_from_audio(self):
        y, sr = librosa.load(self.in_file)
        self.original_audio_buffer = y
        self.sample_rate = sr
        print(sr)
        print(self.sample_rate)

    def apply_stretch(self, stretch_factor):
        print(self.original_audio_buffer)
        y_time_stretched = librosa.effects.time_stretch(self.original_audio_buffer, rate=stretch_factor)

        return y_time_stretched

    def apply_pitch(self, factor):
        y_tritone = librosa.effects.pitch_shift(self.original_audio_buffer, sr=self.sample_rate, n_steps=factor)
        return y_tritone

    def apply_reverb(self, room_size, reverb_absortion ):
        room_dim = room_size
        room = pra.ShoeBox(room_dim, fs=self.sample_rate, max_order=15, absorption=reverb_absortion)
        room.add_source([2, 3, 2], signal=self.original_audio_buffer)
        room.add_microphone_array(pra.MicrophoneArray(np.array([[7, 8, 1.5]]).T, room.fs))
        room.compute_rir()
        y_reverb = np.convolve(room.rir[0][0], self.original_audio_buffer)
        # If necessary, normalize the output
        y_reverb /= np.max(np.abs(y_reverb))
        return y_reverb

    def apply_harmonic(self, harmonic_factor):
        harmonic_buffer = librosa.effects.harmonic(self.original_audio_buffer, harmonic_factor)
        return harmonic_buffer

    def apply_percusive(self, percusive_factor):
        percussive_buffer = librosa.effects.percussive(self.original_audio_buffer, margin=percusive_factor)
        return percussive_buffer

    def render_to_file(self, audio_buffer, output_file):
        print(self.sample_rate)
        sf.write(output_file, audio_buffer, self.sample_rate)

    def get_audio_buffer(self):
        return self.original_audio_buffer

    def create_audio_from_sampled_chunk(self,number_slices, slice_duration, start_sampling_from):
        y = self.original_audio_buffer
        sr = self.sample_rate

        n_samples = int(sr * slice_duration)
        audio_samples = []
        for i in range(number_slices):
            r = int(random.random() * 10)
            print(r)
            temp_buffer = y[sr * i * (start_sampling_from * r):sr * i * (start_sampling_from * r) + n_samples]
            audio_samples.append(temp_buffer)
        combined_bufffers = np.concatenate(audio_samples)
        return combined_bufffers
