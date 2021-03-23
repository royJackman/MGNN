import argparse
import ast

from hwcounter import Timer, count, count_end
from tqdm import trange

parser = argparse.ArgumentParser(description='Benchmarking cycles for a program')
parser.add_argument('-f', '--file', dest='filename', type=str, help='File to benchmark')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    tree = ast.parse(f.read())

compiled = compile(tree, filename="<ast>", mode="exec")

with Timer() as t:
    exec(compiled)
print(f'Elapsed: {t.cycles}')
