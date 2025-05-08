from matplotlib.figure import Figure
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
    AddNeighbor(origin_node, destination_node)
    return True

def GetClosest(g, x, y):
    if not g.nodes:
        return None
    return min(g.nodes, key=lambda node: ((node.x - x)**2 + (node.y - y)**2)**0.5)

def Plot(graph, title="Graph of nodes"):
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.set_title(title)

    for segment in graph.segments:
        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        ax.plot(x_values, y_values, 'k-', linewidth=1)
        mid_x = (segment.origin.x + segment.destination.x) / 2
        mid_y = (segment.origin.y + segment.destination.y) / 2
        ax.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=10, ha='center', color='red')

    for node in graph.nodes:
        ax.scatter(node.x, node.y, color='black', s=50)
        ax.text(node.x, node.y, f" {node.name}", fontsize=12, verticalalignment='bottom')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_aspect('equal', adjustable='datalim')
    return fig

def PlotNode(g, nameOrigin, title="Graph view from node"):
    origin_node = next((node for node in g.nodes if node.name == nameOrigin), None)
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.set_title(f"{title} {nameOrigin}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)

    if origin_node is None:
        return fig

    for segment in g.segments:
        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        ax.plot(x_values, y_values, 'gray', linewidth=1)

    for neighbor in origin_node.neighbors:
        ax.scatter(neighbor.x, neighbor.y, color='green', s=80)
        ax.plot([origin_node.x, neighbor.x], [origin_node.y, neighbor.y], 'r-', linewidth=2)
        mid_x = (origin_node.x + neighbor.x) / 2
        mid_y = (origin_node.y + neighbor.y) / 2
        ax.text(mid_x, mid_y, f"{Distance(origin_node, neighbor):.2f}", fontsize=10, ha='center', color='red')

    ax.scatter(origin_node.x, origin_node.y, color='blue', s=100)

    for node in g.nodes:
        if node not in origin_node.neighbors and node != origin_node:
            ax.scatter(node.x, node.y, color='gray', s=50)

    for node in g.nodes:
        ax.text(node.x, node.y, f" {node.name}", fontsize=12, verticalalignment='bottom')

    ax.set_aspect('equal', adjustable='datalim')
    return fig

def FileGraph(filename):
    G = Graph()
    try:
        with open(filename, 'r') as fichero:
            for line in fichero:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                elementos = line.split()
                if len(elementos) == 3:
                    name, node_x, node_y = elementos
                    node = Node(name, int(node_x), int(node_y))
                    AddNode(G, node)
                elif len(elementos) == 2:
                    node1, node2 = elementos
                    AddSegment(G, node1, node2)
    except Exception as e:
        print(f"Error reading file: {e}")
    return G
