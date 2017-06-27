#!/usr/bin/env python
"""
Solve the Chinese-Postman problem.

For a given graph, determine the minimum amount of backtracking
required to complete an Eularian circuit.

"""
import argparse
import sys

import data.data
from chinesepostman import eularian, network

def setup_args():
    """ Setup argparse to take graph name argument. """
    parser = argparse.ArgumentParser(description='Find an Eularian Cicruit.')
    parser.add_argument('graph', nargs='?', help='Name of graph to load')
    args = parser.parse_args()
    return args.graph

from contextlib import contextmanager
import time

@contextmanager
def timeit_context(name):
    startTime = time.time()
    yield
    elapsedTime = time.time() - startTime
    print('[{}] finished in {} ms'.format(name, int(elapsedTime * 1000)))

def main():
    """ Make it so. """
    edges = None
    graph_name = setup_args()
    try:
        print('Loading graph: {}'.format(graph_name))
        edges = getattr(data.data, graph_name)
    except (AttributeError, TypeError):
        print('\nInvalid graph name. Available graphs:\n\t{}\n'.format(
            '\n\t'.join([x for x in dir(data.data)
            if not x.startswith('__')])))
        sys.exit()

    original_graph = network.Graph(edges)

    with timeit_context(graph_name):
        (total_edges, optional_edges) = original_graph.sizes()
        print('{} total edges with {} optional'.format(total_edges, optional_edges))
        if not original_graph.is_eularian():
            print('Converting to Eularian path...')
            graph = eularian.make_eularian(original_graph)
            print('Conversion complete')
            print('\tAdded {} edges'.format(len(graph) - len(original_graph)))
            print('\tTotal cost is {}'.format(graph.total_cost))
        else:
            graph = original_graph

        print('Attempting to solve Eularian Circuit...')
        route, attempts = eularian.eularian_path(graph, start='A')
        if not route:
            print('\tGave up after {} attempts.'.format(attempts))
        else:
            print('\tSolved in {} attempts'.format(attempts, route))
            print('Solution: ({} edges)'.format(len(route) - 1))
            print('\t{}'.format(route))

if __name__ == '__main__':
    main()
