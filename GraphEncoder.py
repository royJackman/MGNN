import torch
import torch_geometric

from torch_geometric.nn import SAGPooling, GCNConv

class GraphEncoder(torch.nn.Module):
    def __init__(self, in_channels, out_channels, inner_dim=16, ratio=0.5, pools=2):
        super(GraphEncoder, self).__init__()
        self.in_conv = GCNConv(in_channels, inner_dim)
        self.out_conv = GCNConv(inner_dim, out_channels)
        self.in_pools = torch.nn.ModuleList([])
        self.out_pools = []
        
        for p in range(pools):
            self.in_pools.append(SAGPooling(inner_dim, ratio=ratio))
            self.out_pools.append(SAGPooling(inner_dim, ratio=1.0/ratio))
        
        self.out_pools = torch.nn.ModuleList(list(reversed(self.out_pools)))
    
    def forward(self, x, edge_index, out_index):
        out = [torch.relu(self.in_conv(x, edge_index)), edge_index]
        for p in self.in_pools:
            print(out[0].shape, out[1].shape)
            out = p(out[0], out[1])
        return torch.relu(self.out_conv(out[0], out_index))
