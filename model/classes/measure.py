from .chord import Chord

class Measure:
    chords = []
    def __init__(self, name, duration, number, chords = []):
        self.name = name
        self.duration = duration
        self.number = number
        self.chords = chords

    def add_chord(self, chord: Chord):
        self.chords.append(chord)