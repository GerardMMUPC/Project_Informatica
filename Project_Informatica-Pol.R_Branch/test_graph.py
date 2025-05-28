from Graph import *

def CrearGrafo_1():
    G1 = Graph()
    # Añade nodos al grafo (A, B, C, etc.)
    Añadir_nodo(G1, Node("A", 1, 20))
    Añadir_nodo(G1, Node("B", 8, 17))
    Añadir_nodo(G1, Node("C", 15, 20))
    Añadir_nodo(G1, Node("D", 18, 15))
    Añadir_nodo(G1, Node("E", 2, 4))
    Añadir_nodo(G1, Node("F", 6, 5))
    Añadir_nodo(G1, Node("G", 12, 12))
    Añadir_nodo(G1, Node("H", 10, 3))
    Añadir_nodo(G1, Node("I", 19, 1))
    Añadir_nodo(G1, Node("J", 13, 5))
    Añadir_nodo(G1, Node("K", 3, 15))
    Añadir_nodo(G1, Node("L", 4, 10))

    # Añade segmentos al grafo
    Añadir_segmento(G1, "A", "B")
    Añadir_segmento(G1, "A", "E")
    Añadir_segmento(G1, "A", "K")
    Añadir_segmento(G1, "B", "A")
    Añadir_segmento(G1, "B", "C")
    Añadir_segmento(G1, "B", "F")
    Añadir_segmento(G1, "B", "K")
    Añadir_segmento(G1, "B", "G")
    Añadir_segmento(G1, "C", "D")
    Añadir_segmento(G1, "C", "G")
    Añadir_segmento(G1, "D", "G")
    Añadir_segmento(G1, "D", "H")
    Añadir_segmento(G1, "D", "I")
    Añadir_segmento(G1, "E", "F")
    Añadir_segmento(G1, "F", "L")
    Añadir_segmento(G1, "G", "B")
    Añadir_segmento(G1, "G", "F")
    Añadir_segmento(G1, "G", "H")
    Añadir_segmento(G1, "I", "D")
    Añadir_segmento(G1, "I", "J")
    Añadir_segmento(G1, "J", "I")
    Añadir_segmento(G1, "K", "A")
    Añadir_segmento(G1, "K", "L")
    Añadir_segmento(G1, "L", "K")
    Añadir_segmento(G1, "L", "F")

    return G1

def CrearGrafo_2():
    G2 = Graph()

    Añadir_nodo(G2, Node("JFK", 40.6413, -73.7781))
    Añadir_nodo(G2, Node("LAX", 33.9416, -118.4085))
    Añadir_nodo(G2, Node("ORD", 41.9744, -87.9075))
    Añadir_nodo(G2, Node("ATL", 33.6407, -84.4279))
    Añadir_nodo(G2, Node("MIA", 25.7937, -80.2906))

    Añadir_segmento(G2, "JFK", "LAX")
    Añadir_segmento(G2, "JFK", "ORD")
    Añadir_segmento(G2, "LAX", "ORD")
    Añadir_segmento(G2, "LAX", "ATL")
    Añadir_segmento(G2, "ORD", "ATL")
    Añadir_segmento(G2, "ORD", "MIA")
    Añadir_segmento(G2, "ATL", "MIA")

    return G2

if __name__ == "__main__":
    # Grafo 1
    print("Probando el grafo 1...")
    G1 = CrearGrafo_1()
    Plot(G1,title="Grafico con nodos y segmentos")
    PlotNodo(G1, "C", title="Gráfico con nodos y segmentos")

    # Busca el nodo mas cercano a las cordenadas proporcionadas
    closest_node_1 = Encontrar_mas_cercano(G1, 15, 5)
    print(closest_node_1.name)  # Se espera J

    closest_node_2 = Encontrar_mas_cercano(G1, 8, 19)
    print(closest_node_2.name)  # Se espera B

    # Grafo 2
    print("Probando el grafo 2...")
    G2 = CrearGrafo_2()
    Plot(G2,title="Mapa de rutas aéreas de EE. UU.")
    PlotNodo(G2, "JFK", title="Mapa de rutas aéreas conectados a JFK.")


def Cargar_Mapa_Catalunya():
    return Grafico_fichero("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")

def Cargar_Mapa_España():
    return Grafico_fichero("Spain_nav.txt", "Spain_seg.txt", "Spain_aer.txt")

def Cargar_Mapa_ECAC():
    return Grafico_fichero("ECAC_nav.txt", "ECAC_seg.txt", "ECAC_aer.txt")