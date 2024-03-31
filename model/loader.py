from gensim.models import Word2Vec

from rdflib import Graph
from termcolor import  cprint
import os
from dotenv import load_dotenv

load_dotenv()
songs_file_path = './similarity_songs.txt'
song_uri_constant = os.getenv('SONG_URI_CONSTANT')
part_uri_constant = os.getenv('PART_URI_CONSTANT')
chord_uri_constant = os.getenv('CHORD_URI_CONSTANT')
measure_uri_constant = os.getenv('MEASURE_URI_CONSTANT')
pitch_uri_constant = os.getenv('PITCH_URI_CONSTANT')
interval_uri_constant = os.getenv('INTERVAL_URI_CONSTANT')

# Load the pre-trained Node2Vec model
model = Word2Vec.load('./modelv2.model')
# Load the Word2Vec embeddings
word_vectors = model.wv
# Load the ontology graph from ttl file
graph = Graph()
graph.parse("scoreportal/ontology.ttl", format="turtle")


# Declaring utils
songs_list = []
chord_list = []
measure_list = []



for s, p, o in graph:

    if song_uri_constant in o:
        songs_list.append(s)

    if chord_uri_constant in o and len(chord_list) < 150:
        chord_list.append(s)

    if measure_uri_constant in o and len(measure_list) < 200:
        measure_list.append(s)


def get_element_similarity(elements, verbose = 0):
    individuals_tuple_list = []
    checks = set()
    for first_element in elements:
        for second_element in elements:
            if first_element != second_element and (first_element, second_element) not in checks and (second_element, first_element) not in checks:
                similarity = word_vectors.similarity(str(first_element), str(second_element))
                individuals_tuple_list.append((first_element, second_element, similarity))
            checks.add((first_element, second_element))

    individuals_tuple_list.sort(key=lambda x: x[2], reverse=True)
    
    if verbose != 0:
        for similarity_tuple in individuals_tuple_list[:150]:
            cprint(similarity_tuple[0], 'cyan', attrs=["bold"])
            cprint(similarity_tuple[1], 'cyan', attrs=["bold"])
            cprint(similarity_tuple[2], 'green', attrs=["bold"])

    return individuals_tuple_list

measure_similarity_list = get_element_similarity(measure_list, 1)

def write_to_file(file, list_of_tuples):
    with open(file, 'w') as file:
        for tpl in list_of_tuples:
            line = ','.join(map(str, tpl))
            file.write(line + '\n') 

