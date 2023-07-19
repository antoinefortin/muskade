import librosa
import soundfile as sf
import numpy as np
import pyroomacoustics as pra

class audio_dummy_interface:
    def __init__(self, in_audio_file, out_audio_file):
        print("audio dummy interface")
        self.in_audio_file = in_audio_file
        self.out_audio_file = out_audio_file

    def librosa_test(self):
        y, sr = librosa.load(self.in_audio_file, sr=None)
        one_second_audio = y[sr * 2.8:sr * 3]
        sf.write(self.out_audio_file, one_second_audio, sr)


    def extract_audio_ms(self, from_timestamp, ms):
        y, sr = librosa.load(self.in_audio_file, sr=None)
        n_samples = int(sr * ms)
        first_segment = y[sr * 1:sr * 1 + n_samples]
        second_segment = y[sr * 2:sr * 2 + n_samples]
        combined = np.concatenate([first_segment, second_segment])
        sf.write(self.out_audio_file, combined, sr)

    def create_audio_from_sampled_chunk(self,number_slices, slice_duration, start_sampling_from):
        y, sr = librosa.load(self.in_audio_file, sr=None)
        n_samples = int(sr * slice_duration)

        audio_samples = []
        for i in range(number_slices):
            temp_buffer = y[sr * i * start_sampling_from:sr * i * start_sampling_from + n_samples]
            audio_samples.append(temp_buffer)
        combined_bufffers = np.concatenate(audio_samples)
        sf.write(self.out_audio_file, combined_bufffers, sr)


    def add_reverb_to_file(self):
        y, sr = librosa.load(self.in_audio_file)
        room_dim = [10, 15, 3]
        room = pra.ShoeBox(room_dim, fs=sr, max_order=15, absorption=0.35)

        room.add_source([2, 3, 2], signal=y)
        room.add_microphone_array(pra.MicrophoneArray(np.array([[7, 8, 1.5]]).T, room.fs))
        room.compute_rir()

        # convolve using npy
        y_reverb = np.convolve(room.rir[0][0], y)

        # If necessary, normalize the output
        y_reverb /= np.max(np.abs(y_reverb))
        sf.write(self.out_audio_file, y_reverb, sr)


    def add_reverb_to_buffer(self):
        b = 1