from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL
# Define namespace
omo = Namespace("http://onemusiconto.com/omo#")
g = Graph()
g.bind('omo', omo)


'''
Song class and subclasses
'''
Song = URIRef(omo + 'Song')
Title = URIRef(omo + 'SongTitle')
Composer = URIRef(omo + 'SongComposer')
Format = URIRef(omo + 'SongFormat')
Parts = URIRef(omo + 'SongPart')
Measures = URIRef(omo + 'Measure')
g.add((Song, RDF.type, OWL.Class))
g.add((Title, RDFS.subClassOf, Song))
g.add((Composer, RDFS.subClassOf, Song))
g.add((Format, RDFS.subClassOf, Song))
g.add((Parts, RDFS.subClassOf, Song))
g.add((Measures, RDFS.subClassOf, Song))


'''
Part subclasses
'''
Notes = URIRef(omo + 'Notes')
Clef = URIRef(omo + 'Clef')
TimeSignature = URIRef(omo + 'TimeSignature')
Instrument = URIRef(omo + 'Instrument')
Intervals = URIRef(omo + 'Interval')
g.add((Notes, RDFS.subClassOf, Parts))
g.add((Clef, RDFS.subClassOf, Parts))
g.add((TimeSignature, RDFS.subClassOf, Parts))
g.add((Instrument, RDFS.subClassOf, Parts))
g.add((Intervals, RDFS.subClassOf, Parts))


'''
Note subclasses
'''
Offset = URIRef(omo + 'NoteOffset')
Pitch = URIRef(omo + 'NotePitch')
g.add((Offset, RDFS.subClassOf, Notes))
g.add((Pitch, RDFS.subClassOf, Notes))


'''
Measure subclasses
'''
Number = URIRef(omo + 'MeasureNumber')
Chords = URIRef(omo + 'MeasureChords')
g.add((Number, RDFS.subClassOf, Measures))
g.add((Chords, RDFS.subClassOf, Measures))


'''
Chord subclasses
'''
ChordName = URIRef(omo + 'ChordName')
ChordPitches = URIRef(omo +'ChordPitches')
g.add((ChordName, RDFS.subClassOf, Chords))
g.add((ChordPitches, RDFS.subClassOf, Chords))


'''
Song properties
'''
has_title = URIRef(omo + 'hasTitle')
has_composer = URIRef(omo + 'hasComposer')
has_format = URIRef(omo + 'hasFormat')
has_part = URIRef(omo + 'hasParts')
has_measure = URIRef(omo + 'hasMeasure')
# Title property
g.add((has_title, RDF.type, OWL.DatatypeProperty))
g.add((has_title, RDFS.domain, Song))
g.add((has_title, RDFS.range, RDFS.Literal))
# Composer property
g.add((has_composer, RDF.type, OWL.DatatypeProperty))
g.add((has_composer, RDFS.domain, Song))
g.add((has_composer, RDFS.range, RDFS.Literal))
# Format property
g.add((has_format, RDF.type, OWL.DatatypeProperty))
g.add((has_format, RDFS.domain, Song))
g.add((has_format, RDFS.range, RDFS.Literal))
# Part property
g.add((has_part, RDF.type, OWL.ObjectProperty))
g.add((has_part, RDFS.domain, Song))
g.add((has_part, RDFS.range, Parts))
# Measure property
g.add((has_measure, RDF.type, OWL.ObjectProperty))
g.add((has_measure, RDFS.domain, Song))
g.add((has_measure, RDFS.range, Measures))


'''
Part properties
'''
has_notes = URIRef(omo + 'hasNote')
has_clef = URIRef(omo + 'hasClef')
has_signature = URIRef(omo + 'hasSignature')
has_instrument = URIRef(omo + 'hasInstrument')
has_interval = URIRef(omo + 'hasInterval')
# Note property
g.add((has_notes, RDF.type, OWL.ObjectProperty))
g.add((has_notes, RDFS.domain, Parts))
g.add((has_notes, RDFS.range, Notes))
# Clef property
g.add((has_clef, RDF.type, OWL.DatatypeProperty))
g.add((has_clef, RDFS.domain, Parts))
g.add((has_clef, RDFS.range, RDFS.Literal))
# Time Signature property
g.add((has_signature, RDF.type, OWL.DatatypeProperty))
g.add((has_signature, RDFS.domain, Parts))
g.add((has_signature, RDFS.range, RDFS.Literal))
# Instrument property
g.add((has_instrument, RDF.type, OWL.DatatypeProperty))
g.add((has_instrument, RDFS.domain, Parts))
g.add((has_instrument, RDFS.range, RDFS.Literal))
# Intervals property
g.add((has_interval, RDF.type, OWL.ObjectProperty))
g.add((has_interval, RDFS.domain, Parts))
g.add((has_interval, RDFS.range, Intervals))


'''
Notes properties
'''
has_offset = URIRef(omo + 'hasOffset')
has_pitch = URIRef(omo + 'hasPitch')
# Offset property
g.add((has_offset, RDF.type, OWL.DatatypeProperty))
g.add((has_offset, RDFS.domain, Notes))
g.add((has_offset, RDFS.range, RDFS.Literal))
# Pitch property
g.add((has_pitch, RDF.type, OWL.DatatypeProperty))
g.add((has_pitch, RDFS.domain, Notes))
g.add((has_pitch, RDFS.range, RDFS.Literal))


'''
Measure Properties
'''
has_number = URIRef(omo + 'hasNumber')
has_chord = URIRef(omo + 'hasChord')
# Number property
g.add((has_number, RDF.type, OWL.DatatypeProperty))
g.add((has_number, RDFS.domain, Measures))
g.add((has_number, RDFS.range, RDFS.Literal))
# Chords property
g.add((has_chord, RDF.type, OWL.ObjectProperty))
g.add((has_chord, RDFS.domain, Measures))
g.add((has_chord, RDFS.range, Chords))


'''
Chord properties
'''
has_chordName = URIRef(omo + 'hasChordName')
has_chordPitches = URIRef(omo +'hasChordPitches')
# Chord Name property
g.add((has_number, RDF.type, OWL.DatatypeProperty))
g.add((has_number, RDFS.domain, Chords))
g.add((has_number, RDFS.range, RDFS.Literal))
# Chord Pitches property
g.add((has_chordPitches, RDF.type, OWL.ObjectProperty))
g.add((has_chordPitches, RDFS.domain, Chords))
g.add((has_chordPitches, RDFS.range, Pitch))


# Define URI for the song
my_song = URIRef(omo + 'MySong')

# Add RDF type for the song
g.add((my_song, RDF.type, Song))

# Add properties for the song
g.add((my_song, has_title, Literal('My Song Title')))
g.add((my_song, has_composer, Literal('My Song Composer')))
g.add((my_song, has_format, Literal('MP3')))

# Add part for the song
# Define the new part resource
part = URIRef(omo + 'MySongPart')
note = URIRef(omo + "MyNote")
interval = URIRef(omo + "MyInterval")
g.add((part, RDF.type, Parts))
g.add((my_song, has_part, part))
g.add((note, RDF.type, Notes))
g.add((part, has_notes, note))
g.add((interval, RDF.type, Intervals))
g.add((part, has_interval, interval))
# Add properties to the part
g.add((part, has_notes, note))
g.add((part, has_clef, Literal('treble')))
g.add((part, has_signature, Literal('4/4')))
g.add((part, has_instrument, Literal('piano')))
g.add((part, has_interval, interval))
# Add the new part to the song
g.add((my_song, has_part, part))


with open("ontology.ttl", "wb") as f:
    f.write(g.serialize(format="turtle").encode('utf-8'))

