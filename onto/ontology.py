from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal

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
g.add((omo.Part, RDFS.comment, Literal("Has properties: Clef, Scale, Length (quarter-length units)." 
                                      "A part can contain notes")))
'''
Part properties
'''
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

# Add note class:
g.add((omo.Note, RDF.type, OWL.Class))
g.add((omo.Note, RDFS.label, Literal("Note Class")))
g.add((omo.Note, RDFS.comment, Literal("Has properties: Name, Duration. A Note can have a Pitch")))
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
g.add((omo.Pitch, RDFS.comment, Literal("Has properties: Octave, Accidental.")))
'''
Pitch properties
'''
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



'''
Define object properties
'''
# Define the hasPitch object property
g.add((omo.hasPitch, RDF.type, OWL.ObjectProperty))
g.add((omo.hasPitch, RDFS.label, Literal("hasPitch")))
g.add((omo.hasPitch, RDFS.comment, Literal("Relates a note to a pitch")))



'''
Test instances
'''
# Interval instance
g.add((omo.major_third, RDF.type, omo.MusicInterval))
g.add((omo.major_third, omo.IntervalName, Literal("Major Third")))
g.add((omo.major_third, omo.NumSemitones, Literal(4)))
g.add((omo.major_third, omo.IntervalType, Literal("Consonant")))
# Song instance
g.add((omo.MySong, RDF.type, omo.Song))
g.add((omo.MySong, omo.SongComposer, Literal("MySong Composer")))
g.add((omo.MySong, omo.SongTitle, Literal("MySong")))
# Part
g.add((omo.MyPart, RDF.type, omo.Part))
g.add((omo.MyPart, omo.PartClef, Literal("TrebleClef")))
g.add((omo.MyPart, omo.PartScale, Literal("C Major")))
g.add((omo.MyPart, omo.PartLength, Literal("1820 quarter-length units")))
# Note
g.add((omo.MyNote, RDF.type, omo.Note))
g.add((omo.MyNote, omo.NoteName, Literal("E")))
g.add((omo.MyNote, omo.NoteDuration, Literal("2")))
# Pitch
g.add((omo.MyPitch, RDF.type, omo.Pitch))
g.add((omo.MyPitch, omo.PitchOctave, Literal("4")))
g.add((omo.MyPitch, omo.PitchAccidental, Literal("None")))
# Genre
g.add((omo.ClassicGenre, RDF.type, omo.MusicGenre))
g.add((omo.ClassicGenre, omo.GenreType, Literal("Classic")))

# Link the MySong instance and major_third instance
g.add((omo.MyNote, omo.hasPitch, omo.MyPitch))

# serialize the ontology in turtle format and save to file
with open("ontology.ttl", "wb") as f:
    f.write(g.serialize(format="turtle").encode('utf-8'))