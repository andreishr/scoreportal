from rdflib import Graph
from termcolor import  cprint
import os
from dotenv import load_dotenv

load_dotenv()
# Getting URI constants
chord_uri_constant = os.getenv('CHORD_URI_CONSTANT')
measure_uri_constant = os.getenv('MEASURE_URI_CONSTANT')
containsPitch_uri = os.getenv('CONTAINS_PITCH_URI')
chordPitchesList_uri = os.getenv('CONTAINS_PITCHES_LIST_URI')
containsNote_uri = os.getenv('CONTAINS_NOTES_LIST_URI')

#Parsing graph data
graph = Graph()
graph.parse("scoreportal/ontology.ttl", format="turtle")

#Initializing utils
chord_object_list = []
measure_object_list = []

measure_set = set()
measure_attributes = {}

chord_set = set()
chord_attributes = {}



# Getting all measues and chords
for s, p, o in graph:

    if measure_uri_constant in o and len(measure_set) < 10:
        measure_set.add(s)

    if chord_uri_constant in o and len(chord_set) < 10:
        chord_set.add(s)


#Get the attributes dictionaries for measures and chords
for s, p, o in graph:
    if s in measure_set and measure_uri_constant not in o:
        if s not in measure_attributes:
            measure_attributes[s] = []
            measure_attributes[s].append([p, o])
        else:
            measure_attributes[s].append([p, o])

for s, p, o in graph:
    if s in chord_set and chord_uri_constant not in o:
        if s not in chord_attributes:
            chord_attributes[s] = []
            chord_attributes[s].append([p, o])
        else:
            chord_attributes[s].append([p, o])



# Processig objets and appending to lists
for elem in measure_attributes:
    print(elem)
    cprint(measure_attributes[elem], "cyan")

    