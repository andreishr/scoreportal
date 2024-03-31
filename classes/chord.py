class Chord:
    notes = []
    pitches = []
    def __init__(self, name, duration, pitchList, noteList):
        self.name = name
        self.duration = duration
        self.pitchList = pitchList
        self.noteList = noteList
    
    def add_notes(self, note):
        self.notes.append(note)

    def add_pitches(self, pitch):
        self.pitches.append(pitch)