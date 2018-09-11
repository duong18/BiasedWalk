import numpy as np
import networkx as nx
import random
import heapq
from sets import Set


class Graph():
        def __init__(self, nx_G, is_directed, walk_length, i_value, is_BFS):
                self.G = nx_G
                self.is_directed = is_directed
                self.i_value = i_value            # the initialization value of phenomenon
                #self.window_size = window_size
                self.walk_length = walk_length
                self.is_BFS = is_BFS

                additions = [1.0]
                for i in range(walk_length):
                        additions.append(i_value*additions[i])
                self.additions = additions        
                print self.additions

                        
        def update_value(self, tau, u, l):
                #self.get_value(tau, u, l)
                if (tau.has_key(u)):
                        tau[u] = tau[u] + self.additions[l]
                else:
                        tau[u] = self.additions[l]

                return tau[u]


        def get_value(self, tau, u):
                if (tau.has_key(u) == False):
                        #tau[u] = self.additions[l]
                        print "unexpected error"
                        exit()

                return tau[u]

                        
        def simulate_walks(self, num_walks):
                '''
                Simulate jam walks from each node.
                '''
                G = self.G
                walk_length = self.walk_length
                walks = []
                nodes = list(G.nodes())
                
                in_adj = {}             # to difuse gifts
                out_adj = {}            # store neighbors for each node
                for node in nodes:
                        if (self.is_directed):
                                #in_adj[node] = G.predecessors(node)
                                # note: successors and neighbors are the same for directed networks
                                in_adj[node] = set(G.predecessors(node)).union(set(G.successors(node)))
                                out_adj[node] = set(G.successors(node))
                        else:
                                in_adj[node] = set(G.neighbors(node))
                                out_adj[node] = set(in_adj[node])
                                
                print 'Walk iteration:'
                random.shuffle(nodes)           # shuffle node set before doing random walks
                for i in range(num_walks):
                        print "Step:", i+1, "/", num_walks
                        for node in nodes:              # Wishky walk from this node
                                #if (out_adj[node] != []):               # the walk should have at least two nodes
                                tau = {}
                                walk = [node]
                                l = 0
                                
                                while (l < walk_length-1):
                                        u = walk[l]
                                        if (out_adj[u] == set()):          # cannot go further
                                                break
                                        for w in in_adj[u]:             # defuse to all (in, out) neighbors
                                                self.update_value(tau, w, l)

                                        total = 0.0
                                        r = random.random()
                                        summ = 0.0
                                        if (self.is_BFS):
                                                for v in out_adj[u]:
                                                        total = total + tau[v]*G[u][v]['weight']
                                                        
                                                for v in out_adj[u]:
                                                        summ = summ + tau[v]*G[u][v]['weight']
                                                        if (summ/total > r):
                                                                break
                                        else:
                                                for v in out_adj[u]:
                                                        total = total + np.reciprocal(tau[v])*G[u][v]['weight']
                                                        
                                                for v in out_adj[u]:
                                                        summ = summ + np.reciprocal(tau[v])*G[u][v]['weight']
                                                        if (summ/total > r):
                                                                break
                                                
                                        walk.append(v)
                                        l = l + 1
                                        
                                walks.append(walk)
                                #print i, walk
                                        
                return walks
