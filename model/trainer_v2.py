from rdflib import Graph
from node2vec import Node2Vec
import networkx as nx
import torch


print(torch.cuda.is_available())
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

# Load the ontology graph from ttl file
graph = Graph()
graph.parse("scoreportal/ontology.ttl", format="turtle")

nx_graph = nx.Graph()

for s, p, o in graph:
    nx_graph.add_node(s)
    nx_graph.add_node(o)
    nx_graph.add_edge(s, o)


# Create an instance of Node2Vec
node2vec = Node2Vec(nx_graph, dimensions=64, walk_length=30, num_walks=200, workers=1)

# Train Node2Vec model
model = node2vec.fit(window=10, min_count=1, batch_words=4)

model.wv.save_word2vec_format('./modelv2emb.emb')
model.save('./modelv2.model')
# # Get similarity between individuals
# similarity = model.wv.similarity('individual_1', 'individual_2')
# print(f"Similarity between individual_1 and individual_2: {similarity}")