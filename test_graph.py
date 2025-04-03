from Graph import *


def CreateGraph_1():
    G = Graph()

    G.AddNode(Node("A", 1, 20))
    G.AddNode(Node("B", 8, 17))
    G.AddNode(Node("C", 15, 20))
    G.AddNode(Node("D", 18, 15))
    G.AddNode(Node("E", 2, 4))
    G.AddNode(Node("F", 6, 5))
    G.AddNode(Node("G", 12, 12))
    G.AddNode(Node("H", 10, 3))
    G.AddNode(Node("I", 19, 1))
    G.AddNode(Node("J", 13, 5))
    G.AddNode(Node("K", 3, 15))
    G.AddNode(Node("L", 4, 10))

    G.AddSegment( "A", "B")
    G.AddSegment("A", "E")
    G.AddSegment("A", "K")
    G.AddSegment("B", "A")
    G.AddSegment("B", "C")
    G.AddSegment("B", "F")
    G.AddSegment("B", "K")
    G.AddSegment("B", "G")
    G.AddSegment("C", "D")
    G.AddSegment("C", "G")
    G.AddSegment("D", "G")
    G.AddSegment("D", "H")
    G.AddSegment("D", "I")
    G.AddSegment("E", "F")
    G.AddSegment("F", "L")
    G.AddSegment("G", "B")
    G.AddSegment("G", "F")
    G.AddSegment("G", "H")
    G.AddSegment("I", "D")
    G.AddSegment("I", "J")
    G.AddSegment("J", "I")
    G.AddSegment("K", "A")
    G.AddSegment("K", "L")
    G.AddSegment("L", "K")
    G.AddSegment("L", "F")

    return G

def CreateGraph_2():
    G = Graph()

    G.AddNode(Node("JFK", 40.6413, -73.7781))
    G.AddNode(Node("LAX", 33.9416, -118.4085))
    G.AddNode(Node("ORD", 41.9744, -87.9075))
    G.AddNode(Node("ATL", 33.6407, -84.4279))
    G.AddNode(Node("MIA", 25.7937, -80.2906))

    G.AddSegment("JFK", "LAX")
    G.AddSegment("JFK", "ORD")
    G.AddSegment("LAX", "ORD")
    G.AddSegment("LAX", "ATL")
    G.AddSegment("ORD", "ATL")
    G.AddSegment("ORD", "MIA")
    G.AddSegment("ATL", "MIA")

    return G


# Graph 1
print("Probando el grafo...")
G1 = CreateGraph_1()
G1.Plot(title="Grafico con nodos y segmentos")
G1.PlotNode("C",title="Grafico con nodos y segmentos")

n = G1.GetClosest(15, 5)
print(n.name)  # Se espera J
n = G1.GetClosest(8, 19)
print(n.name)  # Se espera B

#Graph 2
G2 = CreateGraph_2()
G2.Plot(title="Mapa de rutas aéreas de EE. UU.")
G2.PlotNode("JFK", title="Mapa de rutas aéreas conectados a JFK.")



