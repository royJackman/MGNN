import argparse
import ast
import astpretty
import cProfile
import torch

import matplotlib.pyplot as plt
import networkx as nx

from astmonkey import visitors, transformers
from torch_geometric.data import Data
from torch_geometric.utils.convert import to_networkx

AST_LITERALS = (ast.Constant, ast.Num, ast.Str, ast.FormattedValue, ast.JoinedStr, ast.Bytes, ast.List, ast.Tuple, ast.Set, ast.Dict, ast.Ellipsis, ast.NameConstant)
AST_VARIABLES = (ast.Name, ast.Load, ast.Store, ast.Del, ast.Starred)
AST_EXPRESSIONS = (ast.Expr, ast.NamedExpr, ast.UnaryOp, ast.UAdd, ast.USub, ast.Not, ast.Invert, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd, ast.MatMult, ast.BoolOp, ast.And, ast.Or, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn, ast.Call, ast.keyword, ast.IfExp, ast.Attribute)
AST_SUBSCRIPT = (ast.Subscript, ast.Index, ast.Slice, ast.ExtSlice)
AST_COMPREHENSION = (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp, ast.comprehension)
AST_STATEMENTS = (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Raise, ast.Assert, ast.Delete, ast.Pass)
AST_IMPORTS = (ast.Import, ast.ImportFrom, ast.alias)
AST_CONTROL_FLOW = (ast.If, ast.For, ast.While, ast.Break, ast.Continue, ast.Try, ast.ExceptHandler, ast.With, ast.withitem)
AST_FUNCTIONS_CLASSES = (ast.FunctionDef, ast.Lambda, ast.arguments, ast.arg, ast.Return, ast.Yield, ast.YieldFrom, ast.Global, ast.Nonlocal, ast.ClassDef)
AST_ASYNC_AWAIT = (ast.AsyncFunctionDef, ast.Await, ast.AsyncFor, ast.AsyncWith)
AST_TOP_LEVEL = (ast.Module, ast.Interactive, ast.Expression)
AST_NODES = [node for nodelist in [AST_LITERALS, AST_VARIABLES, AST_EXPRESSIONS, AST_SUBSCRIPT, AST_COMPREHENSION, AST_STATEMENTS, AST_IMPORTS, AST_CONTROL_FLOW, AST_FUNCTIONS_CLASSES, AST_ASYNC_AWAIT, AST_TOP_LEVEL] for node in nodelist]

class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(node.name)
        self.generic_visit(node)

def clean_class(s):
    return s.replace('_ast.', '').replace('class', '').replace("'", '').replace("< ", '').replace(">", '')

parser = argparse.ArgumentParser(description='AST Dataset Generator')
parser.add_argument('-f', '--file', dest='filename', default='code/Addition.py', type=str, help='Filename to parse')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    tree = ast.parse(f.read())
    
# astpretty.pprint(tree.body[0], indent='  ', show_offsets=False)

edge_index = []
x = []

LITERALS = 0
VARIABLES = 0

next_nodes = [tree]
node_counter = [tree]
node_names = ['Module']
while len(next_nodes) > 0:
    curr = next_nodes.pop(0)
    if isinstance(curr, AST_LITERALS):
        LITERALS += 1
        x.append([0, AST_NODES.index(type(curr))])
        if isinstance(curr, ast.Constant):
            node_names[node_counter.index(curr)] += f': {curr.value}'
    elif isinstance(curr, AST_VARIABLES):
        VARIABLES += 1
        x.append([1, AST_NODES.index(type(curr))])
        if isinstance(curr, ast.Name):
            node_names[node_counter.index(curr)] += f': {curr.id}'
    elif isinstance(curr, AST_EXPRESSIONS):
        x.append([2, AST_NODES.index(type(curr))])
        if isinstance(curr, ast.Call):
            node_names[node_counter.index(curr)] += f': {curr.func.id if isinstance(curr.func, ast.Name) else curr.func.value.id}'
    elif isinstance(curr, AST_SUBSCRIPT):
        x.append([3, AST_NODES.index(type(curr))])
    elif isinstance(curr, AST_COMPREHENSION):
        x.append([4, AST_NODES.index(type(curr))])
    elif isinstance(curr, AST_STATEMENTS):
        x.append([5, AST_NODES.index(type(curr))])
    elif isinstance(curr, AST_IMPORTS):
        x.append([6, AST_NODES.index(type(curr))])
        if isinstance(curr, ast.alias):
            node_names[node_counter.index(curr)] += f': {curr.name} as {curr.asname}'
    elif isinstance(curr, AST_CONTROL_FLOW):
        x.append([7, AST_NODES.index(type(curr))])
    elif isinstance(curr, AST_FUNCTIONS_CLASSES):
        x.append([8, AST_NODES.index(type(curr))])
        if isinstance(curr, ast.FunctionDef):
            node_names[node_counter.index(curr)] += f': {curr.name}'
        elif isinstance(curr, ast.arg):
            node_names[node_counter.index(curr)] += f': {curr.arg}'
    elif isinstance(curr, AST_ASYNC_AWAIT):
        x.append([9, AST_NODES.index(type(curr))])
    elif isinstance(curr, AST_TOP_LEVEL):
        x.append([10, AST_NODES.index(type(curr))])
    else:
        x.append([11], -1)

    for child in ast.iter_child_nodes(curr):
        next_nodes.append(child)
        node_counter.append(child)
        child_idx = len(node_counter) - 1
        node_names.append(clean_class(str(type(child))))

        edge_index.append([node_counter.index(curr), child_idx])

data = Data(x=torch.tensor(x, dtype=torch.float), edge_index=torch.tensor(edge_index, dtype=torch.long).t().contiguous())
graph = to_networkx(data)
png_graph = nx.drawing.nx_pydot.to_pydot(graph)
for i, n in enumerate(node_counter):
    png_graph.get_node(str(i))[0].set_label(node_names[i] + f'\n {i}: {str(x[i])}')
# png_graph.get_node('0')[0].set_label(type(node_counter[0]))
png_graph.write_png('img/' + args.filename.split('/')[-1].replace('.py', '') + '_AST.png')