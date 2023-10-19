from rdflib import Graph, URIRef
import torch
from torch_geometric.data import Data
from model_trainer import GCN
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from tqdm import tqdm

from torch_geometric.datasets import Planetoid
# Put cuda to device
device = "cuda" if torch.cuda.is_available() else "cpu"
print('Device', device)
# Create a new RDF graph
graph = Graph()

# Load the TTL file into the graph
graph.parse("scoreportal/ontology.ttl", format="turtle")

nodes = set()
objects = {}


for s, p, o in graph:
    nodes.add(s)
    if s in objects:
        objects[s].append(o)
    else:
        objects[s] = [o]

    nodes.add(o)

# print(len(nodes))
count_values = {}

for objectt in objects:
    # print(f'Key: {objectt}')
    # print(f'Values: {objects[objectt]}\n')
    # print(f'Number of values: {len(objects[objectt])}\n')
    if len(objects[objectt]) in count_values:
        count_values[len(objects[objectt])] += 1
    else:
        count_values[len(objects[objectt])] = 1

print(count_values)

count_values_sorted = dict(sorted(count_values.items(), key=lambda item: item[1], reverse=True))

# Print the sorted dictionary
print(count_values_sorted)

node_to_id = {node: i for i, node in enumerate(nodes)}

edges = []
for s, _, o in graph:
    if isinstance(s, URIRef) and isinstance(o, URIRef):
        source_node = node_to_id[s]
        target_node = node_to_id[o]
        edges.append([source_node, target_node])

x = torch.randn(len(nodes), 4)
# Convert data into PyTorch tensors
# x = torch.tensor([[node_to_id[node]] for node in node_to_id], dtype=torch.float)  # Replace with your actual node features
edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

# Make data and valdiate
data = Data(edge_index=edge_index, x=x).to(device)

data.validate(raise_on_error=True)
print(data)
print(f'Data node features: {data.num_node_features}')
print(f'Has isolated nodes: {data.has_isolated_nodes()}')
print(f'Has self loops: {data.has_self_loops()}')
print(f'Is directed: {data.is_directed()}\n')



input_dim = x.size(1) # Get number of features as first layer dimension
hidden_dim = x.size(1) # Size of hidden layer
model = GCN(input_dim, hidden_dim, 10).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
criterion = nn.MSELoss()

# TEST
# dataset = Planetoid(root='/tmp/Cora', name='Cora')
# data = dataset[0]
# print(data)

num_epochs = 10
model.train()
for epoch in range(num_epochs):
    optimizer.zero_grad()
    out = model(data)
    loss = criterion(out, torch.zeros_like(out))  # Example loss (minimize distance to zero embeddings)
    loss.backward()
    optimizer.step()
    print(f'Loss value: {loss}')
# model.train()
# for epoch in range(10):
#     optimizer.zero_grad()
#     out = model(data)
#     loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
#     loss.backward()
#     optimizer.step()


# model.eval()
# pred = model(data).argmax(dim=1)
# correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
# acc = int(correct) / int(data.test_mask.sum())
# print(f'Accuracy: {acc:.4f}')
# Initialize the GNN model
# input_dim = x.size(1)
# print(input_dim)
# hidden_dim = 16
# model = GNNNodeClassifier(input_dim, hidden_dim)

# # Define loss and optimizer
# criterion = nn.MSELoss()
# optimizer = optim.Adam(model.parameters(), lr=0.01)

# num_epochs = 20

# # Training loop (for demonstration purposes)
# for epoch in range(num_epochs):

#     optimizer.zero_grad()
#     embeddings = model(data)

#     # Compute similarity (cosine similarity) between embeddings of songs
#     query_embedding = embeddings[0]  # Example: Select the first song as the query
#     song_embeddings = embeddings[1:]  # Exclude the query song
#     similarities = F.cosine_similarity(query_embedding, song_embeddings)

#     # Print similarity scores for demonstration
    
#     print(f'Epoch: {epoch + 1}, Similarities: {similarities}')

#     # You can use similarity scores to find similar songs
#     loss = criterion(embeddings, torch.zeros_like(embeddings))  # Example loss (minimize distance to zero embeddings)
#     loss.backward()
#     optimizer.step()
#     print(f'Loss value: {loss}')
#     print('\n')
