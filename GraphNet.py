import torch
import torch_geometric
import matplotlib.pyplot as plt 

from tqdm import trange
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class GCNConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super(GCNConv, self).__init__(aggr='mean')
        self.lin = torch.nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index):
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))

        x = self.lin(x)

        row, col = edge_index
        deg = degree(row, x.size(0), dtype=x.dtype)
        deg_inv_sqrt = deg.pow(-0.5)
        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]

        return self.propagate(edge_index, size=(x.size(0), x.size(0)), x=x, norm=norm)
    
    def message(self, x_j, norm):
        return norm.view(-1, 1) * x_j

class GraphNet(torch.nn.Module):
    def __init__(self, dataset):
        super(GraphNet, self).__init__()
        self.conv1 = GCNConv(dataset.num_node_features, 16)
        self.conv2 = GCNConv(16, dataset.num_classes)
    
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = torch.nn.functional.relu(x)
        x = torch.nn.functional.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return torch.nn.functional.log_softmax(x, dim=1)


dataset = torch_geometric.datasets.Planetoid(root='/tmp/Cora', name='Cora')

model = GraphNet(dataset)
data = dataset[0]
opti = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

tracc,  teacc = [], []
for epoch in trange(100):
    model.train()
    opti.zero_grad()
    out = model(data)
    loss = torch.nn.functional.nll_loss(out[data.train_mask], data.y[data.train_mask])
    tracc.append(loss.item())
    loss.backward()
    opti.step()
    teloss = torch.nn.functional.nll_loss(out[data.test_mask], data.y[data.test_mask])
    teacc.append(teloss.item())

fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(tracc)
axs[1].plot(teacc)
plt.show()