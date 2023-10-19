import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GCN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers):
        super().__init__()

        self.num_layers = num_layers
        self.convs = torch.nn.ModuleList() 
        self.convs.append(GCNConv(input_dim, hidden_dim))
        for _ in range(self.num_layers - 2): 
            self.convs.append(GCNConv(hidden_dim, hidden_dim))
        self.convs.append(GCNConv(hidden_dim, hidden_dim))

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        for i in range(self.num_layers):
            x = self.convs[i](x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, training=self.training)

        return F.log_softmax(x, dim=1)
    

# import torch
# import torch_geometric
# from torch_geometric.nn import GCNConv
# import torch.nn as nn
# import torch.nn.functional as F
# class GNNNodeClassifier(nn.Module):
#     def __init__(self, input_dim, hidden_dim):
#         super(GNNNodeClassifier, self).__init__()
#         self.conv1 = GCNConv(input_dim, hidden_dim)
#         self.conv2 = GCNConv(hidden_dim, hidden_dim)

#     def forward(self, data):
#         x, edge_index = data.x, data.edge_index
        
#         # Apply the first GCN layer
#         x = self.conv1(x, edge_index)
#         x = F.relu(x)
        
#         # Apply the second GCN layer (output layer)
#         x = self.conv2(x, edge_index)
        
#         return x