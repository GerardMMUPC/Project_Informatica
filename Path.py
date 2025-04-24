#Path.py representa una seqüència de nodes en un gràfic.
import math
import matplotlib.pyplot as plt

class Path:
    def __init__(self):
        self.nodes = [] #Llista buida de nodes (AddNodeToPath)
        self.cost = 0.0

    def AddNodeToPath(self, Node): #Afegeix un node a un camí
        if self.nodes:
            last_node = self.nodes[-1]
            self.cost += Distance(last_node, Node)
        self.nodes.append(Node)

    def ContainsNode(self, Node): #Verifica si un node està en un camí
        return Node in self.nodes #REVISAR

#---
    def CostToNode(self, Node): #Calcula la distància total d'un camí
        if Node not in self.nodes:
            return -1

        total_cost = 0.0
        for i in range(len(self.nodes) - 1):
            if self.nodes[i] == Node:
                return total_cost
            total_cost += Distance(self.nodes[i], self.nodes[i + 1])

        if self.nodes[-1] == Node: #En cas de que el node sigui l'ultim
            return total_cost
        return -1

    def PlotPath(self, Graph):#Dibuixa el camí al gràfic
        if not self.nodes:
            return
        plt.figure(figsize=(8, 6))

        for segment in graph.segments:  #Dibuixa tots els segments
            x_values = [segment.origin.x, segment.destination.x]
            y_values = [segment.origin.y, segment.destination.y]
            plt.plot(x_values, y_values, color='gray', linewidth=1)

            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            plt.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=8, ha='center', color='gray')

        for i in range(len(self.nodes) - 1):    #Dibuixa en vermell els segments del camí
            x_values = [self.nodes[i].x, self.nodes[i + 1].x]
            y_values = [self.nodes[i].y, self.nodes[i + 1].y]
            plt.plot(x_values, y_values, color='red', linewidth=2)

            mid_x = (self.nodes[i].x + self.nodes[i + 1].x) / 2
            mid_y = (self.nodes[i].y + self.nodes[i + 1].y) / 2
            plt.text(mid_x, mid_y, f"{Distance(self.nodes[i], self.nodes[i + 1]):.2f}",
                     fontsize=10, ha='center', color='red', weight='bold')
        for Node in graph.nodes:
            if Node in self.nodes:
                # Highlight nodes in the path
                plt.scatter(Node.x, Node.y, color='red', s=100)
            else:
                plt.scatter(Node.x, Node.y, color='black', s=50)
            plt.text(Node.x, Node.y, f" {Node.name}", fontsize=12, verticalalignment='bottom')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(f"Path from {self.nodes[0].name} to {self.nodes[-1].name}\nTotal cost: {self.cost:.2f}")
        plt.grid(True)
        plt.show()


def FindShortestPath(g, origin_name, destination_name):
    # Trobem els Nodes d'origen i destinació
    origin = None
    destination = None
    for Node in g.nodes:
        if node.name == origin_name:
            origin = Node
        if node.name == destination_name:
            destination = Node

    if not origin or not destination:
        return None

    # Iniciem llista de camins oberts i tancats
    open_paths = [Path()]
    open_paths[0].AddNodeToPath(origin)
    closed_paths = []

    while open_paths:
        # Trobem el camí amb el menor cost
        min_cost = float('inf')
        current_path_index = 0
        for i, path in enumerate(open_paths):
            # Cost estimat = Cost vertader + distancia euclidiana
            last_node = path.nodes[-1]
            euclid_dist = Distance(last_node, destination)
            total_estimated_cost = path.cost + euclid_dist

            if total_estimated_cost < min_cost:
                min_cost = total_estimated_cost
                current_path_index = i

        current_path = open_paths.pop(current_path_index)

        last_node = current_path.nodes[-1] # Comprova si s'ha arribat a la destinació triada
        if last_node == destination:
            return current_path

        for neighbor in last_node.neighbors: # Seguim amb els nodes veïns
            if current_path.ContainsNode(neighbor):
                continue

            new_path = Path()   #Seguim el cami extenent l'anteriorment creat fins al Node veí
            for Node in current_path.nodes:
                new_path.AddNodeToPath(Node)
            new_path.AddNodeToPath(neighbor)

            add_new_path = True #Comprova que el camí tingui un cost menor que els altres

            for i, open_path in enumerate(open_paths): #Comprova els camins que no s'hagin tancat
                if open_path.nodes[-1] == neighbor:
                    if new_path.cost >= open_path.cost:
                        add_new_path = False
                        break
                    else:

                        open_paths.pop(i)
                        break

            if add_new_path:    #Comprova els camins tancats
                for i, closed_path in enumerate(closed_paths):
                    if closed_path.nodes[-1] == neighbor:
                        if new_path.cost >= closed_path.cost:
                            add_new_path = False
                            break
                        else:
                            closed_paths.pop(i)
                            break

            if add_new_path:
                open_paths.append(new_path)

        closed_paths.append(current_path)

    #Si no es troba cap camí:
    return None