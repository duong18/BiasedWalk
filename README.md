# BiasedWalk
This project is the implementation of BiasedWalk, a network representation learning method.

BiasedWalk is introduced in the paper: https://arxiv.org/abs/1809.02482

#### Example
To run *BiasedWalk* on [BlogCatalog network] (http://socialcomputing.asu.edu/datasets/BlogCatalog), execute the following command from the project home directory:<br/>
	``python source/main.py --i_value 0.5 --BFS --unweighted --undirected --input network_datasets/blog.edgelist --output emb/blog.emb``

#### Options
You can check out the other options available to use with *BiasedWalk* using:<br/>
	``python src/main.py --help``

#### Input
The supported input format is an edgelist:

	node1_id_int node2_id_int <weight_float, optional>
		
The graph is assumed to be undirected and unweighted by default. These options can be changed by setting the appropriate flags.

#### Output
The output file has *n+1* lines for a graph with *n* vertices. 
The first line has the following format:

	num_of_nodes dim_of_representation

The next *n* lines are as follows:
	
	node_id dim1 dim2 ... dimd

where dim1, ... , dimd is the *d*-dimensional representation learned by *BiasedWalk*.
