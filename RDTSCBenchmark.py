import argparse
import ast
import rdtsc

parser = argparse.ArgumentParser(description='Benchmarking cycles for a program')
parser.add_argument('-f', '--file', dest='filename', type=str, help='File to benchmark')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    tree = ast.parse(f.read())

compiled = compile(tree, filename="<ast>", mode="exec")

start = rdtsc.get_cycles()
exec(compiled)
end = rdtsc.get_cycles()
print(f'Cycles: {end - start}')
