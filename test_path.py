from Path import Path
import math

class DummyNode:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return self.name

nodeA = DummyNode("A", 0, 0)
nodeB = DummyNode("B", 3, 4)
nodeC = DummyNode("C", 6, 8)

p = Path([nodeA])
p.add_node(nodeB, nodeA.distance(nodeB))
assert p.contains_node(nodeB) == True
assert p.cost_to_node(nodeB) >= 0

# Here you would add more extensive testing for plot_path and different paths
print("All path tests passed.")


# Reachability (add to graph.py)
def reachable_nodes(self, start_node):
    visited = set()
    to_visit = [start_node]

    while to_visit:
        node = to_visit.pop()
        if node not in visited:
            visited.add(node)
            for neighbor, _ in node.neighbors:
                if neighbor not in visited:
                    to_visit.append(neighbor)

    return visited

# test_graph.py should include tests for find_shortest_path and reachable_nodes