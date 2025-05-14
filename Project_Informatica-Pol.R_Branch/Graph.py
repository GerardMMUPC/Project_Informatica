import matplotlib.pyplot as plt
from Node import Node, Distance, AddNeighbor
from Segment import Segment

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []


def AddNode(g, n):
    for node in g.nodes:
        if node.name == n.name:
            return False

    g.nodes.append(n)
    return True


def AddSegment(g, name_origin, name_destination):
    origin_node = None
    destination_node = None

    for node in g.nodes:
        if node.name == name_origin:
            origin_node = node
        if node.name == name_destination:
            destination_node = node

    if origin_node is None or destination_node is None:
        return False

    seg = Segment(f"{origin_node.name}-{destination_node.name}", origin_node, destination_node)
    g.segments.append(seg)

    # Añadir como vecinos en ambas direcciones (grafo no dirigido)
    AddNeighbor(origin_node, destination_node)
    AddNeighbor(destination_node, origin_node)

    return True


def GetClosest(g, x, y):
    if not g.nodes:
        return None

    closest_node = min(g.nodes, key=lambda node: ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5)
    return closest_node

def Plot(graph, title="Graph of nodes"):
    plt.figure(figsize=(8, 6))

    for segment in graph.segments:
        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        plt.plot(x_values, y_values, 'k-', linewidth=1)

        mid_x = (segment.origin.x + segment.destination.x) / 2
        mid_y = (segment.origin.y + segment.destination.y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=10, ha='center', color='red')

    for node in graph.nodes:
        plt.scatter(node.x, node.y, color='black', s=50)
        plt.text(node.x, node.y, f" {node.name}", fontsize=12, verticalalignment='bottom')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(title)
    plt.grid(True)
    plt.show()


def PlotNode(g, nameOrigin, title="Graph view from node"):
    origin_node = None
    for node in g.nodes:
        if node.name == nameOrigin:
            origin_node = node
            break

    if origin_node is None:
        return False

    plt.figure(figsize=(8, 6))

    for segment in g.segments:
        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        plt.plot(x_values, y_values, 'gray', linewidth=1)

    for neighbor in origin_node.neighbors:
        plt.scatter(neighbor.x, neighbor.y, color='green', s=80)
        plt.plot([origin_node.x, neighbor.x], [origin_node.y, neighbor.y], 'r-', linewidth=2)

        mid_x = (origin_node.x + neighbor.x) / 2
        mid_y = (origin_node.y + neighbor.y) / 2

        plt.text(mid_x, mid_y, f"{Distance(origin_node, neighbor):.2f}", fontsize=10, ha='center', color='red')

    plt.scatter(origin_node.x, origin_node.y, color='blue', s=100)

    for node in g.nodes:
        if node not in origin_node.neighbors and node != origin_node:
            plt.scatter(node.x, node.y, color='gray', s=50)

    for node in g.nodes:
        plt.text(node.x, node.y, f" {node.name}", fontsize=12, verticalalignment='bottom')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{title} {nameOrigin}")
    plt.grid(True)
    plt.show()

    return True

def FileGraph(filename):
    G = Graph()
    N = []
    x = []
    y = []

    try:
        print(f"Attempting to open file: {filename}")

        with open(filename, 'r') as fichero:
            line = fichero.readline().strip()
            print("Reading file...")
            if not line:
                print("File is empty or first line is blank.")
                return None

            while line != "":
                print(f"Line: {line}")
                if line.startswith("#"):
                    line = fichero.readline().strip()
                    continue

                elementos = line.split()
                print(f"Split elements: {elementos}")

                if len(elementos) == 3:
                    name = elementos[0]
                    node_x = int(elementos[1])
                    node_y = int(elementos[2])

                    node = Node(name, node_x, node_y)
                    AddNode(G,node)

                    N.append(name)
                    x.append(node_x)
                    y.append(node_y)

                    print (f"Node added: {name} at ({node_x}, {node_y})")

                elif len(elementos) == 2:
                    node1_name = elementos[0]
                    node2_name = elementos[1]

                    AddSegment(G,node1_name, node2_name)

                    print(f"Segment added between {node1_name} and {node2_name}")

                line = fichero.readline().strip()
    except Exception as e:
        print(f"Error reading file: {e}")
    return G


def find_shortest_path(g, origin, destination):
    from Path import Path
    current_paths = [Path([origin], 0)]

    while current_paths:
        current_paths.sort(key=lambda p: p.cost + Distance(p.nodes[-1], destination))
        best_path = current_paths.pop(0)
        last_node = best_path.nodes[-1]

        if last_node == destination:
            return best_path

        for neighbor in last_node.neighbors:
            if not best_path.contains_node(neighbor):
                new_path = best_path.copy()
                distance = Distance(last_node, neighbor)
                new_path.add_node(neighbor, distance)
                current_paths.append(new_path)

    return None


def find_reachable_nodes(g, start_node):
    visited = set()
    queue = [start_node]
    visited.add(start_node)

    while queue:
        current_node = queue.pop(0)

        for neighbor in current_node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return list(visited)

    return None

