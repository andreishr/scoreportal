from rdflib import Graph
from node2vec import Node2Vec
import networkx as nx
import torch

graph = Graph()
graph.parse("scoreportal/ontologyv2.ttl", format="turtle")

nx_graph = nx.Graph()

for s, p, o in graph:
    nx_graph.add_node(s)
    nx_graph.add_node(o)
    nx_graph.add_edge(s, o)

node2vec = Node2Vec(nx_graph, dimensions=64, walk_length=30, num_walks=200, workers=1)
print("Node2ec initialized")
model = node2vec.fit(window=10, min_count=1, batch_words=4)
print("Fit completed, starting save...")
model.wv.save_word2vec_format('./modelv3emb.emb')
print("Embeddings saved, starting saving model")
model.save('./modelv3.model')
print("Model saved!")
