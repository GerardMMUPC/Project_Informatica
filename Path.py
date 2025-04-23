#Path.py representa una seqüència de nodes en un gràfic.

class Path:
    def __init__(self):
        self.nodes = [] #Llista buida de nodes (AddNodeToPath)

    def AddNodeToPath(self, Node): #Afegeix un node a un camí
        if Node not in self.nodes:
            self.nodes.append(Node)

    def ContainsNode(self, Node): #Verifica si un node està en un camí
        return Node in self.nodes #REVISAR

#---
    def CostToNode(self, Node): #Calcula la distància total d'un camí
        cost = 0
        #Càlcul distància Euclidiana
    def PlotPath(self, Graph): #Dibuixa el camí al gràfic