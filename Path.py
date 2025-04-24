# path.py
import math

class Path:
    def __init__(self, nodes=None, cost=0):
        self.nodes = nodes if nodes is not None else []
        self.cost = cost

    def __repr__(self):
        return f"Cost: {self.cost:.2f} -> {[node.name for node in self.nodes]}"

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



