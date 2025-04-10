from Graph import *

def CreateGraph_1():
    # Create Graph object
    G1 = Graph()

    # Add nodes to the graph (A, B, C, etc.)
    AddNode(G1, Node("A", 1, 20))
    AddNode(G1, Node("B", 8, 17))
    AddNode(G1, Node("C", 15, 20))
    AddNode(G1, Node("D", 18, 15))
    AddNode(G1, Node("E", 2, 4))
    AddNode(G1, Node("F", 6, 5))
    AddNode(G1, Node("G", 12, 12))
    AddNode(G1, Node("H", 10, 3))
    AddNode(G1, Node("I", 19, 1))
    AddNode(G1, Node("J", 13, 5))
    AddNode(G1, Node("K", 3, 15))
    AddNode(G1, Node("L", 4, 10))

    # Add segments to the graph
    AddSegment(G1, "A", "B")
    AddSegment(G1, "A", "E")
    AddSegment(G1, "A", "K")
    AddSegment(G1, "B", "A")
    AddSegment(G1, "B", "C")
    AddSegment(G1, "B", "F")
    AddSegment(G1, "B", "K")
    AddSegment(G1, "B", "G")
    AddSegment(G1, "C", "D")
    AddSegment(G1, "C", "G")
    AddSegment(G1, "D", "G")
    AddSegment(G1, "D", "H")
    AddSegment(G1, "D", "I")
    AddSegment(G1, "E", "F")
    AddSegment(G1, "F", "L")
    AddSegment(G1, "G", "B")
    AddSegment(G1, "G", "F")
    AddSegment(G1, "G", "H")
    AddSegment(G1, "I", "D")
    AddSegment(G1, "I", "J")
    AddSegment(G1, "J", "I")
    AddSegment(G1, "K", "A")
    AddSegment(G1, "K", "L")
    AddSegment(G1, "L", "K")
    AddSegment(G1, "L", "F")

    return G1

def CreateGraph_2():
    # Create Graph object
    G2 = Graph()

    # Add nodes to the graph (JFK, LAX, etc.)
    AddNode(G2, Node("JFK", 40.6413, -73.7781))
    AddNode(G2, Node("LAX", 33.9416, -118.4085))
    AddNode(G2, Node("ORD", 41.9744, -87.9075))
    AddNode(G2, Node("ATL", 33.6407, -84.4279))
    AddNode(G2, Node("MIA", 25.7937, -80.2906))

    # Add segments (flights between airports)
    AddSegment(G2, "JFK", "LAX")
    AddSegment(G2, "JFK", "ORD")
    AddSegment(G2, "LAX", "ORD")
    AddSegment(G2, "LAX", "ATL")
    AddSegment(G2, "ORD", "ATL")
    AddSegment(G2, "ORD", "MIA")
    AddSegment(G2, "ATL", "MIA")

    return G2

# Graph 1
print("Probando el grafo 1...")
G1 = CreateGraph_1()
Plot(G1,title="Grafico con nodos y segmentos")
PlotNode(G1,"C", title="Grafico con nodos y segmentos")

# Get the closest node to the given coordinates
closest_node_1 = GetClosest(G1,15, 5)
print(closest_node_1.name)  # Se espera J

closest_node_2 = GetClosest(G1,8, 19)
print(closest_node_2.name)  # Se espera B

# Graph 2
print("Probando el grafo 2...")
G2 = CreateGraph_2()
Plot(G2,title="Mapa de rutas aéreas de EE. UU.")
PlotNode(G2,"JFK", title="Mapa de rutas aéreas conectados a JFK.")
