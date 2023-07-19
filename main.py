import librosa
import soundfile as sf
import mido
from mido import Message, MidiFile, MidiTrack
from components import midi
from components.audio.audio_interface import audio_interface
from components.audio.effects.reverb.reverb_effect import reverb_effect
if __name__ == '__main__':

    audio_interface = audio_interface("assets/beyonce.mp3", 0)
    audioBuffer = audio_interface.get_audio_buffer()
    audio_interface.load_buffer_from_audio()
    audioBuffer = audio_interface.get_audio_buffer()

    audioBufferPerc = audio_interface.apply_percusive(4.0)
    time_stretch_buffer = audio_interface.apply_stretch(0.02)
    audio_interface.reasign_audio_interface_buffer(time_stretch_buffer)
    audio_split_chunk = audio_interface.create_audio_from_sampled_chunk(120, 1.0, 5)
    audio_interface.render_to_file(audio_split_chunk, "chunk_gltich.wav")

