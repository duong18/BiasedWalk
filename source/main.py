'''
BiasedWalk implementation. 
 
Author: Duong Nguyen, Fragkiskos Malliaros
 
The implementation is partially based on the following open source projects:
node2vec, https://github.com/aditya-grover/node2vec
Deepwalk, https://github.com/phanein/deepwalk
'''

import argparse
import numpy as np
import networkx as nx
import biased_walk
from gensim.models import Word2Vec


def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run node2vec.")

	parser.add_argument('--input', nargs='?', default='../graph/?',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='../emb/?',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')

	parser.add_argument('--walk-length', type=int, default=80,
	                    help='Length of walk per source. Default is 80.')

	parser.add_argument('--num-walks', type=int, default=10,
	                    help='Number of walks per source. Default is 10.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--iter', default=1, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--workers', type=int, default=4,
	                    help='Number of parallel workers. Default is 8.')

	#parser.add_argument('--p', type=float, default=1.0,
	#                    help='Return hyperparameter. Default is 1.')

	#parser.add_argument('--q', type=float, default=1.0,
	#                    help='Inout hyperparameter. Default is 1.')

	parser.add_argument('--i_value', type=float, default=1.0,
	                    help='Multitative factor. Default is 1.0')

	#parser.add_argument('--alpha', type=float, default=0.1,
	#                    help='addition percentage for each update. Default is 0.1')

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	parser.add_argument('--BFS', dest='BFS', action='store_true',
	                    help='Do random walks based on DFS(BFS). Default is DFS.')
	parser.add_argument('--DFS', dest='DFS', action='store_false')
	parser.set_defaults(BFS=False)

	return parser.parse_args()


def read_graph():
	'''
	Reads the input network in networkx.
	'''
	if args.weighted:
		G = nx.read_edgelist(args.input, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist(args.input, nodetype=int, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not args.directed:
		G = G.to_undirected()

	return G


def learn_embeddings(walks):
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	walks = [map(str, walk) for walk in walks]              # convert walks to sentences
	model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, sg=1, workers=args.workers, iter=args.iter)
	model.wv.save_word2vec_format(args.output)
	
	return


def main(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''
	nx_G = read_graph()
	G = biased_walk.Graph(nx_G, args.directed, args.walk_length, args.i_value, args.BFS)
	print "args.directed", args.directed
	print "args.weighted", args.weighted
	print "args.walk_length", args.walk_length
	print "args.window_size", args.window_size
	print "args.i_value", args.i_value
	print "args.BFS", args.BFS
	print "DONE-read_graph()"
	
	walks = G.simulate_walks(args.num_walks)
	print "DONE-G.simulate_walks(args.num_walks)"
	learn_embeddings(walks)
	print "DONE-ALL"

if __name__ == "__main__":
	args = parse_args()
	main(args)
