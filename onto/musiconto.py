from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL

omo = Namespace("http://onemusiconto.com/omo#")
g = Graph()
g.bind('omo', omo)
# Song class and subclasses
Song = URIRef(omo + 'Song')
Title = URIRef(omo + 'SongTitle')
Composer = URIRef(omo + 'SongComposer')
Format = URIRef(omo + 'SongFormat')
Part = URIRef(omo + 'SongPart')
g.add((Song, RDF.type, OWL.Class))
g.add((Title, RDFS.subClassOf, Song))
g.add((Composer, RDFS.subClassOf, Song))
g.add((Format, RDFS.subClassOf, Song))
g.add((Part, RDFS.subClassOf, Song))
# Part subclasses
Notes = URIRef(omo + 'Notes')
Clef = URIRef(omo + 'Clef')
TimeSignature = URIRef(omo + 'TimeSignature')
g.add((Notes, RDFS.subClassOf, Part))
g.add((Clef, RDFS.subClassOf, Part))
g.add((TimeSignature, RDFS.subClassOf, Part))



has_title = URIRef(omo + "hasTitle")
has_composer = URIRef(omo + "hasComposer")
has_format = URIRef(omo + "hasFormat")
has_part = URIRef(omo + "hasPart")
g.add((has_title, RDF.type, OWL.DatatypeProperty))
g.add((has_title, RDFS.domain, Song))
g.add((has_title, RDFS.range, RDFS.Literal))
g.add((has_composer, RDF.type, OWL.DatatypeProperty))
g.add((has_composer, RDFS.domain, Song))
g.add((has_composer, RDFS.range, RDFS.Literal))
g.add((has_format, RDF.type, OWL.DatatypeProperty))
g.add((has_format, RDFS.domain, Song))
g.add((has_format, RDFS.range, RDFS.Literal))
g.add((has_part, RDF.type, OWL.ObjectProperty))
g.add((has_part, RDFS.domain, Song))
g.add((has_part, RDFS.range, Part))

has_notes = URIRef(omo + "hasNotes")
has_clef = URIRef(omo + "hasClef")
has_signature = URIRef(omo + "hasSignature")
g.add((has_notes, RDF.type, OWL.ObjectProperty))
g.add((has_notes, RDFS.domain, Part))
g.add((has_notes, RDFS.range, Notes))
g.add((has_clef, RDF.type, OWL.DatatypeProperty))
g.add((has_clef, RDFS.domain, Part))
g.add((has_clef, RDFS.range, RDFS.Literal))
g.add((has_signature, RDF.type, OWL.DatatypeProperty))
g.add((has_signature, RDFS.domain, Part))
g.add((has_signature, RDFS.range, RDFS.Literal))

song1 = URIRef(omo + 'song1')
g.add((song1, RDF.type, Song))
g.add((song1, has_title, Literal('Bohemian Rhapsody')))
g.add((song1, has_composer, Literal('Freddie Mercury')))
g.add((song1, has_format, Literal('MP3')))

with open("ontology.ttl", "wb") as f:
    f.write(g.serialize(format="turtle").encode('utf-8'))

