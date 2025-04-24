# path.py
import math

class Path:
    def __init__(self, nodes=None, cost=0):
        self.nodes = nodes if nodes is not None else []
        self.cost = cost

    def add_node(self, node, cost):
        self.nodes.append(node)
        self.cost += cost

    def contains_node(self, node):
        return node in self.nodes

    def cost_to_node(self, node):
        total = 0
        for i in range(len(self.nodes) - 1):
            if self.nodes[i] == node:
                return total
            total += self.nodes[i].distance(self.nodes[i+1])
        return -1

    def copy(self):
        return Path(self.nodes[:], self.cost)

    def __repr__(self):
        return f"Cost: {self.cost:.2f} -> {[node.name for node in self.nodes]}"


def plot_path(graph, path):
    for i in range(len(path.nodes) - 1):
        graph.plot_segment(path.nodes[i], path.nodes[i + 1], color="blue")



