import librosa

class stretcher_effect:
    def __init__(self, in_audio_file, out_audio_file):
        self.in_audio_file = in_audio_file
        self.out_audio_file = out_audio_file

    def strecth_file(self, timefactor):
        y, sr = librosa.load(self.in_audio_file)
        y_time_stretched = librosa.effects.time_stretch(y, timefactor)
        
