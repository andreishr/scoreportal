from rdflib import Graph
from termcolor import  cprint
import os
from dotenv import load_dotenv
import ast
import math
import numpy as np
from scipy.integrate import quad
import sympy as smp

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

def write_to_file(file, list_of_tuples):
    with open(file, 'w') as file:
        for tpl in list_of_tuples:
            line = ','.join(map(str, tpl))
            file.write(line + '\n') 

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
        print("STEP...")
        for second_element in elements:
            if first_element != second_element and (first_element, second_element) not in checks and (second_element, first_element) not in checks:
                similarity = get_sim_score(first_element, second_element)
                if len(first_element.duration) > 0 and len (second_element.duration) > 0:
                    if (first_element.duration[0] == second_element.duration[0]):
                        similarity_integral, similariy_with_abs = get_mes_sim_integral_based(first_element, second_element)
                        individuals_tuple_list_integral.append((first_element, second_element, similarity_integral, similariy_with_abs))
                individuals_tuple_list.append((first_element, second_element, similarity))
            checks.add((first_element, second_element))

    individuals_tuple_list.sort(key=lambda x: x[2], reverse=True)
    individuals_tuple_list_integral.sort(key=lambda x: x[2])
    
    if verbose != 0:
        for similarity_tuple in individuals_tuple_list[:5]:
            cprint(similarity_tuple[0].name, 'cyan', attrs=["bold"])
            cprint(similarity_tuple[1].name, 'cyan', attrs=["bold"])
            cprint(similarity_tuple[2], 'green', attrs=["bold"])

        print()
    integral_values = [v[2] for v in individuals_tuple_list_integral]
    min_val = 0
    max_val = max(integral_values)
    print(min_val)
    print(max_val)
    scaled_list = [(vs[0], vs[1], (vs[2] - min_val) / (max_val - min_val)) for vs in individuals_tuple_list_integral]
    if verbose != 0:
        for similarity_tuple in individuals_tuple_list_integral[:30]:
            cprint(similarity_tuple[0].name, 'yellow', attrs=["bold"])
            cprint(similarity_tuple[1].name, 'yellow', attrs=["bold"])
            cprint(similarity_tuple[2], 'red', attrs=["bold"])
            cprint(f"ABS: {similarity_tuple[3]}", 'light_red', attrs=["bold"])
        cprint("UNSCALED:", "blue")
        # for similarity_tuple in scaled_list[:100]:
        #     cprint(similarity_tuple[0].name, 'yellow', attrs=["bold"])
        #     cprint(similarity_tuple[1].name, 'yellow', attrs=["bold"])
        #     cprint(similarity_tuple[2], 'red', attrs=["bold"])

    # write_to_file("not_scaled", [(similarity_tuple[0].name, similarity_tuple[1].name, similarity_tuple[2]) for similarity_tuple in individuals_tuple_list_integral])
    # write_to_file("scaled", [(similarity_tuple[0].name, similarity_tuple[1].name, similarity_tuple[2]) for similarity_tuple in scaled_list])

    
    return individuals_tuple_list
    

def get_sim_score(elem1: Measure, elem2: Measure):
    #Todo aici conditie
    sc =  get_sc_score(elem1.chords, elem2.chords, "list")
    wc = 0.4
    sml = 0
    if len(elem1.duration) > 0 and len(elem2.duration) > 0:
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
                in_list1 = any(value in obj.pitches for obj in chord_list1)
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


"""
To be implemented a function of frequency:
f(x)=A*sin(2pi*f*x)
Assumtions:
- all amplitudes are the same (use 1)
- there is no phase shift
- applied only on measures with the same length
- if a chord contains a list of frequencies that is not changed spanning multiple times, it was continuously played, 
    if it has at least one frequency value changed, it is a new chord 

"""

def g(x, c_list):
    sum_of_g = 0
    if isinstance(c_list, list):
        for c in c_list:
            sum_of_g += np.sin(2*math.pi*float(c)*x)
    else:
        sum_of_g += np.sin(2*math.pi*float(c_list)*x)
    return abs(sum_of_g)

def f(x, c_list):
    sum_of_f = 0
    if isinstance(c_list, list):
        for c in c_list:
            sum_of_f += np.sin(2*math.pi*float(c)*x)
    else:
        sum_of_f += np.sin(2*math.pi*float(c_list)*x) 
    return sum_of_f

# def diff_f(x, c_list1, c_list2):
#     return abs(f(x, c_list1) - g(x, c_list2))


def get_mes_sim_integral_based(measure_element1, measure_element2):
    integral_score = 0
    integral_score_abs = 0
    sorted_chords_m1 = sorted(measure_element1.chords, key=lambda x: x.offset)
    sorted_chords_m2 = sorted(measure_element2.chords, key=lambda x: x.offset)
    if len(measure_element1.duration) > 0 and len(measure_element2.duration) > 0:
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
                freqs1.append((chordm1.frequencies, chordm1.offset[0]))
            for chordm2 in sorted_chords_m2:
                offsets2.append(float(chordm2.offset[0]))
                durations2.append(float(chordm2.duration[0]))
                freqs2.append((chordm2.frequencies, chordm2.offset[0]))
            integral_score, integral_score_abs = get_integral_score(offsets1, offsets2, durations1, durations2, freqs1, freqs2, float(measure_element1.duration[0]))
    return integral_score, integral_score_abs

def get_integral_score(offsets1, offsets2, durations1, durations2, freqs1, freqs2, m_duration):
    dict1, tup_list1 = compose_dict(offsets1, durations1, freqs1, m_duration)
    dict2, tup_list2 = compose_dict(offsets2, durations2, freqs2, m_duration)
    tup_list1.extend(tup_list2)
    final_composed = get_final_list(tup_list1)
    sum_integral = 0
    sum_integral_abs = 0
    cprint(f"Total number of integrals required: {len(final_composed)}", "red", attrs=["bold"])
    for i, part in enumerate(final_composed):
        cprint(part, "green")
        part_integrating_intervals = []
        if i > 0:
            if isinstance(part[2], tuple):
                # Entering both measures 
                for chord_freqs_and_offs in part[2]:
                    interval = []
                    if isinstance(chord_freqs_and_offs, tuple):
                        if float(chord_freqs_and_offs[1]) < float(part[0]):
                            interval = [final_composed[i-1][1] - final_composed[i-1][0], final_composed[i-1][1] - final_composed[i-1][0] + part[1] - part[0]]
                        else:
                            interval = [0, part[1] - part[0]]
                    else:
                        if chord_freqs_and_offs == 0:
                            #No singing case
                            interval = [0, 0]
                        else:
                            interval = [0, part[1] - part[0]]
                        # Debug print to see the nature of chords_and_freqs, it might not be a nested list and for loop will iterate through content
                        # cprint(chord_freqs_and_offs, "blue")
                    part_integrating_intervals.append(tuple(interval))
            else:
                # No singing in both measures case
                part_integrating_intervals.append((0, 0))
        else:
            # i == 0 first integral
            # cprint(part, "red")
            part_integrating_intervals.append((part[0], part[1]))
            # Append twie to avoid index ou of range below - don't want to add another condition...:/
            part_integrating_intervals.append((part[0], part[1]))

        cprint(part_integrating_intervals, "cyan", attrs=["bold"])

        if isinstance(part[2], tuple):
            if not isinstance(part[2][1], tuple) and not isinstance(part[2][0], tuple):
                cprint("Single tuple case: Integral should be 0", "yellow")
                cprint(part_integrating_intervals, "magenta")
                # This integral should be 0! 
                i = quad(f, part_integrating_intervals[0][0], part_integrating_intervals[0][1], args=(part[2][1]))
                cprint(f"Integral value: {0}", "light_blue", attrs=["bold"])
                print("\n")
            else:
                cprint("Double tuple/0 and tuple case:", "yellow")
                cprint(part_integrating_intervals, "magenta")
                i1 = quad(f, part_integrating_intervals[0][0], part_integrating_intervals[0][1], args=(part[2][0][0] if isinstance(part[2][0], tuple) else part[2][0]))
                i2 = quad(f, part_integrating_intervals[1][0], part_integrating_intervals[1][1], args=(part[2][1][0] if isinstance(part[2][1], tuple) else part[2][1]))
                i3 = quad(g, part_integrating_intervals[0][0], part_integrating_intervals[0][1], args=(part[2][0][0] if isinstance(part[2][0], tuple) else part[2][0]))
                i4 = quad(g, part_integrating_intervals[1][0], part_integrating_intervals[1][1], args=(part[2][1][0] if isinstance(part[2][1], tuple) else part[2][1]))
                cprint(f"First chord or 0 integral: {i1}", "light_green")
                cprint(f"First chord or 0 integral: {i2}", "light_green")
                cprint(f"Integral subtraction value: {i1[0]-i2[0]}", "light_blue", attrs=["bold"])
                print("\n")
                sum_integral+=abs(i1[0] - i2[0])
                sum_integral_abs+=abs(i3[0] - i4[0])
        else:
            cprint(part_integrating_intervals, "magenta")
            cprint("0 - not tuple case:", "yellow")
            cprint(f"Default integral value: {0}", "light_blue", attrs=["bold"])



    # for part in final_composed:
    #     if isinstance(part[2], tuple):
    #         # sum_integral += abs(quad(lambda x: f(x, part[2][0]) - g(x, part[2][1]), part[0], part[1], limit=50)[0])
    #         sum_integral += quad(diff_f, part[0], part[1], args=(part[2][0], part[2][1]), limit=100)[0]
    #     else:
    #     #    sum_integral += abs(quad(lambda x: f(x, part[2]) - g(x, part[2]), part[0], part[1], limit=50)[0])
    #         sum_integral += quad(diff_f, part[0], part[1], args=(part[2], part[2]), limit=100)[0]

    cprint(sum_integral, "light_red", attrs=["bold"])
    return sum_integral, sum_integral_abs
    
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
        if current_ranges == set():
            current_ranges.add('0')
            final_list.append([e1, e2, ast.literal_eval(','.join(current_ranges))])
        else:
            final_list.append([e1, e2, ast.literal_eval(','.join(current_ranges))]) 
    return final_list

def get_c_values(obj_values, offset, duration):
    return obj_values if float(offset) == 0.0 else 0


get_element_similarity(measure_object_list[:5], 1)




# cprint(abs(quad(lambda x: f(x, ["1", "2.5"]) - g(x, ["2", "0.666"]), 0, 3, limit=100)[0]), "yellow")
# cprint(abs(quad(diff_f, 0, 3, args=(["1", "2.5"], ["2", "0.666"]), limit=100)[0]), "red")


# cprint(quad(f, 0, 3, args=["1", "2.5"]), "blue")
# cprint(quad(g, 0, 3, args=["2", "0.666"]), "red")
# cprint(quad(f, 0, 3, args=["1", "2.5"])[0] - quad(g, 0, 3, args=["2", "0.666"])[0], "green")

# x = smp.symbols('x', real=True)
# h = smp.sin(2*smp.pi*x) + smp.sin(2*smp.pi*2.5*x)
# t = smp.sin(2*smp.pi*2*x) + smp.sin(2*smp.pi*0.666*x)

# cprint(smp.integrate(f(x, ["1", "2.5"]), (x, 0, 6)))

# i1 = smp.integrate(h, (x, 0, 3))
# i2 = smp.integrate(h, (x, 0, 3))
# i3 = smp.integrate(h-t, (x, 0 ,3))
# print(i1)
# print(i2)
# print(i1-i2)
# print(i3.evalf())