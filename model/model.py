from parsingttl import graph, get_interval_rdfs
from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.embedders import Word2Vec
from pyrdf2vec.graphs import KG
from pyrdf2vec.walkers import RandomWalker
# print(get_interval_rdfs())


for subject, predicate, obj in graph:
        if predicate.split('#')[1] == 'hasInterval':
            print(f"Subject: {subject}")
            print(f"Predicate: {predicate}")
            print(f"Object: {obj}")
            