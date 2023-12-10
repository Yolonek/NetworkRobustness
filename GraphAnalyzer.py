import networkx as nx
import numpy as np
from networkx.exception import NetworkXError, NodeNotFound, NetworkXNoPath
from matplotlib import pyplot as plt


class ErdosRenyiGraphGenerator(object):
    def __init__(self, p=0.5, N=1):
        self.N = N
        self.p = p
        self.initial_grid = None
        self.current_grid = None
        self.link_list = None
        self.graph = nx.Graph()

    def set_initial_grid(self, initial_grid=None):
        if initial_grid is None:
            self.initial_grid = np.triu(np.random.random((self.N, self.N)), k=1)
        else:
            self.initial_grid = np.triu(initial_grid, 1)

    def grid_thresholding(self):
        self.current_grid = np.where(self.initial_grid < 1 - self.p, 0, 1).astype(int)

    def print_grid(self, initial=True):
        with np.printoptions(precision=3):
            if initial:
                print(self.initial_grid + np.eye(self.N))
            else:
                print(self.current_grid + np.eye(self.N, dtype=int))

    def convert_grid_to_link_tuple_(self):
        self.link_list = []
        link_cords = np.where(self.current_grid == 1)
        x_cords = link_cords[0]
        y_cords = link_cords[1]
        for x, y in zip(x_cords, y_cords):
            link_tuple = (int(x), int(y))
            self.link_list.append(link_tuple)

    def convert_grid_to_link_tuple(self):
        x_cords, y_cords = np.where(self.current_grid == 1)
        self.link_list = np.concatenate((x_cords[:, None], y_cords[:, None]), axis=1)

    def create_graph(self):
        self.graph.add_nodes_from(range(self.N))
        self.graph.add_edges_from(self.link_list)

    def generate_all_graph_data(self, initial_grid=None):
        self.set_initial_grid(initial_grid=initial_grid)
        self.grid_thresholding()
        self.convert_grid_to_link_tuple()
        self.create_graph()

    def get_nodes_and_links(self):
        return self.N, self.link_list

    def get_generated_graph(self):
        return self.graph





if __name__ == '__main__':
    graph = ErdosRenyiGraphGenerator(N=10)
    graph.set_initial_grid()
    graph.print_grid()
    graph.grid_thresholding()
    graph.print_grid(initial=False)
    graph.convert_grid_to_link_tuple_()
    print(graph.link_list)
    graph.convert_grid_to_link_tuple()
    print(graph.link_list)
    print(graph.link_list[0])
    graph.generate_all_graph_data()