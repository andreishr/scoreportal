from rdflib import Graph
from termcolor import  cprint
import os
from dotenv import load_dotenv
import ast

from classes.chord import Chord

load_dotenv()
# Getting URI constants
chord_uri_constant = os.getenv('CHORD_URI_CONSTANT')
measure_uri_constant = os.getenv('MEASURE_URI_CONSTANT')
containsPitch_uri = os.getenv('CONTAINS_PITCH_URI')
chord_pitchesList_uri = os.getenv('CONTAINS_PITCHES_LIST_URI')
contains_note_uri = os.getenv('CONTAINS_NOTES_LIST_URI')
has_chord_uri = os.getenv('HAS_CHORD_URI')
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

    if measure_uri_constant in o:
        measure_set.add(s)

    if chord_uri_constant in o:
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


for elem in chord_attributes:
    print(elem)
# Processig objets and appending to lists
for elem in measure_attributes:
    for measure_attribute in measure_attributes[elem]:
        if has_chord_uri in measure_attribute[0]:
            chord_name = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordName" in item[0]]
            chord_duration = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordDuration" in item[0]]
            chord_pitches = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#containsPitch" in item[0]]
            chord_pitch_list = [ast.literal_eval(item[1].toPython()) for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordPitches" in item[0]][0]
            chord_notes = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#containsNote" in item[0]]
            chord_note_list = [ast.literal_eval(item[1].toPython()) for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordNotes" in item[0]][0]
            chord_object_list.append(Chord(chord_name, chord_duration, chord_pitch_list, chord_note_list, chord_notes, chord_pitches))
            cprint(chord_name, "red")
            cprint(chord_duration, "red")
            cprint(chord_pitches, "red")
            cprint(chord_pitch_list, "red")
            cprint(chord_notes, "red")
            cprint(chord_object_list[0].name, "green")
            # cprint(attribute[1], "red")
            # cprint(attribute[1].toPython(), "yellow")
            cprint(chord_attributes[measure_attribute[1]], "yellow")
    print(elem)
    cprint(measure_attributes[elem], "cyan")

for chord_obj in chord_object_list:
    cprint(chord_obj.name, "green")
    cprint(chord_obj.pitchList, "green")

    #For measure in measures
    #Check if first element is has chord
    #Get it from chord attributes
    #Map it to object and add to chord list
    #Map the rest of the measure to the measure list

    