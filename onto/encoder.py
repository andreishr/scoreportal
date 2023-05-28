import json
from music21.note import Note
from music21.interval import Interval
from music21.duration import Duration
class MusicElementEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Note):
            return {
                '__class__': 'Note',
                'name': obj.name,
                'duration': obj.duration.quarterLength,
                'pitch_octave': obj.pitch.octave,
                'pitch_accidental': str(obj.pitch.accidental)
                # Add any other relevant properties you want to serialize
            }
        if isinstance(obj, Interval):
            return {
                '__class__': 'Interval',
                'name': obj.directedNiceName,
                'semitones': obj.semitones,
                'pitchStart': obj.pitchStart.name + str(obj.pitchStart.octave),
                'pitchEnd': obj.pitchEnd.name + str(obj.pitchEnd.octave)
            }
        if isinstance(obj, Duration):
            return {
                '__class__': 'Duration',
                'duration' : obj.quarterLength
            }
        return super().default(obj)