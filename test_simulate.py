import numpy as np
import networkx as nx
import algorithmx

class PoW:

    def __init__(self, n_miners):
        self.n_miners = n_miners

G = nx.gnp_random_graph(10, 0.3, 138)

canvas = algorithmx.jupyter_canvas()
canvas.nodes(G.nodes).add()
canvas.edges(G.edges).add()

canvas