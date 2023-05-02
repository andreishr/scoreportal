from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from extractor import song_dict
'''
Create namespace and Graph for the ontology
'''
omo = Namespace("http://onemusiconto.com/omo#")
g = Graph()

# Define MusicInterval class :
g.add((omo.MusicInterval, RDF.type, OWL.Class))
g.add((omo.MusicInterval, RDFS.label, Literal("Music Interval")))
g.add((omo.MusicInterval, RDFS.comment, Literal("Has attributes: Direction, Number of semitones(as range), Type(consonant, disonant), Name")))
'''
Properties of music interval class:
'''
# Direction:
g.add((omo.Direction, RDF.type, OWL.DatatypeProperty))
g.add((omo.Direction, RDFS.label, Literal("Direction")))
g.add((omo.Direction, RDFS.comment, Literal("Ascneding or descending")))
g.add((omo.Direction, RDFS.range, RDFS.Literal))
g.add((omo.Direction, RDFS.domain, omo.MusicInterval))
# Name:
g.add((omo.IntervalName, RDF.type, OWL.DatatypeProperty))
g.add((omo.IntervalName, RDFS.label, Literal("Name")))
g.add((omo.IntervalName, RDFS.comment, Literal("Interval name")))
g.add((omo.IntervalName, RDFS.range, RDFS.Literal))
g.add((omo.IntervalName, RDFS.domain, omo.MusicInterval))
# Number of semitones:
g.add((omo.NumSemitones, RDF.type, OWL.DatatypeProperty))
g.add((omo.NumSemitones, RDFS.label, Literal("Number of Semitones")))
g.add((omo.NumSemitones, RDFS.comment, Literal("Range in number of semitones")))
g.add((omo.NumSemitones, RDFS.range, RDFS.Literal))
g.add((omo.NumSemitones, RDFS.domain, omo.MusicInterval))
# Type:
g.add((omo.IntervalType, RDF.type, OWL.DatatypeProperty))
g.add((omo.IntervalType, RDFS.label, Literal("Interval Type")))
g.add((omo.IntervalType, RDFS.comment, Literal("Consonant or dissonant")))
g.add((omo.IntervalType, RDFS.range, RDFS.Literal))
g.add((omo.IntervalType, RDFS.domain, omo.MusicInterval))
# PitchStart:
g.add((omo.IntervalStart, RDF.type, OWL.DatatypeProperty))
g.add((omo.IntervalStart, RDFS.label, Literal("Interval Start Pitch")))
g.add((omo.IntervalStart, RDFS.comment, Literal("The starting pitch of the interval")))
g.add((omo.IntervalStart, RDFS.range, RDFS.Literal))
g.add((omo.IntervalStart, RDFS.domain, omo.MusicInterval))
# PitchEnd:
g.add((omo.IntervalEnd, RDF.type, OWL.DatatypeProperty))
g.add((omo.IntervalEnd, RDFS.label, Literal("Interval End Pitch")))
g.add((omo.IntervalEnd, RDFS.comment, Literal("The ending pitch of the interval")))
g.add((omo.IntervalEnd, RDFS.range, RDFS.Literal))
g.add((omo.IntervalEnd, RDFS.domain, omo.MusicInterval))

# Define Song Class:
g.add((omo.Song, RDF.type, OWL.Class))
g.add((omo.Song, RDFS.label, Literal("Song")))
g.add((omo.Song, RDFS.comment, Literal("Has properties: Composer, Title. A song can contain Parts")))
'''
Song properties:
'''
# Composer:
g.add((omo.SongComposer, RDF.type, OWL.DatatypeProperty))
g.add((omo.SongComposer, RDFS.label, Literal("Composer name")))
g.add((omo.SongComposer, RDFS.range, RDFS.Literal))
g.add((omo.SongComposer, RDFS.domain, omo.Song))
# Title:
g.add((omo.SongTitle, RDF.type, OWL.DatatypeProperty))
g.add((omo.SongTitle, RDFS.label, Literal("Song title")))
g.add((omo.SongTitle, RDFS.range, RDFS.Literal))
g.add((omo.SongTitle, RDFS.domain, omo.Song))

# Define Part class:
g.add((omo.Part, RDF.type, OWL.Class))
g.add((omo.Part, RDFS.label, Literal("Song Part")))
g.add((omo.Part, RDFS.comment, Literal("Has properties: PartName, PartClef, PartScale, PartLength (quarter-length units),"
                                      "PartSignature, PartInstrument." 
                                      "A part can contain notes")))
'''
Part properties
'''
# Name:
g.add((omo.PartName, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartName, RDFS.label, Literal("Part Name")))
g.add((omo.PartName, RDFS.range, RDFS.Literal))
g.add((omo.PartName, RDFS.domain, omo.Part))
# Clef:
g.add((omo.PartClef, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartClef, RDFS.label, Literal("Part Clef")))
g.add((omo.PartClef, RDFS.range, RDFS.Literal))
g.add((omo.PartClef, RDFS.domain, omo.Part))
# Scale:
g.add((omo.PartScale, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartScale, RDFS.label, Literal("Part Scale")))
g.add((omo.PartScale, RDFS.range, RDFS.Literal))
g.add((omo.PartScale, RDFS.domain, omo.Part))
# Length:
g.add((omo.PartLength, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartLength, RDFS.label, Literal("Part length")))
g.add((omo.PartLength, RDFS.comment, Literal("Part length measured in quarter-length units")))
g.add((omo.PartLength, RDFS.range, RDFS.Literal))
g.add((omo.PartLength, RDFS.domain, omo.Part))
# Signature:
g.add((omo.PartSignature, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartSignature, RDFS.label, Literal("Part Time Signature")))
g.add((omo.PartSignature, RDFS.comment, Literal("Part Time signature (ex. 2/1)")))
g.add((omo.PartSignature, RDFS.range, RDFS.Literal))
g.add((omo.PartSignature, RDFS.domain, omo.Part))
# Instrument:
g.add((omo.PartInstrument, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartInstrument, RDFS.label, Literal("Part Instrument")))
g.add((omo.PartInstrument, RDFS.comment, Literal("Voice can be also considered instrument")))
g.add((omo.PartInstrument, RDFS.range, RDFS.Literal))
g.add((omo.PartInstrument, RDFS.domain, omo.Part))

# # Add chord class:
# g.add((omo.Chord, RDF.type, OWL.Class))
# g.add((omo.Chord, RDFS.label, Literal("Chord Class")))
# g.add((omo.Chord, RDFS.comment, Literal("Has properties: ChordName.")))
# '''
# Chord properties
# '''
# # Name:
# g.add((omo.ChordName, RDF.type, OWL.DatatypeProperty))
# g.add((omo.ChordName, RDFS.label, Literal("Chord Name")))
# g.add((omo.ChordName, RDFS.range, RDFS.Literal))
# g.add((omo.ChordName, RDFS.domain, omo.Chord))

# Add note class:
g.add((omo.Note, RDF.type, OWL.Class))
g.add((omo.Note, RDFS.label, Literal("Note Class")))
g.add((omo.Note, RDFS.comment, Literal("Has properties: NoteName, NoteDuration. A Note can have a Pitch")))
'''
Note properties
'''
# Name:
g.add((omo.NoteName, RDF.type, OWL.DatatypeProperty))
g.add((omo.NoteName, RDFS.label, Literal("Note Name")))
g.add((omo.NoteName, RDFS.range, RDFS.Literal))
g.add((omo.NoteName, RDFS.domain, omo.Note))
# Duration:
g.add((omo.NoteDuration, RDF.type, OWL.DatatypeProperty))
g.add((omo.NoteDuration, RDFS.label, Literal("Note Duration")))
g.add((omo.NoteDuration, RDFS.range, RDFS.Literal))
g.add((omo.NoteDuration, RDFS.domain, omo.Note))

# Add Pitch class:
g.add((omo.Pitch, RDF.type, OWL.Class))
g.add((omo.Pitch, RDFS.label, Literal("Pitch")))
g.add((omo.Pitch, RDFS.comment, Literal("Has properties:Name, Octave, Accidental.")))
'''
Pitch properties
'''
# NameL
g.add((omo.PitchName, RDF.type, OWL.DatatypeProperty))
g.add((omo.PitchName, RDFS.label, Literal("Pitch Name")))
g.add((omo.PitchName, RDFS.range, RDFS.Literal))
g.add((omo.PitchName, RDFS.domain, omo.Pitch))
# Octave:
g.add((omo.PitchOctave, RDF.type, OWL.DatatypeProperty))
g.add((omo.PitchOctave, RDFS.label, Literal("Pitch Octave")))
g.add((omo.PitchOctave, RDFS.range, RDFS.Literal))
g.add((omo.PitchOctave, RDFS.domain, omo.Pitch))
# Accidental:
g.add((omo.PitchAccidental, RDF.type, OWL.DatatypeProperty))
g.add((omo.PitchAccidental, RDFS.label, Literal("Pitch Accidental")))
g.add((omo.PitchAccidental, RDFS.comment, Literal("Modifiers such as '#' or '-' or 'None'")))
g.add((omo.PitchAccidental, RDFS.range, RDFS.Literal))
g.add((omo.PitchAccidental, RDFS.domain, omo.Pitch))

# Add MusicGenre class:
g.add((omo.MusicGenre, RDF.type, OWL.Class))
g.add((omo.MusicGenre, RDFS.label, Literal("Genre")))
g.add((omo.MusicGenre, RDFS.comment, Literal("Has properties: GenreType. Has subclasses: MusicStyles")))
'''
Genre properties
'''
g.add((omo.GenreType, RDF.type, OWL.DatatypeProperty))
g.add((omo.GenreType, RDFS.label, Literal("Specific Genre")))
g.add((omo.GenreType, RDFS.range, RDFS.Literal))
g.add((omo.GenreType, RDFS.domain, omo.MusicGenre))

# Add Style class:
g.add((omo.MusicStyle, RDF.type, OWL.Class))
g.add((omo.MusicStyle, RDFS.label, Literal("Style")))
g.add((omo.MusicStyle, RDFS.comment, Literal("Has properties: SongStyle. Has parent class: MusicGenre")))
g.add((omo.MusicStyle, RDFS.subClassOf, omo.MusicGenre))
'''
Style properties
'''
g.add((omo.SongStyle, RDF.type, OWL.DatatypeProperty))
g.add((omo.SongStyle, RDFS.label, Literal("Specific Genre")))
g.add((omo.SongStyle, RDFS.range, RDFS.Literal))
g.add((omo.SongStyle, RDFS.domain, omo.MusicStyle))


'''
Define object properties
'''
# Define the hasPitch object property
g.add((omo.hasPitch, RDF.type, OWL.ObjectProperty))
g.add((omo.hasPitch, RDFS.label, Literal("hasPitch")))
g.add((omo.hasPitch, RDFS.comment, Literal("Relates a note to a pitch")))
g.add((omo.hasPitch, RDFS.domain, omo.Note))
g.add((omo.hasPitch, RDFS.range, omo.Pitch))
# Define the hasPart object property
g.add((omo.hasPart, RDF.type, OWL.ObjectProperty))
g.add((omo.hasPart, RDFS.label, Literal("hasPart")))
g.add((omo.hasPart, RDFS.comment, Literal("Relates a song to a part")))
g.add((omo.hasPart, RDFS.domain, omo.Song))
g.add((omo.hasPart, RDFS.range, omo.Part))
# Define the hasNote object property
g.add((omo.hasNote, RDF.type, OWL.ObjectProperty))
g.add((omo.hasNote, RDFS.label, Literal("hasNote")))
g.add((omo.hasNote, RDFS.comment, Literal("Relates parts with notes")))
g.add((omo.hasNote, RDFS.domain, omo.Part))
g.add((omo.hasNote, RDFS.range, omo.Note))
# Define the pitchOfPart object property
g.add((omo.pitchOfPart, RDF.type, OWL.ObjectProperty))
g.add((omo.pitchOfPart, RDFS.label, Literal("pitchOfPart")))
g.add((omo.pitchOfPart, RDFS.comment, Literal("Relates pitches to parts")))
g.add((omo.pitchOfPart, RDFS.domain, omo.Pitch))
g.add((omo.pitchOfPart, RDFS.range, omo.Part))
# Define the hasInterval object property
g.add((omo.hasInterval, RDF.type, OWL.ObjectProperty))
g.add((omo.hasInterval, RDFS.label, Literal("hasInterval")))
g.add((omo.hasInterval, RDFS.comment, Literal("Relates parts to intervals")))
g.add((omo.hasInterval, RDFS.domain, omo.Part))
g.add((omo.hasInterval, RDFS.range, omo.MusicInterval))





'''
Add instances
'''
# Song instance
for song in song_dict:
    currentSong = song_dict[song]['songDescription']
    song_uri = omo + song
    g.add((URIRef(song_uri), RDF.type, omo.Song))
    g.add((URIRef(song_uri), omo.SongComposer, Literal(f"Composer: {currentSong[1]}"))) 
    g.add((URIRef(song_uri), omo.SongTitle, Literal(f"Title: {currentSong[0]}")))
    parts = song_dict[song]['Parts']
    for part in parts:
        part_uri = song_uri + "/Part/" + part.replace(" ", "_")
        scale = parts[part][0]
        length = parts[part][1]
        clef = parts[part][2]
        signature = parts[part][3]
        instrument = parts[part][4]
        g.add((URIRef(part_uri), RDF.type, omo.Part))
        g.add((URIRef(part_uri), omo.PartName, Literal(f"{part}")))
        g.add((URIRef(part_uri), omo.ParClef, Literal(f"{clef}")))
        g.add((URIRef(part_uri), omo.PartScale, Literal(f"{scale}")))
        g.add((URIRef(part_uri), omo.PartLength, Literal(f"{length}")))
        g.add((URIRef(part_uri), omo.PartSignature, Literal(f"{signature}")))
        g.add((URIRef(part_uri), omo.PartInstrument, Literal(f"{instrument}")))
        g.add((URIRef(song_uri), omo.hasPart, URIRef(part_uri)))

        noteList = parts[part][5]
        for note in noteList:
            note_uri = omo + "Note/" + note.name[0] + "/Dur/" + str(note.duration).split(".")[2].replace(" ", "_").replace(".", "").replace(">", "")
            g.add((URIRef(note_uri), RDF.type, omo.Note))
            g.add((URIRef(note_uri), omo.NoteName, Literal(f"{note.name[0]}")))
            g.add((URIRef(note_uri), omo.NoteDuration, Literal(f"{note.duration}")))
            g.add((URIRef(part_uri), omo.hasNote, URIRef(note_uri)))
            pitch_uri = note_uri + "/Pitch" + str(note.pitch).replace("#", "Sharp").replace("-", "Flat")
            g.add((URIRef(pitch_uri), RDF.type, omo.Pitch))
            g.add((URIRef(pitch_uri), omo.PitchName, Literal(f"{note.pitch}")))
            g.add((URIRef(pitch_uri), omo.PitchOctave, Literal(f"{note.pitch.octave}")))
            g.add((URIRef(pitch_uri), omo.PitchAccidental, Literal(f"{note.pitch.accidental}")))
            g.add((URIRef(note_uri), omo.hasPitch, URIRef(pitch_uri)))
            g.add((URIRef(pitch_uri), omo.pitchOfPart, URIRef(part_uri))) 

        intervalList = parts[part][6]
        for interval in intervalList:
            interval_uri = omo + str(interval[0].directedNiceName).replace(" ", "_") + "/" + interval[1] + str(interval[0].pitchStart).replace("#", "Sharp").replace("-", "Flat") + str(interval[0].pitchEnd).replace("#", "Sharp").replace("-", "Flat") 
            g.add((URIRef(interval_uri), RDF.type, omo.MusicInterval))
            g.add((URIRef(interval_uri), omo.IntervalName, Literal(f"{interval[0].directedNiceName}")))
            g.add((URIRef(interval_uri), omo.NumSemitones, Literal(interval[0].semitones)))
            g.add((URIRef(interval_uri), omo.IntervalType, Literal(f"{interval[1]}")))
            g.add((URIRef(interval_uri), omo.IntervalStart, Literal(f"{interval[0].pitchStart}")))
            g.add((URIRef(interval_uri), omo.IntervalEnd, Literal(f"{interval[0].pitchEnd}")))
            g.add((URIRef(part_uri), omo.hasInterval, URIRef(interval_uri)))


# Genre
g.add((omo.ClassicGenre, RDF.type, omo.MusicGenre))
g.add((omo.ClassicGenre, omo.GenreType, Literal("Classic")))

# serialize the ontology in turtle format and save to file
with open("ontology.ttl", "wb") as f:
    f.write(g.serialize(format="turtle").encode('utf-8'))