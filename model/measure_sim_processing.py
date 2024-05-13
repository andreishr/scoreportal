from rdflib import Graph
from termcolor import  cprint
import os
from dotenv import load_dotenv
import ast
import math
import numpy as np
from scipy.integrate import quad

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
graph.parse("scoreportal/ontologyv2.ttl", format="turtle")

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
            chord_offset = [item[1].toPython() for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordOffset" in item[0]]
            chord_frequencies = [ast.literal_eval(item[1].toPython()) for item in chord_attributes[measure_attribute[1]] if "http://onemusiconto.com/omo#ChordFrequencies" in item[0]][0]

            chord_tmp_list.append(Chord(chord_name, chord_duration, chord_pitch_list, chord_note_list, chord_notes, chord_pitches, chord_offset, chord_frequencies))

            #Optional mapping to chord list
            chord_object_list.append(Chord(chord_name, chord_duration, chord_pitch_list, chord_note_list, chord_notes, chord_pitches, chord_offset, chord_frequencies))
           

    measure_duration = [item[1].toPython() for item in measure_attributes[elem] if "http://onemusiconto.com/omo#MeasureDuration" in item[0]]
    measure_number = [item[1].toPython() for item in measure_attributes[elem] if "http://onemusiconto.com/omo#MeasureNumber" in item[0]]
    measure_name = elem
    measure_object_list.append(Measure(measure_name, measure_duration, measure_number, chord_tmp_list))


def get_element_similarity(elements, verbose = 0):
    individuals_tuple_list = []
    individuals_tuple_list_integral = []
    checks = set()
    for first_element in elements:
        for second_element in elements:
            if first_element != second_element and (first_element, second_element) not in checks and (second_element, first_element) not in checks:
                similarity = get_sim_score(first_element, second_element)
                similarity_integral = get_mes_sim_integral_based(first_element, second_element)
                individuals_tuple_list.append((first_element, second_element, similarity))
                individuals_tuple_list_integral.append((first_element, second_element, similarity_integral))
            checks.add((first_element, second_element))

    individuals_tuple_list.sort(key=lambda x: x[2], reverse=True)
    individuals_tuple_list_integral.sort(key=lambda x: x[2])
    
    if verbose != 0:
        for similarity_tuple in individuals_tuple_list[:5]:
            cprint(similarity_tuple[0].name, 'cyan', attrs=["bold"])
            cprint(similarity_tuple[1].name, 'cyan', attrs=["bold"])
            cprint(similarity_tuple[2], 'green', attrs=["bold"])

        print()
    # integral_values = [v[2] for v in individuals_tuple_list_integral]
    # min_val = min(integral_values)
    # max_val = max(integral_values)
    # scaled_list = [(vs[0], vs[1], (vs[2] - min_val) / (max_val - min_val)) for vs in individuals_tuple_list_integral]
    # if verbose != 0:
        for similarity_tuple in individuals_tuple_list_integral[:5]:
            cprint(similarity_tuple[0].name, 'yellow', attrs=["bold"])
            cprint(similarity_tuple[1].name, 'yellow', attrs=["bold"])
            cprint(similarity_tuple[2], 'red', attrs=["bold"])
    return individuals_tuple_list
    

def get_sim_score(elem1: Measure, elem2: Measure):
    sc =  get_sc_score(elem1.chords, elem2.chords, "list")
    wc = 0.4
    sml = get_sml_score(elem1.duration, elem2.duration)
    wml = 0.1
    sr = get_sr_score(elem1.chords, elem2.chords)
    wsr = 0.3
    spd = get_spd_score(elem1.chords, elem2.chords)
    wpd = 0.2
    sm = wc * sc + wml * sml + sr * wsr + spd * wpd
    return sm

def get_sc_score(chord_list1, chord_list2, byCriteria: str):
    if byCriteria == "list":
        set_of_tuples = {tuple(chord.noteList) for chord in chord_list2}
        common_chords = [chord for chord in chord_list1 if tuple(chord.noteList) in set_of_tuples]

        return len(common_chords) / len(chord_list1 + chord_list2)
    
def get_sml_score(duration1, duration2):

    d1_float = float(duration1[0])
    d2_float = float(duration2[0])

    ml_diff = 0
    if d1_float > d2_float:
        ml_diff = d1_float - d2_float
    else:
        ml_diff = d2_float - d1_float

    return 1 if ml_diff == 0 else (1 - (ml_diff / (10 ** math.ceil(math.log10(ml_diff)))))

def get_sr_score(chord_list1, chord_list2):

    r_vec1 = [float(chord.duration[0]) for chord in chord_list1]
    r_vec2 = [float(chord.duration[0]) for chord in chord_list2]
    
    len_v1 = len(r_vec1)
    len_v2 = len(r_vec2)

    if len_v1 > len_v2:
        r_vec2 = np.concatenate([r_vec2, np.zeros(len_v1 - len_v2)])
    elif len_v2 > len_v1: 
        r_vec1 = np.concatenate([r_vec1, np.zeros(len_v2 - len_v1)])
    
    dot_p = np.dot(r_vec1, r_vec2)
    norm_v1 = np.linalg.norm(r_vec1)
    norm_v2 = np.linalg.norm(r_vec2)

    return dot_p / (norm_v1 * norm_v2)

def get_spd_score(chord_list1, chord_list2):
        all_values = {value for obj in chord_list1 + chord_list2 for value in obj.pitches}
        checked_values = set()
        # dictionary = {}
        jaccard_vect1 = []
        jaccard_vect2 = []
        for value in all_values:
            if(value not in checked_values):
                # Check if the value is in list1
                in_list1 = any(value in obj.pitches for obj in chord_list1)
                # Check if the value is in list2
                in_list2 = any(value in obj.pitches for obj in chord_list2)

                jaccard_vect1.append(1 if in_list1 else 0)
                jaccard_vect2.append(1 if in_list2 else 0)

                # dictionary[value] = [1 if in_list1 else 0, 1 if in_list2 else 0]

            checked_values.add(value)
        # cprint(dictionary, "cyan")
        # cprint(jaccard_vect2, "yellow")
        # cprint(jaccard_vect1, "green")
        # cprint(jaccard_binary(jaccard_vect1, jaccard_vect2), "blue")
        return jaccard_binary(jaccard_vect1, jaccard_vect2)

def jaccard_binary(x,y):
    intersection = np.logical_and(x, y)
    union = np.logical_or(x, y)
    similarity = intersection.sum() / float(union.sum())
    return similarity



# for measure in measure_attributes:
#     print(measure, measure_attributes[measure])


"""
To be implemented a function of frequency:
f(x)=A*sin(2pi*f*x)
Assumtions:
- all amplitudes are the same (use 1)
- there is no phase shift
- applied only on measures with the same length

"""

def g(x, c_list):
    sum_of_f = 0
    if isinstance(c_list, list):
        for c in c_list:
            sum_of_f += math.sin(2*math.pi*float(c)/100*x)
    else:
        sum_of_f += math.sin(2*math.pi*float(c_list)/100*x)
    return sum_of_f

def f(x, c_list):
    sum_of_f = 0
    if isinstance(c_list, list):
        for c in c_list:
            sum_of_f += math.sin(2*math.pi*float(c)*x)
    else:
        sum_of_f += math.sin(2*math.pi*float(c_list)/100*x)
    return sum_of_f

def get_mes_sim_integral_based(measure_element1, measure_element2):
    integral_score = 0
    sorted_chords_m1 = sorted(measure_element1.chords, key=lambda x: x.offset)
    sorted_chords_m2 = sorted(measure_element2.chords, key=lambda x: x.offset)
    if measure_element1.duration[0] == measure_element2.duration[0]:
        offsets1 = []
        offsets2 = []
        durations1 = []
        durations2 = []
        freqs1 = []
        freqs2 = []
        for chordm1 in sorted_chords_m1:
            offsets1.append(float(chordm1.offset[0]))
            durations1.append(float(chordm1.duration[0]))
            freqs1.append(chordm1.frequencies)
        for chordm2 in sorted_chords_m2:
            offsets2.append(float(chordm2.offset[0]))
            durations2.append(float(chordm2.duration[0]))
            freqs2.append(chordm2.frequencies)
        integral_score = get_dictionary_for_f_x(offsets1, offsets2, durations1, durations2, freqs1, freqs2, float(measure_element1.duration[0]))

    return integral_score

    # for elem in sorted_chords_m1:
    #     cprint(elem.offset, "green")
    #     cprint(max(elem.duration), "blue")
    # for elem in sorted_chords_m2:
    #     cprint(elem.offset, "yellow")
    #     cprint(max(elem.duration), "cyan")

def get_dictionary_for_f_x(offsets1, offsets2, durations1, durations2, freqs1, freqs2, m_duration):
    dict1, tup_list1 = compose_dict(offsets1, durations1, freqs1, m_duration)
    dict2, tup_list2 = compose_dict(offsets2, durations2, freqs2, m_duration)
    tup_list1.extend(tup_list2)
    final_composed = get_final_list(tup_list1)
    sum_integral = 0
  
    for part in final_composed:
        if isinstance(part[2], tuple):
            sum_integral += abs(quad(lambda x: f(x, part[2][0]) - g(x, part[2][1]), part[0], part[1])[0])
        else:
           sum_integral += abs(quad(lambda x: f(x, part[2]) - g(x, part[2]), part[0], part[1])[0])
            
    return sum_integral
    # Print the resulting dictionary
    
def compose_dict(list_offsets: list, list_durations: list, list_values: list, max_duration):
    dict = {}
    tup_list = []
    for i, offset in enumerate(list_offsets):
        dict[str([float(offset), offset+list_durations[i]])] = list_values[i]
        tup_list.append((float(offset), offset+list_durations[i], list_values[i]))
        if i < len(list_offsets) - 1:
            if offset+list_durations[i] < list_offsets[i+1]:
                dict[str([offset+list_durations[i], list_offsets[i+1]])] = 0
                tup_list.append((offset+list_durations[i], list_offsets[i+1], 0))
        elif offset+list_durations[i] < max_duration:
            dict[str([offset+list_durations[i], float(max_duration)])] = 0
            tup_list.append((offset+list_durations[i], float(max_duration), 0))
    return dict, tup_list


def get_final_list(extended_list):
    ranges = extended_list
    endpoints = sorted(list(set([r[0] for r in ranges] + [r[1] for r in ranges])))
    start = {}
    end = {}
    for e in endpoints:
        start[e] = set()
        end[e] = set()

    for r in ranges:
        start[r[0]].add(str(r[2]))
        end[r[1]].add(str(r[2]))

    current_ranges = set()

    final_list = []

    for e1, e2 in zip(endpoints[:-1], endpoints[1:]):
        current_ranges.difference_update(end[e1])
        current_ranges.update(start[e1])
        final_list.append([e1, e2, ast.literal_eval(','.join(current_ranges))])
        # print(e1, e2, ','.join(current_ranges))
    return final_list

def get_c_values(obj_values, offset, duration):
    return obj_values if float(offset) == 0.0 else 0

# Print the resulting dictionary

get_element_similarity(measure_object_list[:20], 1)
