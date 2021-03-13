import ast
import astpretty
import pydot
import torch

import matplotlib.pyplot as plt
import networkx as nx

from astmonkey import visitors, transformers
from torch_geometric.data import Data
from torch_geometric.utils.convert import to_networkx

class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(node.name)
        self.generic_visit(node)

with open('code/Addition.py', 'r') as f:
    tree = ast.parse(f.read())

astpretty.pprint(tree.body[0], indent='  ', show_offsets=False)

edge_index = []
x = []

next_nodes = [tree]
node_counter = [tree]
while len(next_nodes) > 0:
    curr = next_nodes.pop(0)

    if isinstance(curr, (ast.Constant, ast.Num, ast.Str, ast.FormattedValue, ast.JoinedStr, ast.Bytes, ast.List, ast.Tuple, ast.Set, ast.Dict, ast.Ellipsis, ast.NameConstant)):
        x.append([0])
    elif isinstance(curr, (ast.Name, ast.Load, ast.Store, ast.Del, ast.Starred)):
        x.append([1])
    elif isinstance(curr, (ast.Expr, ast.NamedExpr, ast.UnaryOp, ast.UAdd, ast.USub, ast.Not, ast.Invert, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd, ast.MatMult, ast.BoolOp, ast.And, ast.Or, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn, ast.Call, ast.keyword, ast.IfExp, ast.Attribute)):
        x.append([2])
    elif isinstance(curr, (ast.Subscript, ast.Index, ast.Slice, ast.ExtSlice)):
        x.append([3])
    elif isinstance(curr, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp, ast.comprehension)):
        x.append([4])
    elif isinstance(curr, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Raise, ast.Assert, ast.Delete, ast.Pass)):
        x.append([5])
    elif isinstance(curr, (ast.Import, ast.ImportFrom, ast.alias)):
        x.append([6])
    elif isinstance(curr, (ast.If, ast.For, ast.While, ast.Break, ast.Continue, ast.Try, ast.ExceptHandler, ast.With, ast.withitem)):
        x.append([7])
    elif isinstance(curr, (ast.FunctionDef, ast.Lambda, ast.arguments, ast.arg, ast.Return, ast.Yield, ast.YieldFrom, ast.Global, ast.Nonlocal, ast.ClassDef)):
        x.append([8])
    elif isinstance(curr, (ast.AsyncFunctionDef, ast.Await, ast.AsyncFor, ast.AsyncWith)):
        x.append([9])
    elif isinstance(curr, (ast.Module, ast.Interactive, ast.Expression)):
        x.append([10])
    else:
        x.append([11])

    for child in ast.iter_child_nodes(curr):
        next_nodes.append(child)
        node_counter.append(child)
        edge_index.append([node_counter.index(curr), node_counter.index(child)])

data = Data(x=torch.tensor(x, dtype=torch.float), edge_index=torch.tensor(edge_index, dtype=torch.long).t().contiguous())
print(data)
graph = to_networkx(data)
png_graph = nx.drawing.nx_pydot.to_pydot(graph)
png_graph.write_png('out.png')