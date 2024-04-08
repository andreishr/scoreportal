from rdflib import Graph
from termcolor import  cprint
import os
from dotenv import load_dotenv
import ast

from classes.chord import Chord
from classes.measure import Measure

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


for elem in measure_attributes:
    chord_tmp_list = []
    for measure_attribute in measure_attributes[elem]:
        if has_chord_uri in measure_attribute[0]:
            chord_name = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordName" in item[0]]
            chord_duration = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordDuration" in item[0]]
            chord_pitches = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#containsPitch" in item[0]]
            chord_pitch_list = [ast.literal_eval(item[1].toPython()) for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordPitches" in item[0]][0]
            chord_notes = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#containsNote" in item[0]]
            chord_note_list = [ast.literal_eval(item[1].toPython()) for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordNotes" in item[0]][0]
            chord_tmp_list.append(Chord(chord_name, chord_duration, chord_pitch_list, chord_note_list, chord_notes, chord_pitches))

            #Optional mapping to chord list
            chord_object_list.append(Chord(chord_name, chord_duration, chord_pitch_list, chord_note_list, chord_notes, chord_pitches))
           

    measure_duration = [item[1].toPython() for item in measure_attributes[elem] if "http://onemusiconto.com/omo#MeasureDuration" in item[0]]
    measure_number = [item[1].toPython() for item in measure_attributes[elem] if "http://onemusiconto.com/omo#MeasureNumber" in item[0]]
    measure_name = elem
    measure_object_list.append(Measure(measure_name, measure_duration, measure_number, chord_tmp_list))


def get_element_similarity(elements, verbose = 0):
    individuals_tuple_list = []
    checks = set()
    for first_element in elements:
        for second_element in elements:
            if first_element != second_element and (first_element, second_element) not in checks and (second_element, first_element) not in checks:
                similarity = 1 # to be replaced with method that computes similarity between meaasures
                individuals_tuple_list.append((first_element, second_element, similarity))
            checks.add((first_element, second_element))

    individuals_tuple_list.sort(key=lambda x: x[2], reverse=True)
    
    if verbose != 0:
        for similarity_tuple in individuals_tuple_list[:150]:
            cprint(similarity_tuple[0].name, 'cyan', attrs=["bold"])
            cprint(similarity_tuple[1].name, 'cyan', attrs=["bold"])
            cprint(similarity_tuple[2], 'green', attrs=["bold"])

    return individuals_tuple_list
    

get_element_similarity(measure_object_list, 1)