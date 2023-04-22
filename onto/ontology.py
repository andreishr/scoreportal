from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal

'''
Create namespace and Graph for the ontology
'''
omo = Namespace("http://onemusiconto.com/omo#")
g = Graph()
# Define MusicInterval class :
g.add((omo.MusicInterval, RDF.type, OWL.Class))
'''
Properties of music interval class:
'''
g.add((omo.MusicInterval, RDFS.label, Literal("Music Interval")))
g.add((omo.MusicInterval, RDFS.comment, Literal("Has attributes: Direction, Number of semitones(as range), Type(consonant, disonant), Name")))
# Direction:
g.add((omo.Direction, RDF.type, OWL.DatatypeProperty))
g.add((omo.Direction, RDFS.label, Literal("Direction")))
g.add((omo.Direction, RDFS.comment, Literal("Ascneding or descending")))
g.add((omo.Direction, RDFS.range, RDFS.Literal))
# Name:
g.add((omo.IntervalName, RDF.type, OWL.DatatypeProperty))
g.add((omo.IntervalName, RDFS.label, Literal("Name")))
g.add((omo.IntervalName, RDFS.comment, Literal("Interval name")))
g.add((omo.IntervalName, RDFS.range, RDFS.Literal))
# Number of semitones:
g.add((omo.NumSemitones, RDF.type, OWL.DatatypeProperty))
g.add((omo.NumSemitones, RDFS.label, Literal("Number of Semitones")))
g.add((omo.NumSemitones, RDFS.comment, Literal("Range in number of semitones")))
g.add((omo.NumSemitones, RDFS.range, RDFS.Literal))
# Type:
g.add((omo.IntervalType, RDF.type, OWL.DatatypeProperty))
g.add((omo.IntervalType, RDFS.label, Literal("Interval Type")))
g.add((omo.IntervalType, RDFS.comment, Literal("Consonant or dissonant")))
g.add((omo.IntervalType, RDFS.range, RDFS.Literal))

# Define Song Class:
g.add((omo.Song, RDF.type, OWL.Class))
'''
Song properties
'''
# Composer:
g.add((omo.SongComposer, RDF.type, OWL.DatatypeProperty))
g.add((omo.SongComposer, RDFS.label, Literal("Composer name")))
g.add((omo.SongComposer, RDFS.range, RDFS.Literal))
# Title:
g.add((omo.SongTitle, RDF.type, OWL.DatatypeProperty))
g.add((omo.SongTitle, RDFS.label, Literal("Song title")))
g.add((omo.SongTitle, RDFS.range, RDFS.Literal))

# Define Part class:
g.add((omo.Part, RDF.type, OWL.Class))
g.add((omo.Part, RDFS.label, Literal("Song Part")))
g.add((omo.Part, RDFS.comment, Literal("A part of the score")))
'''
Part properties
'''
# Clef
g.add((omo.PartClef, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartClef, RDFS.label, Literal("Part Clef")))
g.add((omo.PartTitle, RDFS.range, RDFS.Literal))
# Scale
g.add((omo.PartScale, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartScale, RDFS.label, Literal("Part Scale")))
g.add((omo.PartScale, RDFS.range, RDFS.Literal))
# Length
g.add((omo.PartLength, RDF.type, OWL.DatatypeProperty))
g.add((omo.PartLength, RDFS.label, Literal("Part length")))
g.add((omo.PartLength, RDFS.comment, Literal("Part length measured in quarter-length units")))
g.add((omo.PartLength, RDFS.range, RDFS.Literal))

# Add note class
g.add((omo.Note, RDF.type, OWL.Class))
'''
Note properties
'''
# Name
g.add((omo.NoteName, RDF.type, OWL.DatatypeProperty))
g.add((omo.NoteName, RDFS.label, Literal("Note Name")))
g.add((omo.NoteName, RDFS.range, RDFS.Literal))
# Duration
g.add((omo.NoteDuration, RDF.type, OWL.DatatypeProperty))
g.add((omo.NoteDuration, RDFS.label, Literal("Note Duration")))
g.add((omo.NoteDuration, RDFS.range, RDFS.Literal))
#TODO pitch 

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
g.add((omo.MyNote, omo.NoteDuration, Literal("4")))

# serialize the ontology in turtle format and save to file
with open("ontology.ttl", "wb") as f:
    f.write(g.serialize(format="turtle").encode('utf-8'))