from parsingttl import graph, get_interval_rdfs
from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.embedders import Word2Vec 
from pyrdf2vec.graphs import KG, Vertex
from pyrdf2vec.walkers import RandomWalker
from tqdm import tqdm
# print(get_interval_rdfs())

if __name__ == '__main__':
    kg = KG()

    list_entities = []

    for subject, predicate, obj in graph:   
        s = Vertex(str(subject))
        list_entities.append(s.name)
        o = Vertex(str(obj))
        list_entities.append(o.name)
        p = Vertex(str(predicate), predicate=True, vprev = s, vnext = o)
        kg.add_walk(s, p, o)
                
    # for entity in list_entities:
    #     print(Vertex(entity.name))

    # for entity in kg._entities:
    #     print(entity)

    # Create an RDF2VecTransformer
    rdf2vec = RDF2VecTransformer(
        Word2Vec(epochs=1),
        walkers=[RandomWalker(4, 10, with_reverse=False, n_jobs=2)], verbose=1)  # Adjust parameters as needed


    embeddings, literals = rdf2vec.fit_transform(kg, list_entities)

    rdf2vec.save("model_data")

    for literal, embedding in zip(literals, embeddings):
        print(f"Entity: {literal}, Embedding: {embedding}")
