import networkx as nx
from gensim.models import KeyedVectors, Word2Vec
from node2vec import Node2Vec
from rdflib import Graph
from termcolor import colored, cprint

songs_file_path = './similarity_songs.txt'

# Load the pre-trained Node2Vec model
model = Word2Vec.load('./modelv2.model')

# Load the Word2Vec embeddings
word_vectors = model.wv

# Load the ontology graph from ttl file
graph = Graph()
graph.parse("scoreportal/ontology.ttl", format="turtle")

# Create an empty NetworkX graph
nx_graph = nx.Graph()
songs_list = []
chord_list = []

song_uri_constant = "http://onemusiconto.com/omo#Song"
part_uri_constant = "http://onemusiconto.com/omo#Part"
chord_uri_constant = "http://onemusiconto.com/omo#Chord"
measure_uri_constant = "http://onemusiconto.com/omo#Measure"
pitch_uri_constant = "http://onemusiconto.com/omo#Pitch"
interval_uri_constant = "http://onemusiconto.com/omo#MusicInterval"

for s, p, o in graph:

    if song_uri_constant in o:
        songs_list.append(s)

    if chord_uri_constant in o:
        chord_list.append(s)

    nx_graph.add_node(s)
    nx_graph.add_node(o)
    nx_graph.add_edge(s, o)

# def get_songs_similarity(nxgraph : Graph):
#     for node1 in nxgraph.nodes():
#         for node2 in nxgraph.nodes():
#             if node1 != node2:
#                 similarity = word_vectors.similarity(str(node1), str(node2))
#                 print(f"Similarity between {node1} and {node2}: {similarity}")

def get_songs_similarity(elements):
    individuals_tuple_list = []
    checks = set()
    for first_element in elements:
        for second_element in elements:
            if first_element != second_element and (first_element, second_element) not in checks and (second_element, first_element) not in checks:
                similarity = word_vectors.similarity(str(first_element), str(second_element))
                individuals_tuple_list.append((first_element, second_element, similarity))
            checks.add((first_element, second_element))

    individuals_tuple_list.sort(key=lambda x: x[2], reverse=True)
    
    for similarity_tuple in individuals_tuple_list[:50]:
        cprint(similarity_tuple[0], 'cyan', attrs=["bold"])
        cprint(similarity_tuple[1], 'cyan', attrs=["bold"])
        cprint(similarity_tuple[2], 'green', attrs=["bold"])

    print(len(individuals_tuple_list))
    return individuals_tuple_list

song_similarity_list = get_songs_similarity(songs_list)

def write_to_file(file, list_of_tuples):
    with open(file, 'w') as file:
        for tpl in list_of_tuples:
            line = ','.join(map(str, tpl))
            file.write(line + '\n') 

print(len(songs_list))
# write_to_file(songs_file_path, song_similarity_list)