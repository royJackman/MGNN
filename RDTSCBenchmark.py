import argparse
import ast
import rdtsc

import numpy as np

parser = argparse.ArgumentParser(description='Benchmarking cycles for a program')
parser.add_argument('-f', '--file', dest='filename', type=str, help='File to benchmark')
parser.add_argument('-i', '--iterations', dest='iterations', type=int, help='Number of times to run compiled code')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    tree = ast.parse(f.read())

compiled = compile(tree, filename="<ast>", mode="exec")
cycles = []
for i in range(args.iterations):
    start = rdtsc.get_cycles()
    exec(compiled)
    end = rdtsc.get_cycles()
    cycles.append(end - start)
cycles = np.array(cycles)
print(f'For {args.iterations} cycles\nMean:\t{np.mean(cycles)}\tMax:\t{np.max(cycles)}\tMin:\t{np.min(cycles)}\tStd:\t{np.std(cycles)}\tVar:\t{np.var(cycles)}')
