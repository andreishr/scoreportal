from rdflib import Graph

# Create a new RDF graph
graph = Graph()

# Load the TTL file into the graph
graph.parse("scoreportal/ontology.ttl", format="turtle")

# for subject, predicate, obj in graph:
#     print(f"Subject: {subject}")
#     print(f"Predicate: {predicate if predicate.split('#')[1] == 'hasInterval' else ''}")
#     print(f"Object: {obj}")

for subject, predicate, obj in graph:
    if predicate.split('#')[1] == 'hasInterval':
        print(f"Subject: {subject}")
        print(f"Predicate: {predicate}")
        print(f"Object: {obj}")
