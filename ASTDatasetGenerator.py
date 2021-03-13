import ast
import astpretty
import torch

from astmonkey import visitors, transformers
from torch_geometric.data import Data

class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(node.name)
        self.generic_visit(node)

with open('Fibonacci.py', 'r') as f:
    tree = ast.parse(f.read())

astpretty.pprint(tree.body[0], indent='  ', show_offsets=False)

for node in ast.iter_child_nodes(tree):
    if isinstance(node, ast.FunctionDef):
        print('Func', node.name, node.lineno, node.args)
    elif isinstance(node, ast.Name):
        print('Name', node.id, node.lineno)
    elif isinstance(node, ast.Call):
        print('Call', node.func.id, node.lineno, node.args)
