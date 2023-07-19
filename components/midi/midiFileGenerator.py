import mido
from mido import Message, MidiFile, MidiTrack
class midi_file_generator:
    def __init__(self, file_path):  # constructor
        self.__file_path = file_path

    def generate_simple_chord(self):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        # C Major chord
        track.append(Message('note_on', note=60, velocity=64, time=0))  # C
        track.append(Message('note_on', note=64, velocity=64, time=0))  # E
        track.append(Message('note_on', note=67, velocity=64, time=0))  # G
        track.append(Message('note_off', note=60, velocity=64, time=480))  # note_off after 480 ticks
        track.append(Message('note_off', note=64, velocity=64, time=0))
        track.append(Message('note_off', note=67, velocity=64, time=0))

        mid.save(self.__file_path)
