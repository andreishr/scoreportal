class Chord:
    notes = []
    pitches = []
    frequencies = []
    def __init__(self, name, duration, pitchList, noteList, notes, pitches, offset, frequencies):
        self.name = name
        self.duration = duration
        self.pitchList = pitchList
        self.noteList = noteList
        self.notes = notes
        self.pitches = pitches
        self.offset = offset
        self.frequencies = frequencies
    
    def add_notes(self, note):
        self.notes.append(note)

    def add_pitches(self, pitch):
        self.pitches.append(pitch)

    def add_frequency(self, frequency):
        self.frequencies.append(frequency)