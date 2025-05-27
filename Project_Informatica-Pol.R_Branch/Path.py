# path.py
import math


class Path:
    def __init__(self, nodes=None, cost=0):
        self.nodes = nodes if nodes else []
        self.cost = cost

    def copy(self):
        return Path(self.nodes.copy(), self.cost)

    def add_node(self, node, distance):
        self.nodes.append(node)
        self.cost += distance

    def contains_node(self, node):
        return node in self.nodes

    def __repr__(self):
        return f"Path({[n.name for n in self.nodes]}, cost={self.cost:.2f})"

def Add_Node_Path(Path, node):
    Path.nodes.append(node)

def Contains_Node(Path, node):
        if node in Path.nodes:
            return True
        else:
            return False

def Cost_To_Node(Path, node):
    total = 0
    for i in range(len(Path.nodes) - 1):
        current_node = Path.nodes[i]
        next_node = Path.nodes[i + 1]
        total += current_node.distance(next_node)
        if current_node == node:
            return total
    return -1


def Plot_Path(graph, Path):
    for i in range(len(Path.nodes) - 1):
        graph.plot_segment(Path.nodes[i], Path.nodes[i + 1], color="blue")